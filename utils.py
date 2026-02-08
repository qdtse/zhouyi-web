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
       Standard: 3 chars. 
       If > 3, use first 3? Or sum?
       Let's use the standard "Report 3 characters" method.
       If user inputs more, take first 3. If less, pad with last char.
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
    
    # Formula:
    # 1. Hundreds digit from s1
    # 2. Tens digit from s2
    # 3. Ones digit from s3
    # Logic from search result:
    # "第一字作百数...凡字笔画...在十笔以外者。减十笔算...若恰在十笔或二十笔。俱照零笔计算。"
    # Mod 10 logic.
    
    n1 = s1 % 10
    n2 = s2 % 10
    n3 = s3 % 10
    
    # "所报之字笔画以三百八十四为度" -> Combine to number, then mod 384?
    # Actually usually it is: (n1*100 + n2*10 + n3) % 384
    # If 0, use 384.
    
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
        # Fallback if local json is incomplete (I only added 100 items for demo)
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
        "explain": result["explain"]
    }

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
    
    return response

def get_random_divination():
    iching = ichingshifa.Iching()
    result = iching.bookgua_details()
    
    # Result structure for random might be slightly different or same
    # Assuming same for simplicity based on previous manual tests
    
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
        return response
    except Exception as e:
        return {"error": str(e)}
