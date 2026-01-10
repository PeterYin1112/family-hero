import { useState, useEffect } from 'react';
import { CHARACTERS, PARENT_PASSWORD, FAMILY_PASSWORD, BASE_VOCAB } from './config/constants';
import { loadFromStorage, saveToStorage } from './utils/storage';
import { initAudio, playSFX } from './utils/audio';
import { firebaseAuth, initFirebase } from './services/firebase';
import { firestoreService } from './services/firebase';
import { useGameLogic } from './hooks/useGameLogic';
import { Menu } from './components/Menu';
import { BattleScene } from './components/BattleScene';
import { Settings } from './components/Settings';
import { PasswordModal } from './components/PasswordModal';
import { ResultScreen } from './components/ResultScreen';

function App() {
  const [screen, setScreen] = useState('menu');
  const [playerKey, setPlayerKey] = useState('daughter');
  const [stats, setStats] = useState(() => loadFromStorage().stats);
  const [vocabMap, setVocabMap] = useState(() => loadFromStorage().vocabMap);
  const [mathSettings, setMathSettings] = useState(() => loadFromStorage().mathSettings);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [userObj, setUserObj] = useState(null);
  const [pwdTarget, setPwdTarget] = useState(null);
  const [pendingAction, setPendingAction] = useState(null);
  const [showAudioPrompt, setShowAudioPrompt] = useState(true);

  // 初始化 Firebase 認證監聽（失敗時自動切換到 LocalStorage 模式）
  useEffect(() => {
    try {
      if (initFirebase()) {
        const unsubscribe = firebaseAuth.onAuthStateChanged((user) => {
          setUserObj(user);
        });
        return () => {
          if (unsubscribe && typeof unsubscribe === 'function') {
            unsubscribe();
          }
        };
      }
    } catch (error) {
      console.warn('Firebase initialization failed, using LocalStorage mode:', error);
      // 繼續使用 LocalStorage 模式
    }
  }, []);

  // 遊戲邏輯 Hook
  const gameLogic = useGameLogic(
    playerKey,
    stats,
    vocabMap,
    mathSettings,
    userObj
  );

  const char = CHARACTERS[playerKey] || CHARACTERS.daughter;

  const handleToggleAudio = () => {
    initAudio();
    setAudioEnabled(true);
    setShowAudioPrompt(false);
    playSFX('start');
  };

  const handlePlayerChange = (newPlayerKey) => {
    setPlayerKey(newPlayerKey);
    playSFX('click');
  };

  const handleSaveAll = (newStats, newVocabMap, newMathSettings) => {
    const updatedStats = newStats || stats;
    const updatedVocabMap = newVocabMap || vocabMap;
    const updatedMathSettings = newMathSettings || mathSettings;

    setStats(updatedStats);
    setVocabMap(updatedVocabMap);
    setMathSettings(updatedMathSettings);

    // 保存到本地
    saveToStorage(updatedStats, updatedVocabMap, updatedMathSettings);

    // 保存到雲端
    if (userObj) {
      firestoreService.saveUserData(userObj.uid, {
        stats: updatedStats,
        vocabMap: updatedVocabMap,
        mathSettings: updatedMathSettings
      });
    }
  };

  const handleRequestStartGame = (mode) => {
    if (CHARACTERS[playerKey].needPwd) {
      setPendingAction({ type: 'startGame', args: [mode] });
      setPwdTarget('FAMILY');
    } else {
      doStartGame(mode);
    }
  };

  const handleRequestSettings = () => {
    setPendingAction({ type: 'settings', args: [] });
    setPwdTarget('PARENT');
  };

  const handlePwdSuccess = () => {
    setPwdTarget(null);
    if (pendingAction?.type === 'startGame') {
      doStartGame(...pendingAction.args);
    } else if (pendingAction?.type === 'settings') {
      setScreen('settings');
    }
    setPendingAction(null);
  };

  const doStartGame = (mode) => {
    if (!audioEnabled) {
      handleToggleAudio();
    }

    const success = gameLogic.startGame(mode, stats);
    if (success) {
      setScreen('game');
    }
  };

  const handleAnswer = (val) => {
    gameLogic.handleAnswer(
      val,
      (newStats) => {
        handleSaveAll(newStats);
      },
      () => {
        // 答錯處理已在 hook 中完成
      },
      () => {
        setScreen('result');
      }
    );
  };

  const handleLevelComplete = () => {
    setScreen('result');
  };

  const handleBackToMenu = () => {
    gameLogic.stopGame();
    setScreen('menu');
  };

  const handleSettingsSave = (newStats, newVocabMap, newMathSettings) => {
    handleSaveAll(newStats, newVocabMap, newMathSettings);
  };

  return (
    <div
      className={`w-full h-screen flex flex-col items-center justify-center relative ${char.bg} transition-colors duration-500`}
    >
        {/* 密碼輸入模態框 */}
        {pwdTarget && (
          <PasswordModal
            targetPassword={
              pwdTarget === 'FAMILY' ? FAMILY_PASSWORD : PARENT_PASSWORD
            }
            onSuccess={handlePwdSuccess}
            onClose={() => {
              setPwdTarget(null);
              setPendingAction(null);
            }}
          />
        )}

        {/* 音效啟動提示 */}
        {showAudioPrompt && screen === 'menu' && !audioEnabled && (
          <div
            className="absolute inset-0 z-50 bg-black/90 flex items-center justify-center cursor-pointer"
            onClick={handleToggleAudio}
          >
            <div className="text-center animate-pulse text-white">
              <div className="text-6xl mb-4">🔊</div>
              <h2 className="text-3xl font-bold">點擊啟動</h2>
            </div>
          </div>
        )}

        {/* 主選單 */}
        {screen === 'menu' && (
          <Menu
            playerKey={playerKey}
            onPlayerChange={handlePlayerChange}
            stats={stats}
            onStartGame={handleRequestStartGame}
            onSettings={handleRequestSettings}
            char={char}
          />
        )}

        {/* 戰鬥場景 */}
        {screen === 'game' && (
          <BattleScene
            playerKey={playerKey}
            stats={stats}
            question={gameLogic.question}
            timer={gameLogic.timer}
            feedback={gameLogic.feedback}
            inputMode={gameLogic.inputMode}
            setInputMode={gameLogic.setInputMode}
            userAnswer={gameLogic.userAnswer}
            setUserAnswer={gameLogic.setUserAnswer}
            feverMode={gameLogic.feverMode}
            consecutiveCorrect={gameLogic.consecutiveCorrect}
            dailyLevel={gameLogic.dailyLevel}
            gameMode={gameLogic.gameMode}
            onAnswer={handleAnswer}
          />
        )}

        {/* 設定頁面 */}
        {screen === 'settings' && (
          <Settings
            userObj={userObj}
            onUserChange={setUserObj}
            stats={stats}
            vocabMap={vocabMap}
            mathSettings={mathSettings}
            onBack={handleBackToMenu}
            onSave={handleSettingsSave}
          />
        )}

        {/* 結果畫面 */}
        {screen === 'result' && (
          <ResultScreen
            level={gameLogic.dailyLevel}
            onBack={handleBackToMenu}
          />
        )}
      </div>
  );
}

export default App;
