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

export const register = (username, password) => {
  return api.post("/register", {
    username: username,
    password: password
  });
};

export const getCurrentUser = () => {
  return api.get("/me");
};

export const updateProfile = (data) => {
  return api.patch("/me", data);
};

// 4️⃣ export api（給其他頁用）
export default api;