<script setup>
import { ref } from "vue";
import { login } from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const password = ref("");
const errorMessage = ref("");

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = "請填寫帳號與密碼。";
    return;
  }
  
  try {
    const res = await login(username.value, password.value);
    
    // ✅ 1. 存 token
    localStorage.setItem("token", res.data.access_token);

    // ✅ 2. 跳頁
    router.push("/chat");

  } catch (err) {
    console.error("登入失敗", err);
    errorMessage.value = err.response?.data?.detail || "登入失敗，請檢查您的帳號密碼。";
  }
};
</script>

<template>
  <div class="h-screen flex items-center justify-center bg-[#313338]">
    <div class="bg-[#2b2d31] p-8 rounded-lg shadow-xl w-96 text-white">
      <h2 class="text-2xl font-bold mb-2 text-center">歡迎回來！</h2>
      <p class="text-gray-400 text-center mb-6">很高興見到您，請登入以繼續。</p>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">使用者名稱</label>
          <input 
            v-model="username" 
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="請輸入帳號" 
          />
        </div>
        
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">密碼</label>
          <input 
            v-model="password" 
            type="password"
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="請輸入密碼" 
          />
        </div>
        
        <button 
          @click="handleLogin"
          class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-bold transition duration-200"
        >
          登入
        </button>
        
        <p v-if="errorMessage" class="text-red-400 text-sm text-center mt-4">
          {{ errorMessage }}
        </p>
        
        <div class="flex justify-between items-center mt-4 text-sm text-gray-400">
          <router-link to="/forgot-password" class="text-blue-400 hover:underline">忘記密碼？</router-link>
          <span>
            需要帳號嗎？
            <router-link to="/register" class="text-blue-400 hover:underline">註冊一個吧</router-link>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
