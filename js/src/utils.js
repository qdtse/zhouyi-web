// 六十四卦名
const HEXAGRAM_NAMES = [
  "坤", "乾", "屯", "蒙", "需", "讼", "师", "比",
  "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
  "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
  "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
  "遯", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
  "损", "益", "夬", "姤", "萃", "升", "困", "井",
  "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
  "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"
];

const HEX_EN = {
  "乾": "The Creative", "坤": "The Receptive", "屯": "Difficulty at the Beginning",
  "蒙": "Youthful Folly", "需": "Waiting", "讼": "Conflict", "师": "The Army",
  "比": "Holding Together", "小畜": "The Taming Power of the Small", "履": "Treading",
  "泰": "Peace", "否": "Standstill", "同人": "Fellowship with Men",
  "大有": "Possession in Great Measure", "谦": "Modesty", "豫": "Enthusiasm",
  "随": "Following", "蛊": "Work on What Has Been Spoiled", "临": "Approach",
  "观": "Contemplation", "噬嗑": "Biting Through", "贲": "Grace",
  "剥": "Splitting Apart", "复": "Return", "无妄": "Innocence",
  "大畜": "The Taming Power of the Great", "颐": "The Corners of the Mouth",
  "大过": "Preponderance of the Great", "坎": "The Abysmal", "离": "The Clinging",
  "咸": "Influence", "恒": "Duration", "遯": "Retreat", "大壮": "The Power of the Great",
  "晋": "Progress", "明夷": "Darkening of the Light", "家人": "The Family",
  "睽": "Opposition", "蹇": "Obstruction", "解": "Deliverance", "损": "Decrease",
  "益": "Increase", "夬": "Break-through", "姤": "Coming to Meet",
  "萃": "Gathering Together", "升": "Pushing Upward", "困": "Oppression",
  "井": "The Well", "革": "Revolution", "鼎": "The Cauldron", "震": "The Arousing",
  "艮": "Keeping Still", "渐": "Development", "归妹": "The Marrying Maiden",
  "丰": "Abundance", "旅": "The Wanderer", "巽": "The Gentle", "兑": "The Joyous",
  "涣": "Dispersion", "节": "Limitation", "中孚": "Inner Truth",
  "小过": "Preponderance of the Small", "既济": "After Completion",
  "未济": "Before Completion"
};

const NAME_TO_INDEX = {
  "乾": 1, "坤": 2, "屯": 3, "蒙": 4, "需": 5, "讼": 6, "师": 7, "比": 8,
  "小畜": 9, "履": 10, "泰": 11, "否": 12, "同人": 13, "大有": 14, "谦": 15, "豫": 16,
  "随": 17, "蛊": 18, "临": 19, "观": 20, "噬嗑": 21, "贲": 22, "剥": 23, "复": 24,
  "无妄": 25, "大畜": 26, "颐": 27, "大过": 28, "坎": 29, "离": 30, "咸": 31, "恒": 32,
  "遯": 33, "大壮": 34, "晋": 35, "明夷": 36, "家人": 37, "睽": 38, "蹇": 39, "解": 40,
  "损": 41, "益": 42, "夬": 43, "姤": 44, "萃": 45, "升": 46, "困": 47, "井": 48,
  "革": 49, "鼎": 50, "震": 51, "艮": 52, "渐": 53, "归妹": 54, "丰": 55, "旅": 56,
  "巽": 57, "兑": 58, "涣": 59, "节": 60, "中孚": 61, "小过": 62, "既济": 63, "未济": 64
};

const TRIGRAM_ELEMENTS = {
  1: "metal", 2: "metal", 3: "fire", 4: "wood", 5: "wood", 6: "water", 7: "earth", 8: "earth"
};

const ELEMENT_RELATIONS = {
  metal: { sheng: "water", ke: "wood" },
  wood: { sheng: "fire", ke: "earth" },
  water: { sheng: "wood", ke: "fire" },
  fire: { sheng: "earth", ke: "metal" },
  earth: { sheng: "metal", ke: "water" }
};

const GUA_MAP = {
  1: "777", 2: "778", 3: "787", 4: "788",
  5: "877", 6: "878", 7: "887", 8: "888"
};

function getStrokes(char) {
  if (/\d/.test(char)) return parseInt(char);
  if (/[a-zA-Z]/.test(char)) return char.toLowerCase().charCodeAt(0) - 96;
  
  const strokeMap = {
    '一': 1, '二': 2, '三': 3, '四': 5, '五': 4, '六': 4, '七': 2, '八': 2, '九': 2, '十': 2,
    '天': 4, '地': 6, '人': 2, '大': 3, '小': 3, '上': 3, '下': 3, '中': 4, '日': 4, '月': 4,
    '年': 6, '时': 7, '分': 4, '金': 8, '木': 4, '水': 4, '火': 4, '土': 3,
    '爱': 10, '情': 11, '财': 10, '富': 12, '健': 10, '康': 11, '事': 8, '业': 13,
    '家': 10, '庭': 9, '子': 3, '女': 3, '父': 4, '母': 5, '兄': 5, '弟': 7,
    '生': 5, '死': 6, '吉': 6, '凶': 4, '好': 6, '坏': 7, '成': 6, '败': 8,
    '进': 7, '退': 9, '来': 7, '去': 5, '开': 4, '关': 6, '起': 10, '落': 12
  };
  
  return strokeMap[char] || char.charCodeAt(0) % 20 + 1;
}

function getHexEn(name) {
  return HEX_EN[name] || name;
}

function calculateMeihuaInterpretation(upperVal, lowerVal, movingYao, focus) {
  if (focus === "general") return {};
  
  const upperRem = upperVal % 8 || 8;
  const lowerRem = lowerVal % 8 || 8;
  
  let tiIdx, yongIdx;
  if (movingYao <= 3) {
    tiIdx = upperRem;
    yongIdx = lowerRem;
  } else {
    tiIdx = lowerRem;
    yongIdx = upperRem;
  }
  
  const tiElement = TRIGRAM_ELEMENTS[tiIdx];
  const yongElement = TRIGRAM_ELEMENTS[yongIdx];
  
  let relation = "equal";
  if (tiElement === yongElement) {
    relation = "equal";
  } else if (ELEMENT_RELATIONS[yongElement].sheng === tiElement) {
    relation = "yong_sheng_ti";
  } else if (ELEMENT_RELATIONS[tiElement].sheng === yongElement) {
    relation = "ti_sheng_yong";
  } else if (ELEMENT_RELATIONS[yongElement].ke === tiElement) {
    relation = "yong_ke_ti";
  } else if (ELEMENT_RELATIONS[tiElement].ke === yongElement) {
    relation = "ti_ke_yong";
  }
  
  let advice = "";
  const focusAdvice = {
    love: {
      yong_sheng_ti: "Great Match. The other party loves you deeply. Success comes easily.",
      equal: "Harmonious relationship. Mutual understanding.",
      ti_sheng_yong: "You give more than you receive. Need patience.",
      ti_ke_yong: "You can control the situation, but need effort to win the heart.",
      yong_ke_ti: "Obstacles and pressure. The other party might be rejecting."
    },
    wealth: {
      yong_sheng_ti: "Great Fortune. Wealth comes to you naturally.",
      equal: "Good financial partnership. Stable income.",
      ti_sheng_yong: "Investment required. Money flows out before coming in.",
      ti_ke_yong: "Wealth through hard work. You can get it if you try.",
      yong_ke_ti: "Risk of loss. Bad for investment. Be conservative."
    },
    career: {
      yong_sheng_ti: "Promotion and help from nobles. Career rises.",
      equal: "Cooperation and support from colleagues.",
      ti_sheng_yong: "Working hard for the team. Exhaustion but contributing.",
      ti_ke_yong: "Overcoming challenges. Success through capability.",
      yong_ke_ti: "Pressure from superiors or environment. Difficulties ahead."
    }
  };
  
  advice = focusAdvice[focus]?.[relation] || "";
  
  return { focus, ti_element: tiElement, yong_element: yongElement, relation, advice };
}

export function calculateHexagramFromText(text, focus = "general") {
  if (!text) return null;
  
  const mid = Math.floor(text.length / 2);
  const upperText = text.length === 1 ? text : text.slice(0, mid);
  const lowerText = text.length === 1 ? text : text.slice(mid);
  
  const upperSum = [...upperText].reduce((sum, c) => sum + getStrokes(c), 0);
  const lowerSum = [...lowerText].reduce((sum, c) => sum + getStrokes(c), 0);
  const totalSum = upperSum + lowerSum;
  
  return calculateHexagramFromNumbers(upperSum, lowerSum, totalSum, focus);
}

export function calculateHexagramFromNumbers(upperVal, lowerVal, totalVal, focus = "general") {
  if (totalVal === undefined) totalVal = upperVal + lowerVal;
  
  const upperRem = upperVal % 8 || 8;
  const lowerRem = lowerVal % 8 || 8;
  const movingYao = totalVal % 6 || 6;
  
  const baseCode = GUA_MAP[lowerRem] + GUA_MAP[upperRem];
  const codeArr = baseCode.split('');
  
  const idx = movingYao - 1;
  const original = codeArr[idx];
  codeArr[idx] = original === '7' ? '9' : '6';
  
  const finalCode = codeArr.join('');
  
  const benGuaIdx = getHexagramIndex(GUA_MAP[lowerRem], GUA_MAP[upperRem]);
  const zhiGuaCode = finalCode.replace(/[69]/g, c => c === '9' ? '8' : '7');
  const zhiGuaIdx = getHexagramIndex(zhiGuaCode.slice(0, 3), zhiGuaCode.slice(3, 6));
  
  const benGuaName = HEXAGRAM_NAMES[benGuaIdx] || "未知卦";
  const zhiGuaName = HEXAGRAM_NAMES[zhiGuaIdx] || "未知卦";
  
  const response = {
    ben_gua: benGuaName,
    zhi_gua: zhiGuaName,
    moving_yao: movingYao,
    gua_code: finalCode,
    upper_val: upperVal,
    lower_val: lowerVal,
    total_val: totalVal,
    summary: `动爻第${movingYao}爻。${benGuaName}之${zhiGuaName}`,
    ben_gua_en: getHexEn(benGuaName),
    zhi_gua_en: getHexEn(zhiGuaName),
    summary_en: `Moving Line: ${movingYao}. ${getHexEn(benGuaName)} -> ${getHexEn(zhiGuaName)}`
  };
  
  if (focus !== "general") {
    Object.assign(response, calculateMeihuaInterpretation(upperVal, lowerVal, movingYao, focus));
  }
  
  return response;
}

function getHexagramIndex(lower, upper) {
  const trigramMap = { "777": 0, "778": 1, "787": 2, "788": 3, "877": 4, "878": 5, "887": 6, "888": 7 };
  const upperIdx = trigramMap[upper] ?? 0;
  const lowerIdx = trigramMap[lower] ?? 0;
  return lowerIdx * 8 + upperIdx;
}

export function getZhugeFromText(text) {
  if (!text) return { error: "请输入至少一个字" };
  
  const chars = [...text];
  while (chars.length < 3) chars.push(chars[chars.length - 1]);
  
  const [c1, c2, c3] = chars.slice(0, 3);
  const s1 = getStrokes(c1);
  const s2 = getStrokes(c2);
  const s3 = getStrokes(c3);
  
  const n1 = s1 % 10;
  const n2 = s2 % 10;
  const n3 = s3 % 10;
  
  const totalVal = n1 * 100 + n2 * 10 + n3;
  let signIdx = totalVal % 384;
  if (signIdx === 0) signIdx = 384;
  
  return {
    type: "zhuge",
    input: text.slice(0, 3),
    strokes: [s1, s2, s3],
    numbers: [n1, n2, n3],
    index: signIdx,
    poem: `第${signIdx}签：此签暗示运势变化，请查阅《诸葛神数》详解。`,
    explain: `签数：${signIdx}。建议参考原书解读。`
  };
}

export function getRandomDivination() {
  const upperVal = Math.floor(Math.random() * 64) + 1;
  const lowerVal = Math.floor(Math.random() * 64) + 1;
  const totalVal = Math.floor(Math.random() * 100) + 1;
  
  return calculateHexagramFromNumbers(upperVal, lowerVal, totalVal);
}

export function getCurrentTimeDivination() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  const hour = now.getHours();
  const minute = now.getMinutes();
  
  const upperVal = (year + month + day) % 64 + 1;
  const lowerVal = (hour + minute) % 64 + 1;
  const totalVal = (year + month + day + hour + minute) % 100 + 1;
  
  const result = calculateHexagramFromNumbers(upperVal, lowerVal, totalVal);
  result.type = "datetime";
  result.datetime = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')} ${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
  
  return result;
}
