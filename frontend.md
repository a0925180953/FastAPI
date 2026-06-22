# 🌐 Frontend 開發規範 (Vue 3 + WebSocket)

## 🎯 目標
建立一個基於 Vue 3 的即時聊天室前端，整合 REST API 與 WebSocket。

---

## 🏗 技術架構

- Vue 3 (Composition API)
- Vite
- Tailwind CSS
- Pinia（狀態管理）
- Vue Router
- Axios（API 呼叫）
- WebSocket（即時通訊）

---

## 📂 專案結構（強制遵守）

frontend/src/

- api/ → 所有 API 呼叫
- stores/ → Pinia 狀態管理
- views/ → 頁面（Login, Register, Chat）
- components/ → 可重用元件
- router/ → 路由設定
- utils/ → 工具（WebSocket、logger）

---

## 🔐 認證流程（Auth Flow）

1. 使用者登入 → 呼叫 `/api/login`
2. 取得 JWT Token
3. Token 存入：
   - Pinia
   - localStorage
4. 所有 API 必須自動帶入 Token（Axios 攔截器）

---

## 📡 API 呼叫規範

- 禁止在 component 內直接使用 axios
- 統一從 `src/api/api.js` 呼叫
- 必須使用環境變數：
