<script setup>
import { ref } from "vue";
import { register } from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const password = ref("");
const message = ref("");
const isError = ref(false);

const handleRegister = async () => {
  try {
    const res = await register(username.value, password.value);
    message.value = res.data.message;
    isError.value = false;
    
    // 註冊成功後，延遲一下下再跳轉到登入頁面
    setTimeout(() => {
      router.push("/login");
    }, 2000);
    
  } catch (err) {
    isError.value = true;
    message.value = err.response?.data?.detail || "註冊失敗，再試一次吧！";
  }
};
</script>

<template>
  <div class="h-screen flex items-center justify-center bg-[#313338]">
    <div class="bg-[#2b2d31] p-8 rounded-lg shadow-xl w-96 text-white">
      <h2 class="text-2xl font-bold mb-6 text-center">建立帳號</h2>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">使用者名稱</label>
          <input 
            v-model="username" 
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="你想叫什麼名字呢？" 
          />
        </div>
        
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">密碼</label>
          <input 
            v-model="password" 
            type="password"
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="密碼要記住哦！" 
          />
        </div>
        
        <button 
          @click="handleRegister"
          class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-bold transition duration-200"
        >
          註冊
        </button>
        
        <p v-if="message" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm text-center mt-4">
          {{ message }}
        </p>
        
        <div class="text-sm text-gray-400 mt-4 text-center">
          已經有帳號了？
          <router-link to="/login" class="text-blue-400 hover:underline">去登入</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
