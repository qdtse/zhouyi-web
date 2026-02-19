// 天干地支
const TIANGAN = "甲乙丙丁戊己庚辛壬癸";
const DIZHI = "子丑寅卯辰巳午未申酉戌亥";

// 天干五行
const TIANGAN_WUXING = {
  甲: "木", 乙: "木",
  丙: "火", 丁: "火",
  戊: "土", 己: "土",
  庚: "金", 辛: "金",
  壬: "水", 癸: "水"
};

// 地支五行
const DIZHI_WUXING = {
  子: "水", 丑: "土", 寅: "木", 卯: "木",
  辰: "土", 巳: "火", 午: "火", 未: "土",
  申: "金", 酉: "金", 戌: "土", 亥: "水"
};

// 五行生克
const WUXING_RELATIONS = {
  生成: { 木: "火", 火: "土", 土: "金", 金: "水", 水: "木" },
  克制: { 木: "土", 土: "水", 水: "火", 火: "金", 金: "木" }
};

// 天干合化
const TIANGAN_HE = {
  甲: "己", 己: "甲",
  乙: "庚", 庚: "乙",
  丙: "辛", 辛: "丙",
  丁: "壬", 壬: "丁",
  戊: "癸", 癸: "戊"
};

// 地支六合
const DIZHI_LIUHE = {
  子: "丑", 丑: "子",
  寅: "亥", 亥: "寅",
  卯: "戌", 戌: "卯",
  辰: "酉", 酉: "辰",
  巳: "申", 申: "巳",
  午: "未", 未: "午"
};

// 地支相冲
const DIZHI_CHONG = {
  子: "午", 午: "子",
  丑: "未", 未: "丑",
  寅: "申", 申: "寅",
  卯: "酉", 酉: "卯",
  辰: "戌", 戌: "辰",
  巳: "亥", 亥: "巳"
};

// 地支相害
const DIZHI_HAI = {
  子: "未", 未: "子",
  丑: "午", 午: "丑",
  寅: "巳", 巳: "寅",
  卯: "辰", 辰: "卯",
  申: "亥", 亥: "申",
  酉: "戌", 戌: "酉"
};

// 春节数据
const SPRING_FESTIVAL = {
  2024: [2, 10], 2025: [1, 29], 2026: [2, 17],
  2023: [1, 22], 2022: [2, 1], 2021: [2, 12],
  2020: [1, 25], 2019: [2, 5], 2018: [2, 16],
  2017: [1, 28], 2016: [2, 8], 2015: [2, 19],
};

function getSpringFestival(year) {
  return SPRING_FESTIVAL[year] || [2, 10];
}

function solarToLunar(year, month, day) {
  const [springMonth, springDay] = getSpringFestival(year);
  const springDate = new Date(year, springMonth - 1, springDay);
  const targetDate = new Date(year, month - 1, day);
  
  let daysDiff = Math.floor((targetDate - springDate) / (1000 * 60 * 60 * 24));
  
  let lunarYear;
  if (daysDiff < 0) {
    lunarYear = year - 1;
    daysDiff += 30;
  } else {
    lunarYear = year;
  }
  
  let lunarMonth = 1;
  let lunarDay = 1 + daysDiff;
  
  while (lunarDay > 30) {
    lunarDay -= 30;
    lunarMonth++;
  }
  
  return { year: lunarYear, month: lunarMonth, day: lunarDay };
}

function getYearGanZhi(year) {
  const offset = (year - 1984) % 60;
  const ganIdx = ((offset % 10) + 10) % 10;
  const zhiIdx = ((offset % 12) + 12) % 12;
  return TIANGAN[ganIdx] + DIZHI[zhiIdx];
}

function getMonthGanZhi(yearGan, lunarMonth) {
  const yearGanIdx = TIANGAN.indexOf(yearGan[0]);
  
  let startGan;
  if ([0, 5].includes(yearGanIdx)) startGan = 2;
  else if ([1, 6].includes(yearGanIdx)) startGan = 4;
  else if ([2, 7].includes(yearGanIdx)) startGan = 6;
  else if ([3, 8].includes(yearGanIdx)) startGan = 8;
  else startGan = 0;
  
  const ganIdx = (startGan + lunarMonth - 1) % 10;
  const zhiIdx = (2 + lunarMonth - 1) % 12;
  
  return TIANGAN[ganIdx] + DIZHI[zhiIdx];
}

function getDayGanZhi(year, month, day) {
  const baseDate = new Date(1900, 0, 31);
  const targetDate = new Date(year, month - 1, day);
  const daysDiff = Math.floor((targetDate - baseDate) / (1000 * 60 * 60 * 24));
  
  const offset = ((daysDiff % 60) + 60) % 60;
  const ganIdx = offset % 10;
  const zhiIdx = offset % 12;
  
  return TIANGAN[ganIdx] + DIZHI[zhiIdx];
}

function getTimeGanZhi(dayGan, hour) {
  const dayGanIdx = TIANGAN.indexOf(dayGan[0]);
  
  let startGan;
  if ([0, 5].includes(dayGanIdx)) startGan = 0;
  else if ([1, 6].includes(dayGanIdx)) startGan = 2;
  else if ([2, 7].includes(dayGanIdx)) startGan = 4;
  else if ([3, 8].includes(dayGanIdx)) startGan = 6;
  else startGan = 8;
  
  const hourIdx = Math.floor((hour + 1) / 2) % 12;
  const ganIdx = (startGan + hourIdx) % 10;
  
  return TIANGAN[ganIdx] + DIZHI[hourIdx];
}

export function getBaziAnalysis(year, month, day, hour) {
  const lunar = solarToLunar(year, month, day);
  
  const yearGz = getYearGanZhi(lunar.year);
  const monthGz = getMonthGanZhi(yearGz[0], lunar.month);
  const dayGz = getDayGanZhi(year, month, day);
  const timeGz = getTimeGanZhi(dayGz[0], hour);
  
  const yearWx = TIANGAN_WUXING[yearGz[0]] + DIZHI_WUXING[yearGz[1]];
  const monthWx = TIANGAN_WUXING[monthGz[0]] + DIZHI_WUXING[monthGz[1]];
  const dayWx = TIANGAN_WUXING[dayGz[0]] + DIZHI_WUXING[dayGz[1]];
  const timeWx = TIANGAN_WUXING[timeGz[0]] + DIZHI_WUXING[timeGz[1]];
  
  const wuxingCounts = {};
  [yearWx, monthWx, dayWx, timeWx].forEach(wx => {
    wuxingCounts[wx[0]] = (wuxingCounts[wx[0]] || 0) + 1;
    wuxingCounts[wx[1]] = (wuxingCounts[wx[1]] || 0) + 1;
  });
  
  const missingWuxing = ["金", "木", "水", "火", "土"].filter(wx => !wuxingCounts[wx]);
  
  const dayGanWx = dayWx[0];
  const monthZhiWx = monthWx[1];
  
  let isStrong = false;
  let relationWithMonth = "平";
  
  if (dayGanWx === monthZhiWx) {
    relationWithMonth = "同气";
    isStrong = true;
  } else if (WUXING_RELATIONS.生成[monthZhiWx] === dayGanWx) {
    relationWithMonth = "得令";
    isStrong = true;
  } else {
    relationWithMonth = "不得令";
  }
  
  return {
    solar: `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')} ${String(hour).padStart(2, '0')}:00:00`,
    lunar: `${lunar.year}年${lunar.month}月${lunar.day}日`,
    bazi: [yearGz, monthGz, dayGz, timeGz],
    wuxing_counts: wuxingCounts,
    missing_wuxing: missingWuxing,
    day_master: {
      gan: dayGz[0],
      wuxing: dayGanWx,
      strength: isStrong ? "偏强" : "偏弱",
      month_relation: relationWithMonth
    },
    spouse_palace: dayGz[1]
  };
}

export function checkMarriageCompatibility(maleData, femaleData) {
  let score = 0;
  const analysis = [];
  
  const maleYearZhi = maleData.bazi[0][1];
  const femaleYearZhi = femaleData.bazi[0][1];
  
  if (DIZHI_LIUHE[maleYearZhi] === femaleYearZhi) {
    score += 20;
    analysis.push("【年支相合】 生肖六合，大吉。基础稳固，缘分深厚。");
  } else if (DIZHI_CHONG[maleYearZhi] === femaleYearZhi) {
    score -= 10;
    analysis.push("【年支相冲】 生肖相冲，基础不稳，易有冲突。建议多沟通包容。");
  } else if (DIZHI_HAI[maleYearZhi] === femaleYearZhi) {
    score -= 5;
    analysis.push("【年支相害】 生肖相害，易生嫌隙。");
  } else {
    score += 10;
    analysis.push("【年支无冲】 生肖配合一般，无严重冲突。");
  }
  
  const maleDayGan = maleData.day_master.gan;
  const femaleDayGan = femaleData.day_master.gan;
  const maleWx = TIANGAN_WUXING[maleDayGan];
  const femaleWx = TIANGAN_WUXING[femaleDayGan];
  
  if (TIANGAN_HE[maleDayGan] === femaleDayGan) {
    score += 30;
    analysis.push("【日干相合】 夫妻心意相通，性格互补，非常理想的组合。");
  } else if (maleWx && femaleWx && 
             (WUXING_RELATIONS.克制[maleWx] === femaleWx || WUXING_RELATIONS.克制[femaleWx] === maleWx)) {
    score -= 5;
    analysis.push("【日干相克】 性格上可能存在差异，需要磨合。");
  } else {
    score += 10;
    analysis.push("【日干平和】 彼此关系平等，相敬如宾。");
  }
  
  const maleDayZhi = maleData.spouse_palace;
  const femaleDayZhi = femaleData.spouse_palace;
  
  if (DIZHI_LIUHE[maleDayZhi] === femaleDayZhi) {
    score += 20;
    analysis.push("【日支相合】 夫妻宫六合，婚后生活和谐，恩爱有加。");
  } else if (DIZHI_CHONG[maleDayZhi] === femaleDayZhi) {
    score -= 15;
    analysis.push("【日支相冲】 夫妻宫相冲，婚后易有动荡或争吵，需注意经营。");
  } else if (DIZHI_HAI[maleDayZhi] === femaleDayZhi) {
    score -= 10;
    analysis.push("【日支相害】 夫妻宫相害，易有不和。");
  } else {
    score += 10;
    analysis.push("【日支无冲】 夫妻宫稳定。");
  }
  
  const maleMissing = new Set(maleData.missing_wuxing);
  const femaleMissing = new Set(femaleData.missing_wuxing);
  
  let complementary = false;
  
  for (const m of maleMissing) {
    if ((femaleData.wuxing_counts[m] || 0) >= 3) {
      complementary = true;
      analysis.push(`【五行互补】 男方缺${m}，女方${m}旺，女方能助旺男方。`);
    }
  }
  
  for (const m of femaleMissing) {
    if ((maleData.wuxing_counts[m] || 0) >= 3) {
      complementary = true;
      analysis.push(`【五行互补】 女方缺${m}，男方${m}旺，男方能助旺女方。`);
    }
  }
  
  if (complementary) {
    score += 20;
  } else if (maleMissing.size === 0 && femaleMissing.size === 0) {
    score += 10;
    analysis.push("【五行均衡】 双方五行俱全，自带平衡。");
  } else {
    score += 5;
    analysis.push("【五行普通】 五行互补性一般。");
  }
  
  score = Math.max(0, Math.min(100, score));
  
  let level = "中等";
  if (score >= 85) level = "上上等婚";
  else if (score >= 75) level = "上等婚";
  else if (score >= 60) level = "中等婚";
  else level = "下等婚 (需谨慎)";
  
  return {
    score,
    level,
    analysis,
    male_info: {
      bazi: maleData.bazzi.join(" "),
      day_master: maleData.day_master.gan
    },
    female_info: {
      bazi: femaleData.bazzi.join(" "),
      day_master: femaleData.day_master.gan
    }
  };
}
