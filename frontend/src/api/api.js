import axios from "axios";

// 1️⃣ 建立 axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// 2️⃣ 自動帶 token（重點）
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// 3️⃣ login（保留你原本寫法）
export const login = (username, password) => {
  const form = new URLSearchParams();

  form.append("username", username);
  form.append("password", password);

  return api.post("/login", form, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  });
};

// 4️⃣ export api（給其他頁用）
export default api;