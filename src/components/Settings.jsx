import { useState, useEffect } from 'react';
import { ArrowLeft } from 'lucide-react';
import { firebaseAuth, initFirebase } from '../services/firebase';
import { firestoreService } from '../services/firebase';

export const Settings = ({ userObj, onUserChange, stats, vocabMap, mathSettings, onBack, onSave }) => {
  const [loading, setLoading] = useState(false);
  const [localUser, setLocalUser] = useState(userObj);

  useEffect(() => {
    setLocalUser(userObj);
  }, [userObj]);

  const handleConnectCloud = async () => {
    setLoading(true);
    try {
      if (!initFirebase()) {
        alert('Firebase 初始化失敗');
        return;
      }
      
      const user = await firebaseAuth.signIn();
      setLocalUser(user);
      
      // 嘗試載入雲端存檔
      const cloudData = await firestoreService.loadUserData(user.uid);
      if (cloudData) {
        const shouldLoad = window.confirm('讀取雲端存檔？');
        if (shouldLoad) {
          if (cloudData.stats) onSave(cloudData.stats, cloudData.vocabMap, cloudData.mathSettings);
          alert('已載入雲端存檔');
        }
      }
      
      onUserChange(user);
    } catch (error) {
      console.error('Connect cloud error:', error);
      alert('連線失敗: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = async () => {
    setLoading(true);
    try {
      await firebaseAuth.signOut();
      setLocalUser(null);
      onUserChange(null);
      alert('已登出');
    } catch (error) {
      console.error('Sign out error:', error);
      alert('登出失敗: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSyncToCloud = async () => {
    if (!localUser) {
      alert('請先登入');
      return;
    }
    
    setLoading(true);
    try {
      const success = await firestoreService.saveUserData(localUser.uid, {
        stats,
        vocabMap,
        mathSettings
      });
      
      if (success) {
        alert('已同步到雲端');
      } else {
        alert('同步失敗');
      }
    } catch (error) {
      console.error('Sync error:', error);
      alert('同步失敗: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full bg-slate-900 p-6 z-20 text-white overflow-y-auto">
      <div className="flex items-center mb-6">
        <button
          onClick={onBack}
          className="mr-4 p-2 hover:bg-white/10 rounded-lg active:scale-95 transition-colors"
        >
          <ArrowLeft size={24} />
        </button>
        <h2 className="text-2xl font-bold">管理中心</h2>
      </div>

      {/* 雲端同步區塊 */}
      <div className="bg-white/10 p-4 rounded-xl mb-4">
        <h3 className="font-bold mb-2">☁️ 雲端同步</h3>
        {localUser ? (
          <div className="space-y-2">
            <div className="text-sm text-gray-300 mb-2">
              已登入: {localUser.email}
            </div>
            <button
              onClick={handleSyncToCloud}
              disabled={loading}
              className="bg-green-600 hover:bg-green-700 disabled:opacity-50 px-4 py-2 rounded w-full mb-2 active:scale-95 transition-colors"
            >
              {loading ? '處理中...' : '上傳到雲端'}
            </button>
            <button
              onClick={handleSignOut}
              disabled={loading}
              className="bg-red-600 hover:bg-red-700 disabled:opacity-50 px-4 py-2 rounded w-full active:scale-95 transition-colors"
            >
              登出
            </button>
          </div>
        ) : (
          <button
            onClick={handleConnectCloud}
            disabled={loading}
            className="bg-white text-black hover:bg-gray-200 disabled:opacity-50 px-4 py-2 rounded w-full active:scale-95 transition-colors"
          >
            {loading ? '處理中...' : 'Google 登入同步'}
          </button>
        )}
      </div>

      {/* 統計資訊 */}
      <div className="bg-white/10 p-4 rounded-xl mb-4">
        <h3 className="font-bold mb-2">📊 遊戲統計</h3>
        <div className="space-y-1 text-sm">
          {Object.entries(stats).map(([key, stat]) => (
            <div key={key} className="flex justify-between">
              <span className="text-gray-300">{key}:</span>
              <span>
                數學 Lv.{stat.dailyMathLevel} | 英文 Lv.{stat.dailyEnglishLevel}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 其他設定 */}
      <div className="bg-white/10 p-4 rounded-xl mb-4">
        <h3 className="font-bold mb-2">⚙️ 其他設定</h3>
        <p className="text-sm text-gray-400">
          更多設定功能開發中...
        </p>
      </div>
    </div>
  );
};
