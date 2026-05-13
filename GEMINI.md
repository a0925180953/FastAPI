# GEMINI.md

本文件旨在為 Gemini (Gemini Code Assist / API) 提供此專案的開發上下文與規範。
語言偏好：繁體中文 (Traditional Chinese)。
專案助理：野原新之助的專屬開發助手(動感超人)。

## 🎯 專案概覽
- **專案名稱**: FastAPI & Vue3 AI 聊天系統
- **目標**: 建立一個支援多頻道、即時通訊 (WebSocket) 且整合多種 AI 模型的現代化聊天室。
- **核心技術**: Python (FastAPI), Vue 3 (Vite), SQLite, WebSocket, OpenAI/Gemini API.
- **主要場景**: 用於多人即時互動、AI 輔助對話，並具備完善的日誌與環境自動化配置。

## 🛠 技術棧與版本 (Technology Stack)
- **Language**: Python 3.11+, TypeScript/JavaScript
- **Frontend**: Vue 3 (Composition API), Vite, Tailwind CSS, Pinia/Router
- **Backend API**: FastAPI (Asynchronous)
- **Database**: SQLite (SQLAlchemy ORM)
- **Real-time**: WebSockets
- **Dev Tools**: Docker, Batch Scripts (setup.bat, dev.bat)

## 🏗 專案架構 (Architecture)
請遵循以下目錄結構與規範：
- `backend/`: FastAPI 後端邏輯
  - `api/`: 認證 (Auth) 與 WebSocket 路由
  - `models/`: SQLAlchemy 資料庫模型
  - `utils/`: 安全性 (Security) 與 日誌 (Logger) 工具
  - `ws/`: WebSocket 頻道連線管理器 (Manager)
- `frontend/`: Vue 3 前端程式碼
  - `src/api/`: 統一 Axios 調用與日誌回傳工具
  - `src/views/`: 聊天室、登入、註冊、設定、忘記密碼頁面
- `logs/`: 自動生成的前後端分離日誌 (backend.log, frontend.log, backend_runtime.log)

## 📝 開發規範 (Guidelines)
1. **日誌管理**: 禁止使用 `print()` 偵錯。後端請用 `backend_logger`，前端發生錯誤時必須透過 `logRemote` 回傳至伺服器持久化。
2. **安全性**: 
   - 敏感網址與 API Key 必須存放於 `.env`。
   - 所有 API 調用與 WebSocket 連線需驗證 JWT Token。
3. **前端 API**: 統一使用 `src/api/api.js`，禁止在元件內直接使用 `fetch` 硬編碼網址。
4. **AI 異常處理**: 當 AI 額度不足或失效時，必須記錄 Error Log 並回覆「AI目前沒額度可使用，請稍後再試，或者找動感超人幫忙喔！」。
5. **風格規範**: 變數使用 `snake_case` (後端)，類別使用 `PascalCase`；註解需清晰並使用繁體中文。

## 🚀 常用指令 (Essential Commands)
- **環境初始化**: 執行 `setup.bat` (自動安裝前後端依賴並建立 .env 範本)。
- **全能量啟動**: 執行 `dev.bat` (同時啟動前後端，並將背景輸出導向日誌)。
- **Docker 啟動**: `docker-compose up --build` (跨平台容器化測試)。
- **手動安裝**:
  - 後端: `pip install -r requirements.txt`
  - 前端: `cd frontend && npm install`

## ⚠️ 陷阱與注意事項 (Important Notes)
- **網址硬編碼**: 前端已整合環境變數。若需修改連線網址，請編輯 `frontend/.env` 中的 `VITE_API_BASE_URL`。
- **資料庫同步**: 修改模型後需刪除 `chat.db` 並執行 `python backend/create_db.py` 重新生成。
- **日誌追蹤**: 開發時可持續監控 `logs/backend_runtime.log` 以獲取即時狀態而不干擾 UI。
