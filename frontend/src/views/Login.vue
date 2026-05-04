<script setup>
import { ref } from "vue";
import { login } from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();   // ⭐ 路由控制

const username = ref("");
const password = ref("");

const handleLogin = async () => {
  try {
    console.log(username.value, password.value);
    const res = await login(username.value, password.value);

    console.log(res.data);

    // ✅ 1. 存 token
    localStorage.setItem("token", res.data.access_token);

    // ✅ 2. 跳頁
    router.push("/chat");

  } catch (err) {
    console.error("登入失敗", err);
  }
};
</script>

<template>
	<h1 class="text-3xl text-red-500">
  Hello Tailwind
</h1>
  <input v-model="username" placeholder="帳號" />
  <input v-model="password" type="password" placeholder="密碼" />
  <button @click="handleLogin">登入</button>
</template>