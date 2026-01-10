# 如何使用 Live Server 執行

## ⚠️ 重要說明

**Live Server 無法直接處理 React + Vite 專案！**

原因：
- Live Server 只是簡單的 HTTP 服務器
- 無法編譯 JSX/React 代碼
- 無法處理 ES6 模組（import/export）
- 無法處理 TypeScript/JSX 轉換

## ✅ 解決方案

### 方案 1：使用 Vite 開發服務器（推薦）

1. **安裝依賴**：
   ```bash
   npm install
   ```

2. **啟動開發服務器**：
   ```bash
   npm run dev
   ```

3. Vite 會自動在瀏覽器中打開應用（通常是 `http://localhost:5173/`）

**優點**：
- ✅ 熱重載（修改代碼自動刷新）
- ✅ 快速編譯
- ✅ 支援所有 React 功能
- ✅ 錯誤訊息更清晰

---

### 方案 2：先建置，再用 Live Server（可行但不推薦）

如果你**必須**使用 Live Server，需要先建置成靜態文件：

1. **安裝依賴**（只需要一次）：
   ```bash
   npm install
   ```

2. **建置生產版本**：
   ```bash
   npm run build
   ```

   這會生成 `dist` 資料夾，包含所有編譯好的靜態文件。

3. **用 Live Server 打開 `dist/index.html`**：
   - 在 VS Code 中，右鍵點擊 `dist/index.html`
   - 選擇 "Open with Live Server"

**缺點**：
- ❌ 每次修改代碼都需要重新建置（`npm run build`）
- ❌ 沒有熱重載
- ❌ 開發效率低
- ❌ 錯誤訊息可能不清楚

---

## 🔍 為什麼 Live Server 一直顯示「載入中」？

因為：
1. Live Server 無法編譯 JSX → JavaScript
2. 瀏覽器無法執行 `import React from 'react'` 這樣的語句
3. `src/main.jsx` 是 JSX 文件，瀏覽器無法直接讀取

所以應用會停在「載入中」，因為 JavaScript 根本沒有執行。

---

## 💡 建議

**請使用 `npm run dev`**，它會：
- 自動編譯所有文件
- 提供熱重載
- 顯示清楚的錯誤訊息
- 讓開發更順暢

如果你不熟悉 npm，只需要記住：
1. `npm install` （第一次，安裝依賴）
2. `npm run dev` （每次開發時運行）

就是這麼簡單！🚀
