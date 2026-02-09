import sys
from ichingshifa import ichingshifa
import json
import os
from strokes import strokes

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
    "风泽中孚": "Inner Truth", "雷山小过": "Preponderance of the Small", "水火既济": "After Completion", "火水未济": "Before Completion"
}

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

def calculate_hexagram_from_text(text):
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

    return calculate_hexagram_from_numbers(upper_sum, lower_sum, total_sum)

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

def calculate_hexagram_from_numbers(upper_val, lower_val, total_val=None):
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
    summary_en = summary_en.replace("吉", "Auspicious").replace("凶", "Ominous").replace("悔", "Regret").replace("吝", "Stingy/Small Trouble")
    response["summary_en"] = summary_en
    
    response["main_text_en"] = "(Classical text translation unavailable)"
    
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
        summary_en = summary_en.replace("吉", "Auspicious").replace("凶", "Ominous")
        response["summary_en"] = summary_en
        response["main_text_en"] = "(Classical text translation unavailable)"
    
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
        
        return response
    except Exception as e:
        return {"error": str(e)}
