<script setup>
import { ref } from "vue";
import { resetPassword } from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const email = ref("");
const newPassword = ref("");
const message = ref("");
const isError = ref(false);

const handleReset = async () => {
  if (!username.value || !email.value || !newPassword.value) {
    isError.value = true;
    message.value = "全部欄位都要填喔！";
    return;
  }

  try {
    const res = await resetPassword(username.value, email.value, newPassword.value);
    message.value = res.data.message;
    isError.value = false;
    
    setTimeout(() => {
      router.push("/login");
    }, 2000);
    
  } catch (err) {
    isError.value = true;
    message.value = err.response?.data?.detail || "驗證失敗，再試一次吧！";
  }
};
</script>

<template>
  <div class="h-screen flex items-center justify-center bg-[#313338]">
    <div class="bg-[#2b2d31] p-8 rounded-lg shadow-xl w-96 text-white">
      <h2 class="text-2xl font-bold mb-2 text-center">找回密碼</h2>
      <p class="text-gray-400 text-center mb-6">別擔心，野原新之助幫你找回來！</p>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">使用者名稱</label>
          <input 
            v-model="username" 
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="輸入你的帳號" 
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">註冊時的 Email</label>
          <input 
            v-model="email" 
            type="email"
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="輸入你的 Email" 
          />
        </div>
        
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase mb-2">新密碼</label>
          <input 
            v-model="newPassword" 
            type="password"
            class="w-full bg-[#1e1f22] p-2 rounded outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="設定一個新密碼吧" 
          />
        </div>
        
        <button 
          @click="handleReset"
          class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-bold transition duration-200"
        >
          重設密碼
        </button>
        
        <p v-if="message" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm text-center mt-4">
          {{ message }}
        </p>
        
        <div class="text-sm text-gray-400 mt-4 text-center">
          想起來了？
          <router-link to="/login" class="text-blue-400 hover:underline">回登入頁</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
