<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getCurrentUser, updateProfile } from "../api/api";

const router = useRouter();
const nickname = ref("");
const avatarUrl = ref("");
const password = ref("");
const message = ref("");
const isError = ref(false);

const loadUserData = async () => {
  try {
    const res = await getCurrentUser();
    nickname.value = res.data.nickname || "";
    avatarUrl.value = res.data.avatar_url || "";
  } catch (err) {
    console.error("載入使用者資料失敗", err);
  }
};

const handleUpdate = async () => {
  message.value = "";
  isError.value = false;
  
  try {
    const data = {
      nickname: nickname.value,
      avatar_url: avatarUrl.value,
    };
    
    if (password.value) {
      data.password = password.value;
    }
    
    await updateProfile(data);
    message.value = `更新成功囉！${nickname.value}大人!`;
    password.value = ""; // 清空密碼欄位
  } catch (err) {
    isError.value = true;
    message.value = err.response?.data?.detail || "更新失敗，再試一次吧！";
  }
};

const goBack = () => {
  router.push("/chat");
};

onMounted(loadUserData);
</script>

<template>
  <div class="min-h-screen bg-[#313338] flex items-center justify-center p-4">
    <div class="bg-[#2b2d31] p-8 rounded-lg shadow-xl w-full max-w-md">
      <h2 class="text-2xl font-bold text-white mb-6 flex items-center gap-2">
        ⚙️ 使用者設定
      </h2>

      <div class="space-y-4">
        <!-- 暱稱 -->
        <div>
          <label class="block text-gray-400 text-sm font-bold mb-2">暱稱</label>
          <input
            v-model="nickname"
            type="text"
            placeholder="幫自己取個帥氣的名字吧"
            class="w-full bg-[#1e1f22] text-white p-3 rounded outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- 大頭貼網址 -->
        <div>
          <label class="block text-gray-400 text-sm font-bold mb-2">大頭貼網址</label>
          <input
            v-model="avatarUrl"
            type="text"
            placeholder="放上頭像的連結 (URL)"
            class="w-full bg-[#1e1f22] text-white p-3 rounded outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div v-if="avatarUrl" class="mt-2 flex justify-center">
             <img :src="avatarUrl" alt="預覽" class="w-20 h-20 rounded-full object-cover border-2 border-blue-500" />
          </div>
        </div>

        <!-- 密碼 (選擇性) -->
        <div>
          <label class="block text-gray-400 text-sm font-bold mb-2">變更密碼 (選填)</label>
          <input
            v-model="password"
            type="password"
            placeholder="若不變更請留空"
            class="w-full bg-[#1e1f22] text-white p-3 rounded outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- 提示訊息 -->
        <div v-if="message" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm font-medium">
          {{ message }}
        </div>

        <div class="flex gap-4 mt-8">
          <button
            @click="goBack"
            class="flex-1 bg-gray-600 text-white p-3 rounded font-bold hover:bg-gray-500 transition"
          >
            回聊天室
          </button>
          <button
            @click="handleUpdate"
            class="flex-1 bg-blue-600 text-white p-3 rounded font-bold hover:bg-blue-500 transition"
          >
            儲存變更
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
