try:
    from lunar_python import Lunar, Solar
except ImportError:
    from simple_lunar import Lunar, Solar

class ZiweiChart:
    def __init__(self, year, month, day, hour):
        # hour is 0-23
        self.solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        self.lunar = self.solar.getLunar()
        self.bazi = self.lunar.getEightChar()
        
        # Basic info
        self.lunar_month = self.lunar.getMonth()
        self.lunar_day = self.lunar.getDay()
        
        # Determine Hour Index (Zi=0, Chou=1...)
        # 23-1 -> Zi(0). 1-3 -> Chou(1).
        self.hour_idx = (hour + 1) // 2 % 12
        
        self.year_gan_idx = self.lunar.getYearGanIndex() # 0=Jia
        
        self.palaces = [{} for _ in range(12)] # 0=Zi, 1=Chou...
        self.ming_idx = 0
        self.shen_idx = 0
        self.wuxing_ju = 0 # 2,3,4,5,6
        self.wuxing_ju_name = ""
        
        self.run()

    def run(self):
        self.assign_palace_names()
        self.assign_palace_stems()
        self.determine_wuxing_ju()
        self.place_major_stars()
        
    def assign_palace_names(self):
        # Ming Palace: From Yin(2), clockwise to month, counter-clockwise to hour
        # Formula: (2 + (Month-1) - Hour) % 12
        self.ming_idx = (2 + (self.lunar_month - 1) - self.hour_idx) % 12
        self.shen_idx = (2 + (self.lunar_month - 1) + self.hour_idx) % 12
        
        names = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", "迁移", "交友", "官禄", "田宅", "福德", "父母"]
        
        # Place names counter-clockwise from Ming
        curr = self.ming_idx
        for name in names:
            self.palaces[curr]["name"] = name
            curr = (curr - 1) % 12
            
        self.palaces[self.shen_idx]["is_shen"] = True
            
    def assign_palace_stems(self):
        # Wu Hu Dun: Year Gan -> Yin Palace Stem
        # Jia(0)/Ji(5) -> Bing(2) Yin
        # Yi(1)/Geng(6) -> Wu(4) Yin
        # Bing(2)/Xin(7) -> Geng(6) Yin
        # Ding(3)/Ren(8) -> Ren(8) Yin
        # Wu(4)/Gui(9) -> Jia(0) Yin
        
        start_stem = (self.year_gan_idx % 5 + 1) * 2 % 10
        
        # Yin is index 2
        for i in range(12):
            # Palace index 2 (Yin) gets start_stem
            # Palace index 3 (Mao) gets start_stem + 1
            # Palace i: offset from 2 is i-2
            offset = i - 2
            stem_idx = (start_stem + offset) % 10
            self.palaces[i]["gan_idx"] = stem_idx
            
    def determine_wuxing_ju(self):
        # Based on Ming Palace Gan and Zhi
        ming_gan = self.palaces[self.ming_idx]["gan_idx"]
        ming_zhi = self.ming_idx
        
        # Na Yin simple lookup
        # Gan: 0,1=0; 2,3=1; 4,5=2; 6,7=3; 8,9=4  (Div 2)
        # Zhi: 0,1,6,7=0; 2,3,8,9=1; 4,5,10,11=2
        
        g_val = ming_gan // 2
        z_map = {0:0, 1:0, 6:0, 7:0, 2:1, 3:1, 8:1, 9:1, 4:2, 5:2, 10:2, 11:2}
        z_val = z_map[ming_zhi]
        
        sum_val = g_val + z_val
        if sum_val >= 5: sum_val -= 5
        sum_val += 1 # 1 to 5
        
        # 1=Gold4, 2=Water2, 3=Fire6, 4=Earth5, 5=Wood3
        ju_map = {1: 4, 2: 2, 3: 6, 4: 5, 5: 3}
        ju_name_map = {4: "金四局", 2: "水二局", 6: "火六局", 5: "土五局", 3: "木三局"}
        
        self.wuxing_ju = ju_map[sum_val]
        self.wuxing_ju_name = ju_name_map[self.wuxing_ju]
        
    def place_major_stars(self):
        d = self.lunar_day
        j = self.wuxing_ju
        
        ziwei_pos = 0
        
        if j == 2: # Water 2
            ziwei_pos = (d + 1) // 2
        elif j == 3: # Wood 3
            q, r = divmod(d, 3)
            if r == 0: ziwei_pos = (q + 2)
            elif r == 1: ziwei_pos = (q + 4) 
            else: ziwei_pos = (q + 1) 
        elif j == 4: # Metal 4
            q, r = divmod(d, 4)
            if r == 0: ziwei_pos = (q + 3)
            elif r == 1: ziwei_pos = (q + 11)
            elif r == 2: ziwei_pos = (q + 4)
            else: ziwei_pos = (q + 1)
        elif j == 5: # Earth 5
            q, r = divmod(d, 5)
            if r == 0: ziwei_pos = (q + 4)
            elif r == 1: ziwei_pos = (q + 6)
            elif r == 2: ziwei_pos = (q + 11)
            elif r == 3: ziwei_pos = (q + 4)
            else: ziwei_pos = (q + 1)
        elif j == 6: # Fire 6
            q, r = divmod(d, 6)
            if r == 0: ziwei_pos = (q + 5)
            elif r == 1: ziwei_pos = (q + 9)
            elif r == 2: ziwei_pos = (q + 6)
            elif r == 3: ziwei_pos = (q + 11)
            elif r == 4: ziwei_pos = (q + 4)
            else: ziwei_pos = (q + 1)
            
        ziwei_pos = ziwei_pos % 12
        
        self.ziwei_star_index = ziwei_pos
        self.add_star(ziwei_pos, "紫微", "major")
        
        # Ziwei Series (Counter-clockwise)
        self.add_star((ziwei_pos - 1) % 12, "天机", "major")
        self.add_star((ziwei_pos - 3) % 12, "太阳", "major")
        self.add_star((ziwei_pos - 4) % 12, "武曲", "major")
        self.add_star((ziwei_pos - 5) % 12, "天同", "major")
        self.add_star((ziwei_pos - 8) % 12, "廉贞", "major")
        
        # Tianfu Location (4 - ziwei)
        tianfu_pos = (4 - ziwei_pos) % 12
        self.add_star(tianfu_pos, "天府", "major")
        
        # Tianfu Series (Clockwise)
        self.add_star((tianfu_pos + 1) % 12, "太阴", "major")
        self.add_star((tianfu_pos + 2) % 12, "贪狼", "major")
        self.add_star((tianfu_pos + 3) % 12, "巨门", "major")
        self.add_star((tianfu_pos + 4) % 12, "天相", "major")
        self.add_star((tianfu_pos + 5) % 12, "天梁", "major")
        self.add_star((tianfu_pos + 6) % 12, "七杀", "major")
        self.add_star((tianfu_pos + 10) % 12, "破军", "major")

    def add_star(self, idx, name, type="common"):
        if "stars" not in self.palaces[idx]:
            self.palaces[idx]["stars"] = []
        self.palaces[idx]["stars"].append({"name": name, "type": type})
        
    def json(self):
        zhi_names = "子丑寅卯辰巳午未申酉戌亥"
        gan_names = "甲乙丙丁戊己庚辛壬癸"
        
        palaces_data = []
        for i, p in enumerate(self.palaces):
            gan = gan_names[p.get("gan_idx", 0)]
            zhi = zhi_names[i]
            palaces_data.append({
                "index": i,
                "zhi": zhi,
                "gan": gan,
                "name": p.get("name", ""),
                "stars": p.get("stars", []),
                "is_shen": p.get("is_shen", False),
                "is_ming": (i == self.ming_idx)
            })
            
        return {
            "bazi": str(self.bazi),
            "lunar": self.lunar.toString(),
            "wuxing_ju": self.wuxing_ju_name,
            "ming_palace": self.palaces[self.ming_idx]["name"],
            "shen_palace": self.palaces[self.shen_idx]["name"],
            "palaces": palaces_data
        }
