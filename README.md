# FastAPI & Vue3 AI 聊天系統 🚀

這是一個基於 **FastAPI** 與 **Vue 3 (Vite)** 構建的現代化 AI 聊天系統。支援多頻道即時通訊 (WebSocket)、完整的使用者認證流程，並整合了遠端日誌追蹤功能。

> **專案小助手提示**: 嘿嘿～我是野原新之助的專屬助手動感超人！這份文件會帶你快速了解這個超酷的專案！

---

## 🛠 技術棧 (Tech Stack)

- **後端 (Backend)**:
  - [FastAPI](https://fastapi.tiangolo.com/): 高性能非同步 Python Web 框架。
  - [SQLAlchemy](https://www.sqlalchemy.org/): 資料庫 ORM 工具。
  - [SQLite](https://sqlite.org/): 輕量級關聯式資料庫。
  - [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API): 實現即時通訊。
- **前端 (Frontend)**:
  - [Vue 3](https://vuejs.org/): Composition API 漸進式框架。
  - [Vite](https://vitejs.dev/): 極速的前端開發建置工具。
  - [Tailwind CSS](https://tailwindcss.com/): Utility-first CSS 框架。
  - [Axios](https://axios-http.com/): HTTP 客戶端。

---

## 📂 專案結構與負責項目 (Project Structure)

### 📂 根目錄 (Root)
```text
.
├── backend/                # 後端專案目錄
├── frontend/               # 前端專案目錄
├── logs/                   # 存放系統生成的日誌文件
├── .env                    # 後端環境變數配置 (包含 API Key)
├── docker-compose.yml      # Docker 容器化編排配置
├── setup.bat               # 環境初始化腳本 (安裝依賴、建立 .env)
├── dev.bat                 # 一鍵開發啟動腳本 (同時啟動前後端)
├── requirements.txt        # Python 後端依賴清單
└── package.json            # 專案管理腳本
```

### 🐍 後端結構 (Backend)
```text
backend/
├── api/
│   ├── auth.py             # 認證路由：負責 登入、註冊、忘記密碼 等 API
│   └── websocket.py        # 通訊路由：處理 WebSocket 連線請求
├── database/
│   └── chat.db             # SQLite 資料庫檔案 (自動生成)
├── models/
│   └── models.py           # SQLAlchemy 模型：定義 User, Message 等資料表結構
├── utils/
│   ├── logger.py           # 日誌工具：自定義 backend_logger 格式與存放路徑
│   └── security.py         # 安全工具：JWT 加密解密、密碼雜湊處理
├── ws/
│   └── manager.py          # WebSocket 管理器：處理頻道加入、廣播與連線維持
├── config.py               # 全域配置：讀取 .env 並提供環境變數存取
├── create_db.py            # 初始化腳本：用於建立資料庫結構
├── database.py             # 資料庫連線配置：建立 Engine 與 SessionLocal
├── main.py                 # 後端入口：初始化 FastAPI 應用與路由掛載
└── schemas.py              # Pydantic 模型：定義 API 請求與回應的資料格式
```

### 🎨 前端結構 (Frontend)
```text
frontend/
├── src/
│   ├── api/
│   │   └── api.js          # 通訊核心：封裝 Axios 並實作 logRemote 遠端日誌功能
│   ├── router/
│   │   └── index.js        # 路由配置：定義各頁面路徑與導航守衛
│   ├── views/
│   │   ├── Chat.vue        # 聊天室主頁面：即時訊息呈現與輸入
│   │   ├── Login.vue       # 登入頁面
│   │   ├── Register.vue    # 註冊頁面
│   │   ├── Settings.vue    # 個人設定頁面
│   │   └── ForgotPassword.vue # 忘記密碼處理頁面
│   ├── App.vue             # 前端根元件
│   ├── main.ts             # 前端入口：初始化 Vue 實例與掛載套件
│   └── style.css           # 全域樣式與 Tailwind CSS 載入
├── index.html              # HTML 模板
└── vite.config.ts          # Vite 建置配置
```

---

## 🚀 快速開始 (Getting Started)

### 1. 環境初始化
執行以下腳本自動安裝所有依賴並建立 `.env` 範本：
```bash
setup.bat
```

### 2. 啟動開發環境
執行以下腳本同時啟動 FastAPI 後端與 Vite 前端：
```bash
dev.bat
```
- 前端網址: `http://localhost:5173`
- 後端 API: `http://localhost:8000`
- API 文件: `http://localhost:8000/docs`

---

## 📝 開發規範與注意事項

1. **日誌管理**:
   - 後端使用 `backend_logger` 記錄重要事件。
   - 前端錯誤會透過 `logRemote` 回傳至後端 `logs/frontend.log`，方便集中監控。
2. **AI 回覆**:
   - 若 AI API 額度不足或發生異常，系統將統一回覆：「AI目前沒額度可使用，請稍後再試，或者找動感超人幫忙喔！」。
3. **資料庫異動**:
   - 若修改了 `backend/models/models.py`，請刪除 `chat.db` 並重新執行 `python backend/create_db.py`。

---

## 🛡 安全性
- 所有敏感資訊 (如 `JWT_SECRET`, `AI_API_KEY`) 必須存放於根目錄的 `.env`。
- API 呼叫需帶上 JWT Token 進行驗證。

---

## 🧪 測試與 CI/CD (Testing & CI/CD)

本專案整合了自動化測試與 GitHub Actions 流程：

### 1. 後端測試 (Pytest)
使用 `pytest` 進行單元測試與整合測試。
- **測試目錄**: `backend/tests/`
- **執行測試**:
  ```bash
  $env:PYTHONPATH="."; venv\Scripts\pytest backend/tests
  ```

### 2. 前端測試 (Vitest)
使用 `vitest` 進行元件與邏輯測試。
- **測試目錄**: `frontend/src/__tests__/`
- **執行測試**:
  ```bash
  cd frontend && npm run test
  ```

### 3. CI/CD 流程
當程式碼推送到 `main` 或 `master` 分支，或發起 Pull Request 時，GitHub Actions 會自動執行：
- **Backend-tests**: 安裝依賴並執行 `pytest`。
- **Frontend-check**: 安裝依賴、執行 `vitest` 並嘗試 `npm run build` 確保建置正常。

---

