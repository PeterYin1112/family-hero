import { STORAGE_KEY, INITIAL_DB, INITIAL_MATH_SETTINGS, BASE_VOCAB } from '../config/constants';

export const loadFromStorage = () => {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (!saved) {
      return {
        stats: { ...INITIAL_DB },
        vocabMap: {
          daughter: BASE_VOCAB,
          son: BASE_VOCAB,
          mom: BASE_VOCAB,
          challenger: BASE_VOCAB
        },
        mathSettings: INITIAL_MATH_SETTINGS
      };
    }
    
    const stats = { ...INITIAL_DB };
    if (saved.stats) {
      Object.keys(INITIAL_DB).forEach((key) => {
        if (saved.stats[key]) {
          stats[key] = { ...INITIAL_DB[key], ...saved.stats[key] };
        }
      });
    }
    
    return {
      stats,
      vocabMap: saved.vocabMap || {
        daughter: BASE_VOCAB,
        son: BASE_VOCAB,
        mom: BASE_VOCAB,
        challenger: BASE_VOCAB
      },
      mathSettings: saved.mathSettings || INITIAL_MATH_SETTINGS
    };
  } catch (error) {
    console.error("Load storage error:", error);
    return {
      stats: { ...INITIAL_DB },
      vocabMap: {
        daughter: BASE_VOCAB,
        son: BASE_VOCAB,
        mom: BASE_VOCAB,
        challenger: BASE_VOCAB
      },
      mathSettings: INITIAL_MATH_SETTINGS
    };
  }
};

export const saveToStorage = (stats, vocabMap, mathSettings) => {
  try {
    const data = { stats, vocabMap, mathSettings };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    return true;
  } catch (error) {
    console.error("Save storage error:", error);
    return false;
  }
};
