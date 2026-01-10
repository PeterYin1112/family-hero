import { useState, useRef, useEffect } from 'react';
import { BASE_VOCAB, MONSTERS, getInitialStat } from '../config/constants';
import { playSFX, speakWord } from '../utils/audio';
import { saveToStorage } from '../utils/storage';
import { firestoreService } from '../services/firebase';

export const useGameLogic = (playerKey, stats, vocabMap, mathSettings, userObj) => {
  const [gameMode, setGameMode] = useState('math');
  const [dailyLevel, setDailyLevel] = useState(1);
  const [timer, setTimer] = useState(0);
  const [question, setQuestion] = useState({ text: "Ready?", answer: "" });
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [inputMode, setInputMode] = useState('select');
  const [feverMode, setFeverMode] = useState(false);
  const [consecutiveCorrect, setConsecutiveCorrect] = useState(0);
  
  const timerRef = useRef(null);
  const statsRef = useRef(stats);

  useEffect(() => {
    statsRef.current = stats;
  }, [stats]);

  const generateMathQuestion = (level) => {
    const n1 = Math.floor(Math.random() * (level * 2)) + 1;
    const n2 = Math.floor(Math.random() * (level * 2)) + 1;
    const ops = ['+', '-', '*'];
    const op = ops[Math.floor(Math.random() * ops.length)];
    let answer;
    
    switch (op) {
      case '+':
        answer = (n1 + n2).toString();
        break;
      case '-':
        answer = (Math.max(n1, n2) - Math.min(n1, n2)).toString();
        break;
      case '*':
        answer = (n1 * n2).toString();
        break;
      default:
        answer = (n1 + n2).toString();
    }
    
    return {
      text: `${n1} ${op} ${n2} = ?`,
      answer,
      type: 'math'
    };
  };

  const generateEnglishQuestion = (level) => {
    const vocab = vocabMap[playerKey] || BASE_VOCAB;
    if (vocab.length === 0) {
      return { text: "No vocabulary available", answer: "", type: 'english' };
    }
    
    const word = vocab[Math.floor(Math.random() * vocab.length)];
    const options = [word.word];
    
    // 生成其他選項
    while (options.length < 4) {
      const otherWord = vocab[Math.floor(Math.random() * vocab.length)].word;
      if (!options.includes(otherWord)) {
        options.push(otherWord);
      }
    }
    
    // 打亂選項順序
    const shuffled = options.sort(() => Math.random() - 0.5);
    
    return {
      text: word.word,
      answer: word.word,
      options: shuffled,
      mean: word.mean,
      type: 'english'
    };
  };

  const startGame = (mode, currentStats) => {
    const pStat = currentStats[playerKey] || getInitialStat();
    const curLv = mode.includes('math') ? pStat.dailyMathLevel : pStat.dailyEnglishLevel;
    const otherLv = mode.includes('math') ? pStat.dailyEnglishLevel : pStat.dailyMathLevel;
    
    // 平衡機制：每 20 級檢查一次
    if (curLv > 0 && curLv % 20 === 0 && otherLv < curLv) {
      alert(`🚧 請先將另一科練到 Lv.${curLv}！`);
      return false;
    }
    
    setGameMode(mode);
    setDailyLevel(curLv + 1);
    setFeverMode(false);
    setConsecutiveCorrect(0);
    
    // 生成問題
    const q = mode.includes('math')
      ? generateMathQuestion(curLv + 1)
      : generateEnglishQuestion(curLv + 1);
    
    setQuestion(q);
    setTimer(30);
    setUserAnswer('');
    setFeedback(null);
    
    // 英文題目自動朗讀
    if (mode.includes('english') && q.text) {
      setTimeout(() => speakWord(q.text), 500);
    }
    
    // 啟動計時器
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setTimer((t) => {
        if (t > 0) return t - 1;
        handleTimeOut();
        return 0;
      });
    }, 1000);
    
    return true;
  };

  const handleTimeOut = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setFeedback('timeout');
    playSFX('hit');
  };

  const handleAnswer = (val, onCorrect, onWrong, onLevelComplete) => {
    if (timerRef.current) clearInterval(timerRef.current);
    
    const ans = val || userAnswer;
    const isCorrect = ans.toLowerCase().trim() === question.answer.toLowerCase().trim();
    
    if (isCorrect) {
      playSFX('win');
      setFeedback('correct');
      
      // 更新統計
      const newStats = JSON.parse(JSON.stringify(statsRef.current));
      const pStat = newStats[playerKey] || getInitialStat();
      
      if (gameMode.includes('math')) {
        newStats[playerKey].dailyMathLevel = dailyLevel;
      } else {
        newStats[playerKey].dailyEnglishLevel = dailyLevel;
      }
      
      // 計算分數（Fever Mode 加成）
      const baseScore = 100;
      const score = feverMode ? Math.floor(baseScore * 1.5) : baseScore;
      newStats[playerKey].dailyScore += score;
      
      // 記錄怪獸
      const monster = MONSTERS[dailyLevel % MONSTERS.length];
      if (!newStats[playerKey].monsterBook.includes(monster)) {
        newStats[playerKey].monsterBook.push(monster);
      }
      
      // Fever Mode 邏輯
      const newConsecutive = consecutiveCorrect + 1;
      setConsecutiveCorrect(newConsecutive);
      if (newConsecutive >= 3 && !feverMode) {
        setFeverMode(true);
      }
      
      // 保存到本地和雲端
      saveToStorage(newStats, vocabMap, mathSettings);
      if (userObj) {
        firestoreService.saveUserData(userObj.uid, {
          stats: newStats,
          vocabMap,
          mathSettings
        });
      }
      
      // 英文答對時複誦
      if (gameMode.includes('english')) {
        speakWord(question.answer);
      }
      
      if (onCorrect) onCorrect(newStats);
      
      // 每 10 關結算一次
      if (dailyLevel % 10 === 0) {
        setTimeout(() => {
          if (onLevelComplete) onLevelComplete();
        }, 1500);
      } else {
        // 繼續下一題
        setTimeout(() => {
          const nextLevel = dailyLevel + 1;
          setDailyLevel(nextLevel);
          const nextQ = gameMode.includes('math')
            ? generateMathQuestion(nextLevel)
            : generateEnglishQuestion(nextLevel);
          setQuestion(nextQ);
          setUserAnswer('');
          setFeedback(null);
          setTimer(30);
          
          if (gameMode.includes('english') && nextQ.text) {
            setTimeout(() => speakWord(nextQ.text), 500);
          }
          
          timerRef.current = setInterval(() => {
            setTimer((t) => {
              if (t > 0) return t - 1;
              handleTimeOut();
              return 0;
            });
          }, 1000);
        }, 1000);
      }
    } else {
      playSFX('hit');
      setFeedback('wrong');
      setConsecutiveCorrect(0);
      setFeverMode(false);
      
      if (onWrong) onWrong();
      
      // 答錯時不清除問題，讓玩家可以再試
      // 清除反饋並重新啟動計時器
      setTimeout(() => {
        setFeedback(null);
        setTimer(30);
        if (timerRef.current) clearInterval(timerRef.current);
        timerRef.current = setInterval(() => {
          setTimer((t) => {
            if (t > 0) return t - 1;
            handleTimeOut();
            return 0;
          });
        }, 1000);
      }, 1000);
    }
  };

  const stopGame = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setTimer(0);
    setFeedback(null);
  };

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  return {
    gameMode,
    dailyLevel,
    timer,
    question,
    userAnswer,
    setUserAnswer,
    feedback,
    inputMode,
    setInputMode,
    feverMode,
    consecutiveCorrect,
    startGame,
    handleAnswer,
    stopGame
  };
};
