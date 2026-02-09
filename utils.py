# Copyright (C) 2026 Sugarworm
# This file is part of Zhouyi Divination System.
#
# Zhouyi Divination System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import sys
from ichingshifa import ichingshifa
import json
import os
from strokes import strokes
import re

# Load Zhuge Data
ZHUGE_DATA = []
zhuge_file = os.path.join(os.path.dirname(__file__), "zhuge_data.json")
if os.path.exists(zhuge_file):
    try:
        with open(zhuge_file, "r", encoding="utf-8") as f:
            ZHUGE_DATA = json.load(f)
    except:
        pass

HEX_EN = {
    "乾": "The Creative", "坤": "The Receptive", "屯": "Difficulty at the Beginning", "蒙": "Youthful Folly",
    "需": "Waiting", "讼": "Conflict", "师": "The Army", "比": "Holding Together",
    "小畜": "The Taming Power of the Small", "履": "Treading", "泰": "Peace", "否": "Standstill",
    "同人": "Fellowship with Men", "大有": "Possession in Great Measure", "谦": "Modesty", "豫": "Enthusiasm",
    "随": "Following", "蛊": "Work on What Has Been Spoiled", "临": "Approach", "观": "Contemplation",
    "噬嗑": "Biting Through", "贲": "Grace", "剥": "Splitting Apart", "复": "Return",
    "无妄": "Innocence", "大畜": "The Taming Power of the Great", "颐": "The Corners of the Mouth", "大过": "Preponderance of the Great",
    "坎": "The Abysmal", "离": "The Clinging", "咸": "Influence", "恒": "Duration",
    "遯": "Retreat", "大壮": "The Power of the Great", "晋": "Progress", "明夷": "Darkening of the Light",
    "家人": "The Family", "睽": "Opposition", "蹇": "Obstruction", "解": "Deliverance",
    "损": "Decrease", "益": "Increase", "夬": "Break-through", "姤": "Coming to Meet",
    "萃": "Gathering Together", "升": "Pushing Upward", "困": "Oppression", "井": "The Well",
    "革": "Revolution", "鼎": "The Cauldron", "震": "The Arousing", "艮": "Keeping Still",
    "渐": "Development", "归妹": "The Marrying Maiden", "丰": "Abundance", "旅": "The Wanderer",
    "巽": "The Gentle", "兑": "The Joyous", "涣": "Dispersion", "节": "Limitation",
    "中孚": "Inner Truth", "小过": "Preponderance of the Small", "既济": "After Completion", "未济": "Before Completion",
    "乾为天": "The Creative", "坤为地": "The Receptive", "水雷屯": "Difficulty at the Beginning", "山水蒙": "Youthful Folly",
    "水天需": "Waiting", "天水讼": "Conflict", "地水师": "The Army", "水地比": "Holding Together",
    "风天小畜": "The Taming Power of the Small", "天泽履": "Treading", "地天泰": "Peace", "天地否": "Standstill",
    "天火同人": "Fellowship with Men", "火天大有": "Possession in Great Measure", "地山谦": "Modesty", "雷地豫": "Enthusiasm",
    "泽雷随": "Following", "山风蛊": "Work on What Has Been Spoiled", "地泽临": "Approach", "风地观": "Contemplation",
    "火雷噬嗑": "Biting Through", "山火贲": "Grace", "山地剥": "Splitting Apart", "地雷复": "Return",
    "天雷无妄": "Innocence", "山天大畜": "The Taming Power of the Great", "山雷颐": "The Corners of the Mouth", "泽风大过": "Preponderance of the Great",
    "坎为水": "The Abysmal", "离为火": "The Clinging", "泽山咸": "Influence", "雷风恒": "Duration",
    "天山遯": "Retreat", "雷天大壮": "The Power of the Great", "火地晋": "Progress", "地火明夷": "Darkening of the Light",
    "风火家人": "The Family", "火泽睽": "Opposition", "水山蹇": "Obstruction", "雷水解": "Deliverance",
    "山泽损": "Decrease", "风雷益": "Increase", "泽天夬": "Break-through", "天风姤": "Coming to Meet",
    "泽地萃": "Gathering Together", "地风升": "Pushing Upward", "泽水困": "Oppression", "水风井": "The Well",
    "泽火革": "Revolution", "火风鼎": "The Cauldron", "震为雷": "The Arousing", "艮为山": "Keeping Still",
    "风山渐": "Development", "雷泽归妹": "The Marrying Maiden", "雷火丰": "Abundance", "火山旅": "The Wanderer",
    "巽为风": "The Gentle", "兑为泽": "The Joyous", "风水涣": "Dispersion", "水泽节": "Limitation",
    "风泽中孚": "Inner Truth", "雷山小过": "Preponderance of the Small", "水火既济": "After Completion", "火水未济": "Before Completion",
    
    # Traditional Chinese Mappings
    "訟": "Conflict", "師": "The Army", "謙": "Modesty", "隨": "Following", "蠱": "Work on What Has Been Spoiled",
    "臨": "Approach", "觀": "Contemplation", "賁": "Grace", "剝": "Splitting Apart", "復": "Return", "無妄": "Innocence",
    "頤": "The Corners of the Mouth", "大過": "Preponderance of the Great", "離": "The Clinging", "恆": "Duration",
    "大壯": "The Power of the Great", "晉": "Progress", "損": "Decrease", "漸": "Development", "歸妹": "The Marrying Maiden",
    "豐": "Abundance", "兌": "The Joyous", "渙": "Dispersion", "節": "Limitation", "小過": "Preponderance of the Small",
    "既濟": "After Completion", "未濟": "Before Completion"
}

NAME_TO_INDEX = {
    "乾": 1, "坤": 2, "屯": 3, "蒙": 4, "需": 5, "讼": 6, "师": 7, "比": 8,
    "小畜": 9, "履": 10, "泰": 11, "否": 12, "同人": 13, "大有": 14, "谦": 15, "豫": 16,
    "随": 17, "蛊": 18, "临": 19, "观": 20, "噬嗑": 21, "贲": 22, "剥": 23, "复": 24,
    "无妄": 25, "大畜": 26, "颐": 27, "大过": 28, "坎": 29, "离": 30, "咸": 31, "恒": 32,
    "遯": 33, "大壮": 34, "晋": 35, "明夷": 36, "家人": 37, "睽": 38, "蹇": 39, "解": 40,
    "损": 41, "益": 42, "夬": 43, "姤": 44, "萃": 45, "升": 46, "困": 47, "井": 48,
    "革": 49, "鼎": 50, "震": 51, "艮": 52, "渐": 53, "归妹": 54, "丰": 55, "旅": 56,
    "巽": 57, "兑": 58, "涣": 59, "节": 60, "中孚": 61, "小过": 62, "既济": 63, "未济": 64,
    
    # Traditional Chinese Mappings for Index
    "訟": 6, "師": 7, "謙": 15, "隨": 17, "蠱": 18, "臨": 19, "觀": 20, "賁": 22, "剝": 23, "復": 24,
    "無妄": 25, "頤": 27, "大過": 28, "離": 30, "恆": 32, "大壯": 34, "晉": 35, "損": 41,
    "漸": 53, "歸妹": 54, "豐": 55, "兌": 58, "渙": 59, "節": 60, "小過": 62, "既濟": 63, "未濟": 64
}

# 1:Qian(Metal), 2:Dui(Metal), 3:Li(Fire), 4:Zhen(Wood), 5:Xun(Wood), 6:Kan(Water), 7:Gen(Earth), 8:Kun(Earth)
TRIGRAM_ELEMENTS = {
    1: "metal", 2: "metal", 3: "fire", 4: "wood", 5: "wood", 6: "water", 7: "earth", 8: "earth"
}
ELEMENT_RELATIONS = {
    "metal": {"sheng": "water", "ke": "wood"},
    "wood": {"sheng": "fire", "ke": "earth"},
    "water": {"sheng": "wood", "ke": "fire"},
    "fire": {"sheng": "earth", "ke": "metal"},
    "earth": {"sheng": "metal", "ke": "water"}
}

# Load English Yi Jing Data
YI_JING_EN = {}
yijing_file = os.path.join(os.path.dirname(__file__), "yi_jing_en.json")
if os.path.exists(yijing_file):
    try:
        with open(yijing_file, "r", encoding="utf-8") as f:
            YI_JING_EN = json.load(f)
    except:
        pass

# Load French Yi Jing Data
YI_JING_FR = {}
yijing_fr_file = os.path.join(os.path.dirname(__file__), "yi_jing_fr.json")
if os.path.exists(yijing_fr_file):
    try:
        with open(yijing_fr_file, "r", encoding="utf-8") as f:
            YI_JING_FR = json.load(f)
    except:
        pass

def get_strokes(char):
    if char.isdigit():
        return int(char)
    if 'a' <= char.lower() <= 'z':
        # English Numerology: A=1, B=2...
        return ord(char.lower()) - 96
    
    # Use strokes library for Chinese chars
    try:
        # strokes library returns int for simplified/traditional
        s = strokes(char)
        if isinstance(s, int):
            return s
        # Sometimes it might return 0 if not found?
        if s > 0: return s
    except:
        pass
        
    return 0 # Default fallback

def calculate_hexagram_from_text(text, focus="general"):
    """
    Meihua Yishu Logic:
    1. Split text into Upper (First half) and Lower (Second half).
    2. Sum strokes/values for Upper and Lower.
    3. Calculate Hexagram indices (mod 8).
    4. Calculate Moving Yao (Total mod 6).
    """
    if not text:
        return None

    mid = len(text) // 2
    if len(text) == 1:
        upper_text = text
        lower_text = text
    elif len(text) % 2 != 0:
        # Odd length: Upper has less chars (Yang), Lower has more (Yin)
        upper_text = text[:mid]
        lower_text = text[mid:]
    else:
        upper_text = text[:mid]
        lower_text = text[mid:]

    upper_sum = sum(get_strokes(c) for c in upper_text)
    lower_sum = sum(get_strokes(c) for c in lower_text)
    total_sum = upper_sum + lower_sum

    return calculate_hexagram_from_numbers(upper_sum, lower_sum, total_sum, focus)

def calculate_zhuge_from_text(text):
    """
    Zhuge Shenshu Logic:
    1. Take 3 chars (or first 3 chars, or map text to 3 numbers).
    2. If text length < 3, pad or repeat? 
    3. Use standard "Report 3 characters" method.
    """
    if not text:
        return {"error": "请输入至少一个字"}
    
    chars = list(text)
    if len(chars) < 3:
        # Pad with last char
        while len(chars) < 3:
            chars.append(chars[-1])
    
    # Take first 3 for calculation
    c1, c2, c3 = chars[0], chars[1], chars[2]
    
    s1 = get_strokes(c1)
    s2 = get_strokes(c2)
    s3 = get_strokes(c3)
    
    n1 = s1 % 10
    n2 = s2 % 10
    n3 = s3 % 10
    
    total_val = n1 * 100 + n2 * 10 + n3
    
    sign_idx = total_val % 384
    if sign_idx == 0:
        sign_idx = 384
        
    # Find poem
    result = None
    for item in ZHUGE_DATA:
        if item["index"] == sign_idx:
            result = item
            break
            
    if not result:
        # Fallback
        result = {
            "index": sign_idx, 
            "poem": "签文暂缺（数据扩充中）", 
            "explain": "请查阅《诸葛神数》原书第" + str(sign_idx) + "签。"
        }
        
    return {
        "type": "zhuge",
        "input": text[:3],
        "strokes": [s1, s2, s3],
        "numbers": [n1, n2, n3],
        "index": sign_idx,
        "poem": result["poem"],
        "explain": result["explain"],
        "poem_en": result.get("poem_en", ""),
        "explain_en": result.get("explain_en", "")
    }

def get_hex_en(name):
    # Try full name
    if name in HEX_EN:
        return HEX_EN[name]
    # Try short name (last char usually)
    if len(name) > 1:
        short = name[-1]
        if short in HEX_EN:
            return HEX_EN[short]
    return name

def calculate_meihua_interpretation(upper_val, lower_val, moving_yao, focus):
    if focus == "general":
        return {}
        
    upper_rem = upper_val % 8
    if upper_rem == 0: upper_rem = 8

    lower_rem = lower_val % 8
    if lower_rem == 0: lower_rem = 8
    
    # Determine Ti (Body) and Yong (Application)
    # Moving yao 1-3: Lower changes (Yong), Upper static (Ti)
    # Moving yao 4-6: Upper changes (Yong), Lower static (Ti)
    
    if moving_yao <= 3:
        ti_idx = upper_rem
        yong_idx = lower_rem
        position = "Lower Trigram Moves"
    else:
        ti_idx = lower_rem
        yong_idx = upper_rem
        position = "Upper Trigram Moves"
        
    ti_element = TRIGRAM_ELEMENTS[ti_idx]
    yong_element = TRIGRAM_ELEMENTS[yong_idx]
    
    relation = "equal"
    if ti_element == yong_element:
        relation = "equal" # Bi He
    elif ELEMENT_RELATIONS[yong_element]["sheng"] == ti_element:
        relation = "yong_sheng_ti" # Great Auspicious
    elif ELEMENT_RELATIONS[ti_element]["sheng"] == yong_element:
        relation = "ti_sheng_yong" # Exhaustion
    elif ELEMENT_RELATIONS[yong_element]["ke"] == ti_element:
        relation = "yong_ke_ti" # Ominous
    elif ELEMENT_RELATIONS[ti_element]["ke"] == yong_element:
        relation = "ti_ke_yong" # Auspicious but hard
        
    advice = ""
    # Interpretation based on Focus and Relation
    if focus == "love": # 姻缘
        if relation == "yong_sheng_ti":
            advice = "Great Match. The other party loves you deeply. Success comes easily."
        elif relation == "equal":
            advice = "Harmonious relationship. Mutual understanding."
        elif relation == "ti_sheng_yong":
            advice = "You give more than you receive. Need patience."
        elif relation == "ti_ke_yong":
            advice = "You can control the situation, but need effort to win the heart."
        elif relation == "yong_ke_ti":
            advice = "Obstacles and pressure. The other party might be rejecting or situation is against you."
            
    elif focus == "wealth": # 财运
        if relation == "yong_sheng_ti":
            advice = "Great Fortune. Wealth comes to you naturally."
        elif relation == "equal":
            advice = "Good financial partnership. Stable income."
        elif relation == "ti_sheng_yong":
            advice = "Investment required. Money flows out before coming in."
        elif relation == "ti_ke_yong":
            advice = "Wealth through hard work. You can get it if you try."
        elif relation == "yong_ke_ti":
            advice = "Risk of loss. Bad for investment. Be conservative."
            
    elif focus == "career": # 官运/事业
        if relation == "yong_sheng_ti":
            advice = "Promotion and help from nobles. Career rises."
        elif relation == "equal":
            advice = "Cooperation and support from colleagues."
        elif relation == "ti_sheng_yong":
            advice = "Working hard for the team. Exhaustion but contributing."
        elif relation == "ti_ke_yong":
            advice = "Overcoming challenges. Success through capability."
        elif relation == "yong_ke_ti":
            advice = "Pressure from superiors or environment. Difficulties ahead."
            
    return {
        "focus": focus,
        "ti_element": ti_element,
        "yong_element": yong_element,
        "relation": relation,
        "advice": advice
    }

def calculate_hexagram_from_numbers(upper_val, lower_val, total_val=None, focus="general"):
    if total_val is None:
        total_val = upper_val + lower_val
        
    upper_rem = upper_val % 8
    if upper_rem == 0: upper_rem = 8

    lower_rem = lower_val % 8
    if lower_rem == 0: lower_rem = 8

    moving_yao = total_val % 6
    if moving_yao == 0: moving_yao = 6
    
    # 1:777 (Qian), 2:778 (Dui), 3:787 (Li), 4:788 (Zhen)
    # 5:877 (Xun), 6:878 (Kan), 7:887 (Gen), 8:888 (Kun)
    gua_map = {1:"777", 2:"778", 3:"787", 4:"788", 5:"877", 6:"878", 7:"887", 8:"888"}
    
    # Base code: Lower Gua (lines 1-3) + Upper Gua (lines 4-6)
    base_code = gua_map[lower_rem] + gua_map[upper_rem]
    
    idx = moving_yao - 1
    char_list = list(base_code)
    original = char_list[idx]
    
    if original == '7':
        char_list[idx] = '9' # Old Yang
    elif original == '8':
        char_list[idx] = '6' # Old Yin
        
    final_code = "".join(char_list)
    
    # Get details from ichingshifa
    iching = ichingshifa.Iching()
    result = iching.mget_bookgua_details(final_code)
    
    # Parse result
    # result structure: [code, BenGuaName, ZhiGuaName, DictOfLines, SummaryTuple]
    
    response = {
        "ben_gua": result[1],
        "zhi_gua": result[2],
        "moving_yao": moving_yao,
        "gua_code": final_code,
        "upper_val": upper_val,
        "lower_val": lower_val,
        "total_val": total_val
    }
    
    summary_tuple = result[4]
    # summary_tuple: (MovingYaoInfo, HexagramRelation, MainText, [Extra])
    
    response["summary"] = f"{summary_tuple[0]} {summary_tuple[1]}"
    
    main_text = ""
    if len(summary_tuple) >= 4:
        main_text = summary_tuple[3]
    elif len(summary_tuple) == 3:
        main_text = summary_tuple[2]
        
    # Append specific yao text if short
    if len(main_text) < 10:
        yao_text = result[3].get(moving_yao, "")
        if yao_text:
            main_text = f"{main_text}\n{yao_text}"
            
    response["main_text"] = main_text
    
    # Add Tuan (Judgement) for Ben Gua
    tuan_text = result[3].get(0, "")
    response["ben_gua_text"] = tuan_text
    
    # English Translations
    response["ben_gua_en"] = get_hex_en(result[1])
    response["zhi_gua_en"] = get_hex_en(result[2])
    
    # Summary Translation
    summary_en = response["summary"]
    
    # Match pattern: 動爻有【1】根。 【家人之同人】
    match = re.search(r"動爻有【(\d+)】根。[ \t]*【(.*?)之(.*?)】", summary_en)
    if match:
        count = match.group(1)
        hex1 = match.group(2)
        hex2 = match.group(3)
        hex1_en = get_hex_en(hex1)
        hex2_en = get_hex_en(hex2)
        summary_en = f"Moving Lines: {count}. {hex1_en} -> {hex2_en}"
    else:
        summary_en = summary_en.replace("吉", "Auspicious").replace("凶", "Ominous").replace("悔", "Regret").replace("吝", "Stingy/Small Trouble")
        
    response["summary_en"] = summary_en
    
    # Add Focus Advice
    if focus != "general":
        interpretation = calculate_meihua_interpretation(upper_val, lower_val, moving_yao, focus)
        response.update(interpretation)
    
    # Populate English Text from YI_JING_EN
    ben_gua_name = result[1]
    hex_idx = NAME_TO_INDEX.get(ben_gua_name)
    
    if hex_idx:
        en_data = YI_JING_EN.get(str(hex_idx))
        if en_data:
            response["ben_gua_text_en"] = en_data.get("judgement", "")
            
            line_text_en = en_data.get("lines", {}).get(str(moving_yao), "")
            if line_text_en:
                response["main_text_en"] = line_text_en
            else:
                response["main_text_en"] = "(English line text unavailable)"
        else:
            response["main_text_en"] = "(Classical text translation unavailable)"
            
        # Populate French Text
        fr_data = YI_JING_FR.get(str(hex_idx))
        if fr_data:
            response["ben_gua_fr"] = fr_data.get("name", ben_gua_name)
            # French Judgement
            response["ben_gua_text_fr"] = fr_data.get("judgement", "")
            
            # French Line
            line_text_fr = fr_data.get("lines", {}).get(str(moving_yao), "")
            if line_text_fr:
                response["main_text_fr"] = line_text_fr
            else:
                response["main_text_fr"] = "(Texte français indisponible)"
        else:
            response["ben_gua_fr"] = ben_gua_name
            response["main_text_fr"] = "(Traduction française indisponible)"
            
        # Zhi Gua Name FR
        zhi_gua_name = result[2]
        zhi_idx = NAME_TO_INDEX.get(zhi_gua_name)
        if zhi_idx and str(zhi_idx) in YI_JING_FR:
            response["zhi_gua_fr"] = YI_JING_FR[str(zhi_idx)]["name"]
        else:
            response["zhi_gua_fr"] = zhi_gua_name
            
        # Summary FR (Simple translation)
        # "Moving Lines: X. Hex1 -> Hex2"
        # "Traits mobiles: X. Hex1 -> Hex2"
        if match:
            hex1_fr = response.get("ben_gua_fr", hex1)
            hex2_fr = response.get("zhi_gua_fr", hex2)
            response["summary_fr"] = f"Traits mobiles: {count}. {hex1_fr} -> {hex2_fr}"
        else:
            # Simple replacements
            summary_fr = response["summary"]
            summary_fr = summary_fr.replace("吉", "Faste (Bon)").replace("凶", "Néfaste (Mauvais)").replace("悔", "Regret").replace("吝", "Petit souci")
            response["summary_fr"] = summary_fr

    else:
        response["main_text_en"] = "(Classical text translation unavailable)"
        response["main_text_fr"] = "(Traduction française indisponible)"
    
    return response

def get_random_divination():
    iching = ichingshifa.Iching()
    result = iching.bookgua_details()
    
    response = {
        "ben_gua": result[1],
        "zhi_gua": result[2] if len(result) > 2 else "",
        "raw_result": str(result)
    }
    
    if len(result) > 4:
        summary_tuple = result[4]
        response["summary"] = f"{summary_tuple[0]} {summary_tuple[1]}"
        main_text = ""
        if len(summary_tuple) >= 4:
            main_text = summary_tuple[3]
        elif len(summary_tuple) == 3:
            main_text = summary_tuple[2]
        response["main_text"] = main_text
        response["ben_gua_text"] = result[3].get(0, "")
        
        # Add EN
        response["ben_gua_en"] = get_hex_en(response["ben_gua"])
        response["zhi_gua_en"] = get_hex_en(response["zhi_gua"])
        summary_en = response["summary"]
        
        match = re.search(r"動爻有【(\d+)】根。[ \t]*【(.*?)之(.*?)】", summary_en)
        if match:
            count = match.group(1)
            hex1 = match.group(2)
            hex2 = match.group(3)
            hex1_en = get_hex_en(hex1)
            hex2_en = get_hex_en(hex2)
            summary_en = f"Moving Lines: {count}. {hex1_en} -> {hex2_en}"
        else:
            summary_en = summary_en.replace("吉", "Auspicious").replace("凶", "Ominous")
            
        response["summary_en"] = summary_en
        
        # Populate English Text
        ben_gua_name = response["ben_gua"]
        hex_idx = NAME_TO_INDEX.get(ben_gua_name)
        
        if hex_idx:
            en_data = YI_JING_EN.get(str(hex_idx))
            if en_data:
                response["ben_gua_text_en"] = en_data.get("judgement", "")
                
                # Identify moving lines from code
                # code is in result[0] ? No, result[0] is not passed in response.
                # But result[0] is code?
                # In calculate_hexagram_from_numbers, result = iching.mget_bookgua_details(final_code)
                # In get_random_divination, result = iching.bookgua_details()
                # result[0] is the code string (e.g. "776789")
                
                code = result[0]
                moving_lines = []
                for i, char in enumerate(code):
                    if char in ['6', '9']:
                        moving_lines.append(i + 1)
                
                if moving_lines:
                    texts = []
                    for line_idx in moving_lines:
                        text = en_data.get("lines", {}).get(str(line_idx), "")
                        if text:
                            texts.append(text)
                    response["main_text_en"] = "\n".join(texts) if texts else "(English line text unavailable)"
                else:
                    # No moving lines, usually use Judgement or Tuan?
                    # Or maybe use Thuan text (Judgement) as main text?
                    # In Chinese tradition, if no moving lines, use Ben Gua Tuan.
                    # which is already in ben_gua_text_en.
                    # So main_text_en can be empty or same as Judgement.
                    response["main_text_en"] = en_data.get("judgement", "")
            else:
                response["main_text_en"] = "(Classical text translation unavailable)"
                
            # Populate French Text
            fr_data = YI_JING_FR.get(str(hex_idx))
            if fr_data:
                response["ben_gua_fr"] = fr_data.get("name", ben_gua_name)
                response["ben_gua_text_fr"] = fr_data.get("judgement", "")
                
                # Moving lines FR
                code = result[0]
                moving_lines = []
                for i, char in enumerate(code):
                    if char in ['6', '9']:
                        moving_lines.append(i + 1)
                        
                if moving_lines:
                    texts = []
                    for line_idx in moving_lines:
                        text = fr_data.get("lines", {}).get(str(line_idx), "")
                        if text:
                            texts.append(text)
                    response["main_text_fr"] = "\n".join(texts) if texts else "(Texte français indisponible)"
                else:
                    response["main_text_fr"] = fr_data.get("judgement", "")
            else:
                response["ben_gua_fr"] = ben_gua_name
                response["main_text_fr"] = "(Traduction française indisponible)"
                
            # Summary FR
            if match:
                hex1_fr = response.get("ben_gua_fr", match.group(2))
                hex2_fr = match.group(3) # TODO: map zhi gua name to FR
                
                # Need to find hex2 index from Chinese Name
                zhi_name_cn = match.group(3)
                zhi_idx_cn = NAME_TO_INDEX.get(zhi_name_cn)
                if zhi_idx_cn and str(zhi_idx_cn) in YI_JING_FR:
                    hex2_fr = YI_JING_FR[str(zhi_idx_cn)]["name"]
                
                response["summary_fr"] = f"Traits mobiles: {count}. {hex1_fr} -> {hex2_fr}"
            else:
                summary_fr = response["summary"]
                summary_fr = summary_fr.replace("吉", "Fauste (Bon)").replace("凶", "Néfaste (Mauvais)")
                response["summary_fr"] = summary_fr
                
        else:
            response["main_text_en"] = "(Classical text translation unavailable)"
            response["main_text_fr"] = "(Traduction française indisponible)"
    
    return response

def get_current_time_divination():
    import datetime
    now = datetime.datetime.now()
    iching = ichingshifa.Iching()
    
    try:
        # Tuple return: (Name, BenGua, MovingYao, Text)
        result = iching.datetime_bookgua(int(now.year), int(now.month), int(now.day), int(now.hour), int(now.minute))
        
        response = {
            "gua_name": result[0],
            "ben_gua": result[1],
            "moving_yao_info": result[2],
            "main_text": result[3],
            "type": "datetime"
        }
        
        # Add EN
        response["gua_name_en"] = get_hex_en(result[0])
        # Need to parse moving_yao_info for EN?
        
        # Add FR
        gua_name = result[0]
        hex_idx = NAME_TO_INDEX.get(gua_name)
        if hex_idx and str(hex_idx) in YI_JING_FR:
            fr_data = YI_JING_FR[str(hex_idx)]
            response["gua_name_fr"] = fr_data["name"]
            
            # Parse moving yao
            yao_info = result[2] # e.g. "初九" or "六二"
            line_idx = None
            if "初" in yao_info: line_idx = 1
            elif "二" in yao_info: line_idx = 2
            elif "三" in yao_info: line_idx = 3
            elif "四" in yao_info: line_idx = 4
            elif "五" in yao_info: line_idx = 5
            elif "上" in yao_info: line_idx = 6
            
            if line_idx:
                response["main_text_fr"] = fr_data.get("lines", {}).get(str(line_idx), "")
            else:
                response["main_text_fr"] = fr_data.get("judgement", "")
        else:
            response["main_text_fr"] = "(Texte français indisponible)"
        
        return response
    except Exception as e:
        return {"error": str(e)}
