# Copyright (C) 2026 Sugarworm
# This file is part of Zhouyi Divination System.
#
# Zhouyi Divination System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

try:
    from lunar_python import Solar, Lunar
except ImportError:
    from simple_lunar import Solar, Lunar
from collections import Counter

# 五行生克关系
WUXING_RELATIONS = {
    "生成": {
        "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
    },
    "克制": {
        "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
    }
}

# 天干合化
TIANGAN_HE = {
    "甲": "己", "己": "甲", # 甲己合土
    "乙": "庚", "庚": "乙", # 乙庚合金
    "丙": "辛", "辛": "丙", # 丙辛合水
    "丁": "壬", "壬": "丁", # 丁壬合木
    "戊": "癸", "癸": "戊"  # 戊癸合火
}

# 地支六合
DIZHI_LIUHE = {
    "子": "丑", "丑": "子", # 子丑合土
    "寅": "亥", "亥": "寅", # 寅亥合木
    "卯": "戌", "戌": "卯", # 卯戌合火
    "辰": "酉", "酉": "辰", # 辰酉合金
    "巳": "申", "申": "巳", # 巳申合水
    "午": "未", "未": "午"  # 午未合土
}

# 地支相冲
DIZHI_CHONG = {
    "子": "午", "午": "子",
    "丑": "未", "未": "丑",
    "寅": "申", "申": "寅",
    "卯": "酉", "酉": "卯",
    "辰": "戌", "戌": "辰",
    "巳": "亥", "亥": "巳"
}

# 地支相害
DIZHI_HAI = {
    "子": "未", "未": "子",
    "丑": "午", "午": "丑",
    "寅": "巳", "巳": "寅",
    "卯": "辰", "辰": "卯",
    "申": "亥", "亥": "申",
    "酉": "戌", "戌": "酉"
}

# 地支三刑
# 简化处理：寅巳申、丑未戌、子卯

def get_bazi_analysis(year, month, day, hour):
    """
    获取八字分析结果
    """
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    
    # 获取八字干支
    year_gan = bazi.getYearGan()
    year_zhi = bazi.getYearZhi()
    month_gan = bazi.getMonthGan()
    month_zhi = bazi.getMonthZhi()
    day_gan = bazi.getDayGan()
    day_zhi = bazi.getDayZhi()
    time_gan = bazi.getTimeGan()
    time_zhi = bazi.getTimeZhi()
    
    # 获取五行
    year_wx = bazi.getYearWuXing()   # e.g. "木土"
    month_wx = bazi.getMonthWuXing() # e.g. "土火"
    day_wx = bazi.getDayWuXing()     # e.g. "木金"
    time_wx = bazi.getTimeWuXing()   # e.g. "金土"
    
    # 统计五行数量 (基于天干地支)
    # 注意：lunar_python 的 getXxxWuXing() 返回的是纳音五行还是正五行？
    # Check: getYearWuXing() returns string like "木土" (Gan=Mu, Zhi=Tu)
    
    wuxing_cnt = Counter()
    
    # 解析 "木土" 这种字符串
    wuxing_cnt[year_wx[0]] += 1
    wuxing_cnt[year_wx[1]] += 1
    wuxing_cnt[month_wx[0]] += 1
    wuxing_cnt[month_wx[1]] += 1
    wuxing_cnt[day_wx[0]] += 1
    wuxing_cnt[day_wx[1]] += 1
    wuxing_cnt[time_wx[0]] += 1
    wuxing_cnt[time_wx[1]] += 1
    
    # 缺失五行
    missing_wuxing = []
    for wx in ["金", "木", "水", "火", "土"]:
        if wuxing_cnt[wx] == 0:
            missing_wuxing.append(wx)
            
    # 日主强弱 (简化版：看月令是否生助)
    # 月令：month_zhi
    # 日元：day_gan
    # 需要映射地支对应的五行和天干对应的五行
    # 这里简单判断月支五行是否生助日干五行
    day_gan_wx = day_wx[0]
    month_zhi_wx = month_wx[1]
    
    is_strong = False
    relation_with_month = "平"
    if day_gan_wx == month_zhi_wx:
        relation_with_month = "同气"
        is_strong = True
    elif WUXING_RELATIONS["生成"][month_zhi_wx] == day_gan_wx:
        relation_with_month = "得令" # 月令生身
        is_strong = True
    else:
        relation_with_month = "不得令"
        
    strength_desc = "偏强" if is_strong else "偏弱"
    
    return {
        "solar": solar.toYmdHms(),
        "lunar": lunar.toFullString(),
        "bazi": [
            f"{year_gan}{year_zhi}",
            f"{month_gan}{month_zhi}",
            f"{day_gan}{day_zhi}",
            f"{time_gan}{time_zhi}"
        ],
        "wuxing_counts": dict(wuxing_cnt),
        "missing_wuxing": missing_wuxing,
        "day_master": {
            "gan": day_gan,
            "wuxing": day_gan_wx,
            "strength": strength_desc,
            "month_relation": relation_with_month
        },
        "spouse_palace": day_zhi # 夫妻宫
    }

def check_marriage_compatibility(male_data, female_data):
    """
    合婚分析
    male_data, female_data 是 get_bazi_analysis 的返回结果
    """
    score = 0
    analysis = []
    
    # 1. 生肖合婚 (年支)
    male_year_zhi = male_data["bazi"][0][1]
    female_year_zhi = female_data["bazi"][0][1]
    
    if DIZHI_LIUHE.get(male_year_zhi) == female_year_zhi:
        score += 20
        analysis.append("【年支相合】 生肖六合，大吉。基础稳固，缘分深厚。")
    elif DIZHI_CHONG.get(male_year_zhi) == female_year_zhi:
        score -= 10
        analysis.append("【年支相冲】 生肖相冲，基础不稳，易有冲突。建议多沟通包容。")
    elif DIZHI_HAI.get(male_year_zhi) == female_year_zhi:
        score -= 5
        analysis.append("【年支相害】 生肖相害，易生嫌隙。")
    else:
        score += 10
        analysis.append("【年支无冲】 生肖配合一般，无严重冲突。")
        
    # 2. 日干合婚 (日元)
    male_day_gan = male_data["day_master"]["gan"]
    female_day_gan = female_data["day_master"]["gan"]
    
    # Check if we have WuXing for Day Gan (should be 1 char)
    # male_day_gan e.g. "甲"
    # Need to know its wuxing.
    # WUXING_RELATIONS keys are "木", "火"...
    # Need GAN_WUXING mapping.
    
    GAN_WUXING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    male_wx = GAN_WUXING.get(male_day_gan)
    female_wx = GAN_WUXING.get(female_day_gan)
    
    if TIANGAN_HE.get(male_day_gan) == female_day_gan:
        score += 30
        analysis.append("【日干相合】 夫妻心意相通，性格互补，非常理想的组合。")
    elif male_wx and female_wx and (WUXING_RELATIONS["克制"].get(male_wx) == female_wx or \
         WUXING_RELATIONS["克制"].get(female_wx) == male_wx):
         # 简单的五行相克
         score -= 5
         analysis.append("【日干相克】 性格上可能存在差异，需要磨合。")
    else:
        score += 10
        analysis.append("【日干平和】 彼此关系平等，相敬如宾。")

    # 3. 夫妻宫合婚 (日支)
    male_day_zhi = male_data["spouse_palace"]
    female_day_zhi = female_data["spouse_palace"]
    
    if DIZHI_LIUHE.get(male_day_zhi) == female_day_zhi:
        score += 20
        analysis.append("【日支相合】 夫妻宫六合，婚后生活和谐，恩爱有加。")
    elif DIZHI_CHONG.get(male_day_zhi) == female_day_zhi:
        score -= 15
        analysis.append("【日支相冲】 夫妻宫相冲，婚后易有动荡或争吵，需注意经营。")
    elif DIZHI_HAI.get(male_day_zhi) == female_day_zhi:
        score -= 10
        analysis.append("【日支相害】 夫妻宫相害，易有不和。")
    else:
        score += 10
        analysis.append("【日支无冲】 夫妻宫稳定。")
        
    # 4. 五行互补
    # 比较缺失五行。如果一方缺的，另一方旺（这里简单判断数量），则互补
    male_missing = set(male_data["missing_wuxing"])
    female_missing = set(female_data["missing_wuxing"])
    male_counts = male_data["wuxing_counts"]
    female_counts = female_data["wuxing_counts"]
    
    complementary = False
    
    # 检查男方缺的，女方是否有 >= 3
    for m in male_missing:
        if female_counts.get(m, 0) >= 3:
            complementary = True
            analysis.append(f"【五行互补】 男方缺{m}，女方{m}旺，女方能助旺男方。")
            
    # 检查女方缺的，男方是否有 >= 3
    for m in female_missing:
        if male_counts.get(m, 0) >= 3:
            complementary = True
            analysis.append(f"【五行互补】 女方缺{m}，男方{m}旺，男方能助旺女方。")
            
    if complementary:
        score += 20
    else:
        # 如果都没有缺失，或者都不旺
        if not male_missing and not female_missing:
            score += 10
            analysis.append("【五行均衡】 双方五行俱全，自带平衡。")
        else:
            analysis.append("【五行普通】 五行互补性一般。")
            score += 5

    # 评分归一化
    if score > 100: score = 100
    if score < 0: score = 0
    
    level = "中等"
    if score >= 85: level = "上上等婚"
    elif score >= 75: level = "上等婚"
    elif score >= 60: level = "中等婚"
    else: level = "下等婚 (需谨慎)"
    
    return {
        "score": score,
        "level": level,
        "analysis": analysis,
        "male_info": {
            "bazi": " ".join(male_data["bazi"]),
            "day_master": male_data["day_master"]["gan"]
        },
        "female_info": {
            "bazi": " ".join(female_data["bazi"]),
            "day_master": female_data["day_master"]["gan"]
        }
    }
