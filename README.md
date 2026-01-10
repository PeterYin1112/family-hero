# 印家英雄榜 (Family Hero Quest) 🎮

一款專為家庭設計的教育型 RPG 網頁遊戲，透過「打怪獸」的遊戲化機制，激勵孩子練習數學與英文。

## 專案概述

這是一個完整的 React + Vite 專案，將原本的單一 HTML 文件重構為現代化的模組化架構。

## 技術棧

- **Frontend**: React 18, Tailwind CSS, Lucide React (Icons)
- **Backend/Storage**: Google Firebase (Firestore, Auth)
- **Build Tool**: Vite
- **Design**: Mobile-First, Responsive (RWD)

## 安裝與運行

### 前置需求

- Node.js 16+ 
- npm 或 yarn

### 安裝依賴

```bash
npm install
```

### 開發模式

```bash
npm run dev
```

應用將在 `http://localhost:5173` 啟動

### 建置生產版本

```bash
npm run build
```

建置結果將輸出到 `dist/` 目錄

### 預覽生產版本

```bash
npm run preview
```

## 專案結構

```
family-hero/
├── src/
│   ├── components/          # React 組件
│   │   ├── BattleScene.jsx  # 戰鬥場景組件
│   │   ├── Character.jsx    # 角色顯示組件
│   │   ├── ErrorBoundary.jsx # 錯誤邊界
│   │   ├── Menu.jsx         # 主選單組件
│   │   ├── PasswordModal.jsx # 密碼輸入模態框
│   │   ├── ResultScreen.jsx # 結果畫面組件
│   │   └── Settings.jsx     # 設定頁面組件
│   ├── config/              # 配置檔案
│   │   └── constants.js     # 遊戲常數與配置
│   ├── hooks/               # 自定義 Hooks
│   │   └── useGameLogic.js  # 遊戲邏輯 Hook
│   ├── services/            # 服務層
│   │   └── firebase.js      # Firebase 服務
│   ├── utils/               # 工具函數
│   │   ├── audio.js         # 音效與語音功能
│   │   └── storage.js       # 本地儲存管理
│   ├── App.jsx              # 主應用組件
│   ├── main.jsx             # 應用入口
│   └── index.css            # 全局樣式
├── index.html               # HTML 入口
├── package.json             # 專案配置
├── vite.config.js           # Vite 配置
├── tailwind.config.js       # Tailwind CSS 配置
└── postcss.config.js        # PostCSS 配置
```

## 核心功能

### 1. 角色系統
- **印品榕 (女兒)**: 冰雪女王主題
- **印晨希 (兒子)**: 甲蟲王者主題
- **印媽媽**: 神力女超人主題
- **挑戰者**: 訪客模式（免密碼）

### 2. 雙軌制進度
- 數學與英文兩條主線
- 平衡機制：每 20 級檢查一次，確保兩科進度平衡

### 3. 戰鬥循環
- 根據等級生成不同強度的怪獸
- 數學題：加減乘除（依等級動態調整難度）
- 英文題：單字填空（支援選擇題與拼字題）
- Fever Mode：連續答對 3 題進入狂熱模式（分數 x1.5）
- 每 10 關結算並觸發寶箱掉落

### 4. 物品與獎勵
- 裝備系統：Weapon, Head, Shield, Pet
- 紙娃娃系統：裝備即時顯示在角色身上
- 每週重置：裝備與分數每週一重置（圖鑑永久保留）

## 開發指南

### 添加新角色

在 `src/config/constants.js` 中的 `CHARACTERS` 物件中添加新角色：

```javascript
newCharacter: {
  id: 'newCharacter',
  name: '角色名稱',
  avatar: '🎮',
  theme: 'princess', // 或 'hero'
  color: 'text-purple-400',
  bg: 'bg-purple-900',
  attackType: 'magic',
  needPwd: true
}
```

### 添加新單字

在 `src/config/constants.js` 中的 `BASE_VOCAB` 陣列中添加：

```javascript
{ word: "hello", type: "noun", mean: "你好" }
```

或在設定頁面通過 UI 添加（功能開發中）。

### 修改數學題難度

在 `src/hooks/useGameLogic.js` 中的 `generateMathQuestion` 函數調整難度計算邏輯。

## Firebase 配置

Firebase 配置已在 `src/services/firebase.js` 中設定。如需更改，請修改 `firebaseConfig` 物件。

### 數據結構

用戶數據儲存在 Firestore 的 `users/{uid}` 路徑下：

```javascript
{
  stats: {
    daughter: { dailyMathLevel, dailyEnglishLevel, dailyScore, earnedItems, monsterBook },
    son: { ... },
    mom: { ... },
    challenger: { ... }
  },
  vocabMap: {
    daughter: [...],
    son: [...],
    // ...
  },
  mathSettings: { ... }
}
```

## 部署

### GitHub Pages

1. 安裝 gh-pages：
```bash
npm install --save-dev gh-pages
```

2. 在 `package.json` 中添加部署腳本：
```json
"scripts": {
  "deploy": "npm run build && gh-pages -d dist"
}
```

3. 執行部署：
```bash
npm run deploy
```

### 其他平台

建置後的 `dist/` 目錄可以直接部署到任何靜態網站託管服務（如 Netlify, Vercel 等）。

## 注意事項

- 手機端輸入英文時，已強制設定 `autoCapitalize="none"` 避免首字大寫誤判
- 若 Firebase 連線失敗，系統會自動切換至 LocalStorage 模式
- 所有動畫效果已遷移到 Tailwind CSS 配置中

## 授權

本專案為家庭內部使用專案。
