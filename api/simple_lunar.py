"""
简化的农历/八字计算模块
只包含 Cloudflare Workers 部署所需的最小功能
"""

# 天干
TIANGAN = "甲乙丙丁戊己庚辛壬癸"
# 地支
DIZHI = "子丑寅卯辰巳午未申酉戌亥"
# 生肖
SHENGXIAO = "鼠牛虎兔龙蛇马羊猴鸡狗猪"

# 天干五行
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 简化农历数据（1900-2100年的春节日期）
# 格式：{年份: (春节月, 春节日)}
SPRING_FESTIVAL = {
    2024: (2, 10), 2025: (1, 29), 2026: (2, 17),
    2023: (1, 22), 2022: (2, 1), 2021: (2, 12),
    2020: (1, 25), 2019: (2, 5), 2018: (2, 16),
    2017: (1, 28), 2016: (2, 8), 2015: (2, 19),
    # 可以根据需要添加更多年份
}

def get_spring_festival(year):
    """获取指定年份的春节日期"""
    if year in SPRING_FESTIVAL:
        return SPRING_FESTIVAL[year]
    # 简化处理：使用近似值
    # 春节通常在1月21日至2月20日之间
    return (2, 10)  # 默认2月10日

def solar_to_lunar(year, month, day):
    """
    简化的公历转农历
    返回 (农历年, 农历月, 农历日, 是否闰月)
    """
    spring_month, spring_day = get_spring_festival(year)
    
    # 计算从春节开始的天数差
    from datetime import datetime
    spring_date = datetime(year, spring_month, spring_day)
    target_date = datetime(year, month, day)
    
    days_diff = (target_date - spring_date).days
    
    # 简化处理：假设农历每月30天（实际有大小月之分）
    if days_diff < 0:
        # 在春节之前，属于上一年农历
        lunar_year = year - 1
        # 简化：假设上一年腊月有30天
        days_diff += 30
    else:
        lunar_year = year
    
    # 计算农历月日
    lunar_month = 1
    lunar_day = 1 + days_diff
    
    # 简化：每月30天
    while lunar_day > 30:
        lunar_day -= 30
        lunar_month += 1
    
    is_leap = False  # 简化：不考虑闰月
    
    return (lunar_year, lunar_month, lunar_day, is_leap)

def get_year_ganzhi(year):
    """获取年干支"""
    # 1984年是甲子年
    offset = (year - 1984) % 60
    gan_idx = offset % 10
    zhi_idx = offset % 12
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]

def get_month_ganzhi(year_gan, lunar_month):
    """
    获取月干支
    年干决定正月起始
    甲己之年丙作首，乙庚之岁戊为头
    丙辛之岁寻庚起，丁壬壬位顺行流
    戊癸之年何方发，甲寅之上好追求
    """
    year_gan_idx = TIANGAN.index(year_gan[0])
    
    # 确定正月天干
    if year_gan_idx in [0, 5]:  # 甲己
        start_gan = 2  # 丙
    elif year_gan_idx in [1, 6]:  # 乙庚
        start_gan = 4  # 戊
    elif year_gan_idx in [2, 7]:  # 丙辛
        start_gan = 6  # 庚
    elif year_gan_idx in [3, 8]:  # 丁壬
        start_gan = 8  # 壬
    else:  # 戊癸
        start_gan = 0  # 甲
    
    # 正月从寅开始
    gan_idx = (start_gan + lunar_month - 1) % 10
    zhi_idx = (2 + lunar_month - 1) % 12  # 寅是索引2
    
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]

def get_day_ganzhi(year, month, day):
    """
    获取日干支
    使用简化算法
    """
    from datetime import datetime
    # 以1900年1月31日为基准（甲子日）
    base_date = datetime(1900, 1, 31)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    offset = days_diff % 60
    gan_idx = offset % 10
    zhi_idx = offset % 12
    
    return TIANGAN[gan_idx] + DIZHI[zhi_idx]

def get_time_ganzhi(day_gan, hour):
    """
    获取时干支
    日干决定时辰起始
    甲己还加甲，乙庚丙作初
    丙辛从戊起，丁壬庚子居
    戊癸何方发，壬子是真途
    """
    day_gan_idx = TIANGAN.index(day_gan[0])
    
    # 确定子时的天干
    if day_gan_idx in [0, 5]:  # 甲己
        start_gan = 0  # 甲
    elif day_gan_idx in [1, 6]:  # 乙庚
        start_gan = 2  # 丙
    elif day_gan_idx in [2, 7]:  # 丙辛
        start_gan = 4  # 戊
    elif day_gan_idx in [3, 8]:  # 丁壬
        start_gan = 6  # 庚
    else:  # 戊癸
        start_gan = 8  # 壬
    
    # 计算时辰索引 (23-1点子时，1-3点丑时...)
    hour_idx = (hour + 1) // 2 % 12
    
    gan_idx = (start_gan + hour_idx) % 10
    
    return TIANGAN[gan_idx] + DIZHI[hour_idx]

class SimpleBazi:
    """简化版八字计算"""
    
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        
        # 计算农历
        self.lunar_year, self.lunar_month, self.lunar_day, _ = solar_to_lunar(year, month, day)
        
        # 计算八字
        self.year_gz = get_year_ganzhi(self.lunar_year)
        self.month_gz = get_month_ganzhi(self.year_gz[0], self.lunar_month)
        self.day_gz = get_day_ganzhi(year, month, day)
        self.time_gz = get_time_ganzhi(self.day_gz[0], hour)
    
    def getYearGan(self):
        return self.year_gz[0]
    
    def getYearZhi(self):
        return self.year_gz[1]
    
    def getMonthGan(self):
        return self.month_gz[0]
    
    def getMonthZhi(self):
        return self.month_gz[1]
    
    def getDayGan(self):
        return self.day_gz[0]
    
    def getDayZhi(self):
        return self.day_gz[1]
    
    def getTimeGan(self):
        return self.time_gz[0]
    
    def getTimeZhi(self):
        return self.time_gz[1]
    
    def getYearWuXing(self):
        return TIANGAN_WUXING[self.getYearGan()] + DIZHI_WUXING[self.getYearZhi()]
    
    def getMonthWuXing(self):
        return TIANGAN_WUXING[self.getMonthGan()] + DIZHI_WUXING[self.getMonthZhi()]
    
    def getDayWuXing(self):
        return TIANGAN_WUXING[self.getDayGan()] + DIZHI_WUXING[self.getDayZhi()]
    
    def getTimeWuXing(self):
        return TIANGAN_WUXING[self.getTimeGan()] + DIZHI_WUXING[self.getTimeZhi()]
    
    def __str__(self):
        return f"{self.year_gz} {self.month_gz} {self.day_gz} {self.time_gz}"

# 兼容层：模拟 lunar_python 的 Solar 类
class Solar:
    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
    
    @classmethod
    def fromYmdHms(cls, year, month, day, hour, minute, second):
        return cls(year, month, day, hour, minute, second)
    
    def getLunar(self):
        return SimpleLunar(self.year, self.month, self.day, self.hour)
    
    def toYmdHms(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d}"

class SimpleLunar:
    """简化版农历类"""
    
    def __init__(self, year, month, day, hour=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self._bazi = None
    
    def getEightChar(self):
        if self._bazi is None:
            self._bazi = SimpleBazi(self.year, self.month, self.day, self.hour)
        return self._bazi
    
    def getMonth(self):
        lunar_year, lunar_month, lunar_day, _ = solar_to_lunar(self.year, self.month, self.day)
        return lunar_month
    
    def getDay(self):
        lunar_year, lunar_month, lunar_day, _ = solar_to_lunar(self.year, self.month, self.day)
        return lunar_day
    
    def getYearGanIndex(self):
        bazi = self.getEightChar()
        return TIANGAN.index(bazi.getYearGan())
    
    def toString(self):
        lunar_year, lunar_month, lunar_day, _ = solar_to_lunar(self.year, self.month, self.day)
        return f"{lunar_year}年{lunar_month}月{lunar_day}日"
    
    def toFullString(self):
        return self.toString()

# 导出兼容接口
Lunar = SimpleLunar
