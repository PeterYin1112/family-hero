import { useState, useEffect } from 'react';
import { FullBodyChar } from './Character';
import { CHARACTERS, MONSTERS } from '../config/constants';
import { speakWord } from '../utils/audio';

export const BattleScene = ({
  playerKey,
  stats,
  question,
  timer,
  feedback,
  inputMode,
  setInputMode,
  userAnswer,
  setUserAnswer,
  feverMode,
  consecutiveCorrect,
  dailyLevel,
  gameMode,
  onAnswer
}) => {
  const char = CHARACTERS[playerKey] || CHARACTERS.daughter;
  const monster = MONSTERS[dailyLevel % MONSTERS.length];
  const [shake, setShake] = useState(false);

  useEffect(() => {
    if (feedback === 'wrong') {
      setShake(true);
      setTimeout(() => setShake(false), 300);
    }
  }, [feedback]);

  const handleSelectAnswer = (option) => {
    onAnswer(option);
  };

  const handleSubmit = () => {
    if (userAnswer.trim()) {
      onAnswer();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="h-full w-full flex flex-col relative z-10 bg-slate-900/80">
      {/* 頂部資訊欄 */}
      <div className="p-4 flex justify-between items-center text-white bg-black/20">
        <div className="text-3xl">{char.avatar}</div>
        <div className="flex items-center gap-2">
          {feverMode && (
            <div className="text-red-500 font-bold animate-pulse">🔥 FEVER</div>
          )}
          {consecutiveCorrect > 0 && (
            <div className="text-yellow-400 text-sm">連擊: {consecutiveCorrect}</div>
          )}
        </div>
        <div className="text-4xl font-mono">{timer}</div>
        <div className="text-4xl">{monster}</div>
      </div>

      {/* 角色和怪獸區域 */}
      <div className="flex-1 flex items-center justify-center relative">
        <div className={`scale-150 transition-transform ${shake ? 'animate-shake' : ''}`}>
          <FullBodyChar charId={playerKey} items={stats[playerKey]?.earnedItems} />
        </div>
        {feedback === 'correct' && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-9xl animate-pop">✨</div>
          </div>
        )}
        {feedback === 'wrong' && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-9xl text-red-500 animate-shake">💥</div>
          </div>
        )}
      </div>

      {/* 題目和輸入區域 */}
      <div className="p-6 bg-slate-800 rounded-t-3xl text-center border-t-2 border-white/10">
        {/* 題目 */}
        <div className="mb-4">
          <h2 className="text-3xl font-black text-white mb-2">{question?.text}</h2>
          {question?.mean && (
            <p className="text-gray-400 text-sm">({question.mean})</p>
          )}
        </div>

        {/* 輸入模式選擇 */}
        {gameMode.includes('english') && (
          <div className="flex gap-2 mb-4 justify-center">
            <button
              onClick={() => setInputMode('select')}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                inputMode === 'select'
                  ? 'bg-yellow-400 text-black'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }`}
            >
              選擇題
            </button>
            <button
              onClick={() => setInputMode('text')}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                inputMode === 'text'
                  ? 'bg-yellow-400 text-black'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }`}
            >
              拼字題
            </button>
          </div>
        )}

        {/* 答案輸入 */}
        {inputMode === 'select' && question?.options ? (
          <div className="grid grid-cols-2 gap-4">
            {question.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectAnswer(option)}
                className="bg-white/10 hover:bg-white/20 p-4 rounded-xl font-bold active:scale-95 transition-colors"
              >
                {option}
              </button>
            ))}
          </div>
        ) : (
          <div className="flex gap-2">
            <input
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 bg-black/50 p-3 text-2xl text-white rounded-xl text-center border-2 border-transparent focus:border-yellow-400"
              placeholder="答案"
              type={gameMode.includes('math') ? 'tel' : 'text'}
              autoCapitalize="none"
              autoCorrect="off"
              autoComplete="off"
            />
            <button
              onClick={handleSubmit}
              className="bg-yellow-400 hover:bg-yellow-500 text-black px-6 py-3 rounded-xl font-bold active:scale-95 transition-colors"
            >
              GO
            </button>
          </div>
        )}

        {/* 回饋顯示 */}
        {feedback && (
          <div
            className={`mt-4 text-4xl font-bold animate-pop ${
              feedback === 'correct'
                ? 'text-green-500'
                : feedback === 'wrong'
                ? 'text-red-500'
                : 'text-yellow-500'
            }`}
          >
            {feedback === 'correct' && '⭕'}
            {feedback === 'wrong' && '❌'}
            {feedback === 'timeout' && '⏰'}
          </div>
        )}
      </div>
    </div>
  );
};
