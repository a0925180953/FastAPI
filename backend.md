
---

## 💬 WebSocket 規範

- 連線時必須帶 JWT Token
- 使用單一 WebSocket 管理模組（utils/websocket.js）
- 禁止在 component 內直接 new WebSocket

---

## 🧠 狀態管理（Pinia）

必須建立：

- useAuthStore
  - token
  - user_info
  - login/logout

- useChatStore
  - messages
  - sendMessage()
  - receiveMessage()

---

## 🖥 頁面需求（Views）

### 1️⃣ 註冊頁 (Register.vue)
- 欄位：
  - username
  - password
  - confirm password
- 呼叫 API：`/api/register`

---

### 2️⃣ 登入頁 (Login.vue)
- 欄位：
  - username
  - password
- 成功後：
  - 儲存 token
  - 導向 Chat 頁

---

### 3️⃣ 忘記密碼 (ForgotPassword.vue)
- 輸入 email 或 username
- 呼叫 `/api/forgot-password`

---

### 4️⃣ 聊天室 (Chat.vue)

功能：
- 顯示聊天紀錄
- 發送訊息
- 即時接收訊息（WebSocket）

---

## 🔄 WebSocket 流程

1. 進入 Chat 頁面 → 建立連線
2. 接收訊息 → 更新 store
3. 發送訊息 → WebSocket send
4. 離開頁面 → 關閉連線

---

## 🪵 Logging 規範

- 所有錯誤必須使用 `logRemote()`
- 禁止 console.log()

---

## ❌ 禁止事項（非常重要）

- 禁止硬編碼 API URL
- 禁止在 component 直接寫 business logic
- 禁止未處理錯誤
- 禁止直接操作 DOM（非必要）
違反以上規範的程式碼，必須自動重構為符合架構的版本。

---

## 🧪 驗證要求（Agent 必須完成）

- 登入後能成功拿到 token
- WebSocket 能正常收發訊息
- 刷新頁面 token 不遺失
- 聊天紀錄能正確顯示
