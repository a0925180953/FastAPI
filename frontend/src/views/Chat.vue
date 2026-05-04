<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";

const ws = ref(null);
const message = ref("");
const messages = ref([]);
const chatBox = ref(null);

// 👉 這裡先簡單寫死（之後可從 token decode）
const username = "Tom";

onMounted(() => {
  const token = localStorage.getItem("token");

  ws.value = new WebSocket(`ws://127.0.0.1:8000/ws?token=${token}`);

  ws.value.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    messages.value.push(data);

    // 🔥 自動滾動到底
    await nextTick();
    chatBox.value.scrollTop = chatBox.value.scrollHeight;
  };
});

const sendMessage = () => {
  if (!message.value.trim()) return;

  ws.value.send(
    JSON.stringify({
      message: message.value,
    })
  );

  message.value = "";
};

onBeforeUnmount(() => {
  ws.value?.close();
});
</script>

<template>
  <div class="flex flex-col h-screen p-4 bg-gray-100">
    <h1 class="text-xl font-bold mb-4">聊天室</h1>

    <!-- 訊息區 -->
    <div ref="chatBox" class="flex-1 overflow-y-auto space-y-2 mb-4">
      <div
        v-for="(msg, i) in messages"
        :key="i"
        class="flex"
        :class="msg.user === username ? 'justify-end' : 'justify-start'"
      >
        <div
          class="px-3 py-2 rounded-lg max-w-xs"
          :class="msg.user === username
            ? 'bg-blue-500 text-white'
            : 'bg-white border'"
        >
          <div class="text-xs opacity-70 mb-1">
            {{ msg.user }}
          </div>
          <div>{{ msg.message }}</div>
        </div>
      </div>
    </div>

    <!-- 輸入區 -->
    <div class="flex gap-2">
      <input
        v-model="message"
        class="border p-2 flex-1 rounded"
        placeholder="輸入訊息..."
        @keyup.enter="sendMessage"
      />
      <button
        @click="sendMessage"
        class="bg-blue-500 text-white px-4 rounded"
      >
        送出
      </button>
    </div>
  </div>
</template>