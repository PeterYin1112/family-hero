export const CHARACTERS = {
  daughter: {
    id: 'daughter',
    name: '冰雪女王榕',
    avatar: '👸',
    theme: 'princess',
    color: 'text-cyan-300',
    bg: 'bg-ice',
    attackType: 'ice',
    needPwd: true
  },
  son: {
    id: 'son',
    name: '甲蟲王者希',
    avatar: '👦',
    theme: 'hero',
    color: 'text-green-400',
    bg: 'bg-beetle-forest',
    attackType: 'beetle',
    needPwd: true
  },
  mom: {
    id: 'mom',
    name: '神力女超人',
    avatar: '👩',
    theme: 'princess',
    color: 'text-yellow-400',
    bg: 'bg-desert',
    attackType: 'magic',
    needPwd: true
  },
  challenger: {
    id: 'challenger',
    name: '挑戰者',
    subName: '(免密碼)',
    avatar: '🦸',
    theme: 'hero',
    color: 'text-blue-400',
    bg: 'bg-volcano',
    attackType: 'slash',
    needPwd: false
  }
};

export const BASE_VOCAB = [
  { word: "cat", type: "noun", mean: "貓" },
  { word: "dog", type: "noun", mean: "狗" },
  { word: "apple", type: "noun", mean: "蘋果" },
  { word: "book", type: "noun", mean: "書" }
];

export const SENTENCE_TEMPLATES = {
  noun: [{ text: "This is a ___.", hint: "這是一個..." }]
};

export const ITEMS_DB = {
  princess: {
    math: [{ id: 'pm1', icon: '🪄', type: 'weapon' }],
    english: [{ id: 'pe1', icon: '🌟', type: 'weapon' }]
  },
  hero: {
    math: [{ id: 'hm1', icon: '⚔️', type: 'weapon' }],
    english: [{ id: 'he1', icon: '🗡️', type: 'weapon' }]
  }
};

export const MONSTERS = ["👾", "👽", "🦖", "🦕", "🐙", "🐉"];

export const PARENT_PASSWORD = "28825252";
export const FAMILY_PASSWORD = "168";

export const STORAGE_KEY = 'fh_v24_emoji';

export const getInitialStat = () => ({
  dailyMathLevel: 0,
  dailyEnglishLevel: 0,
  dailyScore: 0,
  earnedItems: [],
  monsterBook: [],
  weeklyHistory: []
});

export const INITIAL_DB = {
  daughter: getInitialStat(),
  son: getInitialStat(),
  mom: getInitialStat(),
  challenger: getInitialStat()
};

export const INITIAL_MATH_SETTINGS = {
  daughter: { slots: [{ range: 10, weight: 1 }] },
  son: { weights: { '2-digit-add-sub': 1 } },
  challenger: { weights: { '2-digit-add-sub': 1 } }
};
