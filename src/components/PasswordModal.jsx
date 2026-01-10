import { useState } from 'react';
import { playSFX } from '../utils/audio';

export const PasswordModal = ({ targetPassword, onSuccess, onClose }) => {
  const [input, setInput] = useState("");

  const handleNum = (n) => {
    const next = input + n;
    setInput(next);
    
    if (next === targetPassword) {
      playSFX('start');
      onSuccess();
    } else if (next.length >= targetPassword.length) {
      setInput("");
      alert("密碼錯誤");
      playSFX('hit');
    } else {
      playSFX('click');
    }
  };

  const handleDelete = () => {
    setInput(input.slice(0, -1));
    playSFX('click');
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-pop">
      <div className="bg-slate-800 p-6 rounded-2xl border-2 border-blue-400 w-full max-w-xs text-center">
        <h3 className="text-xl font-bold mb-4">🔒 請輸入密碼</h3>
        <div className="bg-black/50 p-4 rounded-xl text-3xl font-mono tracking-widest mb-6 h-16 flex items-center justify-center">
          {input.length > 0 ? "*".repeat(input.length) : <span className="opacity-30">----</span>}
        </div>
        <div className="grid grid-cols-3 gap-3 mb-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
            <button
              key={n}
              onClick={() => handleNum(n.toString())}
              className="numpad-btn active:scale-95"
            >
              {n}
            </button>
          ))}
          <button
            onClick={onClose}
            className="numpad-btn text-red-400 text-sm active:scale-95"
          >
            取消
          </button>
          <button
            onClick={() => handleNum("0")}
            className="numpad-btn active:scale-95"
          >
            0
          </button>
          <button
            onClick={handleDelete}
            className="numpad-btn text-sm active:scale-95"
          >
            ⬅️
          </button>
        </div>
      </div>
    </div>
  );
};
