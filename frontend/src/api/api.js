import axios from "axios";

// 1️⃣ 建立 axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

// 2️⃣ 自動帶 token（重點）
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// 3️⃣ 處理回應（自動登出邏輯）
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token 過期或無效
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// 4️⃣ login（保留你原本寫法）
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

export const register = (username, password, email = null) => {
  return api.post("/register", {
    username: username,
    password: password,
    email: email
  });
};

export const resetPassword = (username, email, newPassword) => {
  return api.post("/reset-password", {
    username: username,
    email: email,
    new_password: newPassword
  });
};

export const getCurrentUser = () => {
  return api.get("/me");
};

export const getHistory = (channel) => {
  return api.get("/history", {
    params: { channel: channel }
  });
};

export const updateProfile = (data) => {
  return api.patch("/me", data);
};

// 傳送日誌到後端
export const logRemote = (level, message, stack = null) => {
  return api.post("/logs/frontend", {
    level: level,
    message: message,
    url: window.location.href,
    stack: stack
  }).catch(() => {
    // 如果連日誌都傳不出去，就只印在 console
    console.warn("Log failed to send to server.");
  });
};

// 4️⃣ export api（給其他頁用）
export default api;