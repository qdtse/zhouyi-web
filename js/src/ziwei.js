const TIANGAN = "甲乙丙丁戊己庚辛壬癸";
const DIZHI = "子丑寅卯辰巳午未申酉戌亥";

export class ZiweiChart {
  constructor(year, month, day, hour) {
    this.year = year;
    this.month = month;
    this.day = day;
    this.hour = hour;
    
    this.lunarMonth = this.getLunarMonth();
    this.lunarDay = this.getLunarDay();
    this.hourIdx = Math.floor((hour + 1) / 2) % 12;
    this.yearGanIdx = this.getYearGanIdx();
    
    this.palaces = Array.from({ length: 12 }, () => ({}));
    this.mingIdx = 0;
    this.shenIdx = 0;
    this.wuxingJu = 0;
    this.wuxingJuName = "";
    
    this.run();
  }
  
  getLunarMonth() {
    const springFestival = {
      2024: [2, 10], 2025: [1, 29], 2026: [2, 17],
      2023: [1, 22], 2022: [2, 1], 2021: [2, 12],
    };
    const [springMonth, springDay] = springFestival[this.year] || [2, 10];
    const springDate = new Date(this.year, springMonth - 1, springDay);
    const targetDate = new Date(this.year, this.month - 1, this.day);
    let daysDiff = Math.floor((targetDate - springDate) / (1000 * 60 * 60 * 24));
    
    if (daysDiff < 0) daysDiff += 30;
    
    let lunarMonth = 1;
    let lunarDay = 1 + daysDiff;
    while (lunarDay > 30) {
      lunarDay -= 30;
      lunarMonth++;
    }
    
    this.lunarDay = lunarDay;
    return lunarMonth;
  }
  
  getLunarDay() {
    return this.lunarDay || 1;
  }
  
  getYearGanIdx() {
    const lunarYear = this.year;
    const offset = (lunarYear - 1984) % 60;
    return ((offset % 10) + 10) % 10;
  }
  
  run() {
    this.assignPalaceNames();
    this.assignPalaceStems();
    this.determineWuxingJu();
    this.placeMajorStars();
  }
  
  assignPalaceNames() {
    this.mingIdx = (2 + (this.lunarMonth - 1) - this.hourIdx + 12) % 12;
    this.shenIdx = (2 + (this.lunarMonth - 1) + this.hourIdx) % 12;
    
    const names = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", "迁移", "交友", "官禄", "田宅", "福德", "父母"];
    
    let curr = this.mingIdx;
    for (const name of names) {
      this.palaces[curr].name = name;
      curr = (curr - 1 + 12) % 12;
    }
    
    this.palaces[this.shenIdx].isShen = true;
  }
  
  assignPalaceStems() {
    const startStem = ((this.yearGanIdx % 5 + 1) * 2) % 10;
    
    for (let i = 0; i < 12; i++) {
      const offset = i - 2;
      this.palaces[i].ganIdx = (startStem + offset + 10) % 10;
    }
  }
  
  determineWuxingJu() {
    const mingGan = this.palaces[this.mingIdx].ganIdx;
    const mingZhi = this.mingIdx;
    
    const gVal = Math.floor(mingGan / 2);
    const zMap = { 0: 0, 1: 0, 6: 0, 7: 0, 2: 1, 3: 1, 8: 1, 9: 1, 4: 2, 5: 2, 10: 2, 11: 2 };
    const zVal = zMap[mingZhi];
    
    let sumVal = gVal + zVal;
    if (sumVal >= 5) sumVal -= 5;
    sumVal += 1;
    
    const juMap = { 1: 4, 2: 2, 3: 6, 4: 5, 5: 3 };
    const juNameMap = { 4: "金四局", 2: "水二局", 6: "火六局", 5: "土五局", 3: "木三局" };
    
    this.wuxingJu = juMap[sumVal];
    this.wuxingJuName = juNameMap[this.wuxingJu];
  }
  
  placeMajorStars() {
    const d = this.lunarDay;
    const j = this.wuxingJu;
    
    let ziweiPos = 0;
    
    if (j === 2) {
      ziweiPos = Math.floor((d + 1) / 2);
    } else if (j === 3) {
      const [q, r] = [Math.floor(d / 3), d % 3];
      if (r === 0) ziweiPos = q + 2;
      else if (r === 1) ziweiPos = q + 4;
      else ziweiPos = q + 1;
    } else if (j === 4) {
      const [q, r] = [Math.floor(d / 4), d % 4];
      if (r === 0) ziweiPos = q + 3;
      else if (r === 1) ziweiPos = q + 11;
      else if (r === 2) ziweiPos = q + 4;
      else ziweiPos = q + 1;
    } else if (j === 5) {
      const [q, r] = [Math.floor(d / 5), d % 5];
      if (r === 0) ziweiPos = q + 4;
      else if (r === 1) ziweiPos = q + 6;
      else if (r === 2) ziweiPos = q + 11;
      else if (r === 3) ziweiPos = q + 4;
      else ziweiPos = q + 1;
    } else if (j === 6) {
      const [q, r] = [Math.floor(d / 6), d % 6];
      if (r === 0) ziweiPos = q + 5;
      else if (r === 1) ziweiPos = q + 9;
      else if (r === 2) ziweiPos = q + 6;
      else if (r === 3) ziweiPos = q + 11;
      else if (r === 4) ziweiPos = q + 4;
      else ziweiPos = q + 1;
    }
    
    ziweiPos = ziweiPos % 12;
    this.ziweiStarIndex = ziweiPos;
    
    this.addStar(ziweiPos, "紫微", "major");
    this.addStar((ziweiPos - 1 + 12) % 12, "天机", "major");
    this.addStar((ziweiPos - 3 + 12) % 12, "太阳", "major");
    this.addStar((ziweiPos - 4 + 12) % 12, "武曲", "major");
    this.addStar((ziweiPos - 5 + 12) % 12, "天同", "major");
    this.addStar((ziweiPos - 8 + 12) % 12, "廉贞", "major");
    
    const tianfuPos = (4 - ziweiPos + 12) % 12;
    this.addStar(tianfuPos, "天府", "major");
    
    this.addStar((tianfuPos + 1) % 12, "太阴", "major");
    this.addStar((tianfuPos + 2) % 12, "贪狼", "major");
    this.addStar((tianfuPos + 3) % 12, "巨门", "major");
    this.addStar((tianfuPos + 4) % 12, "天相", "major");
    this.addStar((tianfuPos + 5) % 12, "天梁", "major");
    this.addStar((tianfuPos + 6) % 12, "七杀", "major");
    this.addStar((tianfuPos + 10) % 12, "破军", "major");
  }
  
  addStar(idx, name, type = "common") {
    if (!this.palaces[idx].stars) {
      this.palaces[idx].stars = [];
    }
    this.palaces[idx].stars.push({ name, type });
  }
  
  toJSON() {
    const palacesData = this.palaces.map((p, i) => ({
      index: i,
      zhi: DIZHI[i],
      gan: TIANGAN[p.ganIdx || 0],
      name: p.name || "",
      stars: p.stars || [],
      is_shen: p.isShen || false,
      is_ming: i === this.mingIdx
    }));
    
    return {
      wuxing_ju: this.wuxingJuName,
      ming_palace: this.palaces[this.mingIdx].name,
      shen_palace: this.palaces[this.shenIdx].name,
      palaces: palacesData
    };
  }
}
