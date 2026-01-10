# 快速開始指南

## 問題：應用一直顯示「🚀 載入中...」

如果應用一直顯示載入畫面，請按照以下步驟檢查：

### 1. 安裝依賴（必需）

```bash
npm install
```

如果沒有安裝依賴，Vite 無法編譯和運行應用。

### 2. 啟動開發服務器

```bash
npm run dev
```

等待 Vite 編譯完成，會顯示類似以下訊息：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 3. 在瀏覽器中打開

打開瀏覽器並訪問 `http://localhost:5173/`

### 4. 檢查瀏覽器控制台

如果仍然有問題，打開瀏覽器的開發者工具（F12），查看 Console 標籤是否有錯誤訊息。

常見錯誤：
- **模組未找到**：需要運行 `npm install`
- **Firebase 錯誤**：應用會自動切換到 LocalStorage 模式，仍可正常使用
- **編譯錯誤**：檢查終端機的錯誤訊息

### 5. 如果 Firebase 初始化失敗

應用設計為在 Firebase 初始化失敗時自動切換到 LocalStorage 模式，所有功能仍可使用，只是無法同步到雲端。

### 檢查清單

- [ ] 已運行 `npm install`
- [ ] 已運行 `npm run dev` 且沒有錯誤
- [ ] 瀏覽器訪問正確的 URL（通常是 `http://localhost:5173/`）
- [ ] 瀏覽器控制台沒有嚴重錯誤（Firebase 警告可忽略）

### 需要幫助？

如果問題持續，請檢查：
1. Node.js 版本是否為 16+（運行 `node -v`）
2. 終端機的完整錯誤訊息
3. 瀏覽器控制台的完整錯誤訊息
