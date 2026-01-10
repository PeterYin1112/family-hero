import { CHARACTERS } from '../config/constants';
import { FullBodyChar } from './Character';
import { Settings } from 'lucide-react';

export const Menu = ({ playerKey, onPlayerChange, stats, onStartGame, onSettings, char }) => {
  const playerStat = stats[playerKey] || { dailyMathLevel: 0, dailyEnglishLevel: 0 };

  return (
    <div className="p-4 flex flex-col items-center gap-6 z-10 w-full max-w-md">
      <h1 className="text-4xl font-black text-yellow-400 drop-shadow-lg">印家英雄榜</h1>
      
      {/* 角色選擇 */}
      <div className="flex gap-2">
        {Object.values(CHARACTERS).map(c => (
          <button
            key={c.id}
            onClick={() => onPlayerChange(c.id)}
            className={`p-3 rounded-xl border-2 transition-all active:scale-95 ${
              playerKey === c.id
                ? 'border-yellow-400 bg-white/20'
                : 'border-transparent opacity-50'
            }`}
          >
            <div className="text-3xl">{c.avatar}</div>
          </button>
        ))}
      </div>

      {/* 角色資訊 */}
      <div className="bg-white/10 p-8 rounded-[3rem] w-full border-2 border-white/20 text-center relative">
        <div className="scale-125 mb-4">
          <FullBodyChar charId={playerKey} items={stats[playerKey]?.earnedItems} />
        </div>
        <h2 className="text-xl font-bold mb-2">{char.name}</h2>
        {char.subName && <p className="text-sm text-gray-300 mb-4">{char.subName}</p>}
        
        {/* 關卡資訊 */}
        <div className="mb-4 text-sm text-gray-300">
          <div>數學 Lv.{playerStat.dailyMathLevel || 0}</div>
          <div>英文 Lv.{playerStat.dailyEnglishLevel || 0}</div>
          <div>總分: {playerStat.dailyScore || 0}</div>
        </div>

        {/* 開始遊戲按鈕 */}
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => onStartGame('daily_math')}
            className="bg-orange-600 hover:bg-orange-700 p-3 rounded-xl font-bold shadow-lg active:scale-95 transition-colors"
          >
            數學 Lv.{playerStat.dailyMathLevel || 0}
          </button>
          <button
            onClick={() => onStartGame('daily_english')}
            className="bg-blue-600 hover:bg-blue-700 p-3 rounded-xl font-bold shadow-lg active:scale-95 transition-colors"
          >
            英文 Lv.{playerStat.dailyEnglishLevel || 0}
          </button>
        </div>
      </div>

      {/* 管理按鈕 */}
      <div className="flex gap-4 text-sm text-gray-400 font-bold">
        <button
          onClick={onSettings}
          className="bg-white/10 px-3 py-1 rounded-full flex items-center gap-1 hover:bg-white/20 active:scale-95 transition-colors"
        >
          <Settings size={16} />
          <span>管理</span>
        </button>
      </div>
    </div>
  );
};
