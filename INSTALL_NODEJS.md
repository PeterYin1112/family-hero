# 安裝 Node.js 指南

## 步驟

1. **下載 Node.js**：
   - 訪問：https://nodejs.org/
   - 下載 LTS 版本（推薦，例如 v20.x 或 v18.x）
   - 選擇 Windows Installer (.msi)

2. **安裝**：
   - 執行下載的 .msi 文件
   - 一直點「下一步」（Next），使用預設選項
   - ✅ **重要**：確保勾選「Add to PATH」選項

3. **驗證安裝**：
   - 重新啟動 VS Code 和 PowerShell
   - 運行以下命令：
     ```powershell
     node --version
     npm --version
     ```
   - 應該會顯示版本號（例如：v20.10.0）

4. **安裝專案依賴**：
   ```powershell
   npm install
   ```

5. **啟動開發服務器**：
   ```powershell
   npm run dev
   ```

## 如果安裝後仍無法使用

1. **重新啟動 VS Code**（完全關閉並重新打開）
2. **重新啟動 PowerShell**（關閉並重新打開終端）
3. **檢查環境變數**：
   - 按下 `Win + R`，輸入 `sysdm.cpl`，按 Enter
   - 點擊「進階」→「環境變數」
   - 確認「系統變數」中的 `Path` 包含 Node.js 的安裝路徑（通常是 `C:\Program Files\nodejs\`）
