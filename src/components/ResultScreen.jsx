export const ResultScreen = ({ level, onBack }) => {
  return (
    <div className="h-full flex flex-col items-center justify-center bg-slate-900 text-white p-8 text-center animate-pop">
      <div className="text-8xl mb-4">🏆</div>
      <h2 className="text-4xl font-bold mb-4">通過第 {level} 關!</h2>
      <button
        onClick={onBack}
        className="bg-white text-black px-8 py-3 rounded-xl font-bold hover:bg-gray-200 active:scale-95 transition-colors"
      >
        返回
      </button>
    </div>
  );
};
