<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const ws = ref(null);
const input = ref("");
const messages = ref([]);
const chatBox = ref(null);

const token = localStorage.getItem("token");

const handleLogout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};

onMounted(() => {
  ws.value = new WebSocket(`ws://127.0.0.1:8000/ws?token=${token}`);

  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data);

    messages.value.push({
      role: "ai",
      text: data.message,
      time: new Date().toLocaleTimeString(),
    });

    scrollBottom();
  };
});

onBeforeUnmount(() => {
  ws.value?.close();
});

const sendMessage = () => {
  if (!input.value.trim()) return;

  const msg = input.value;

  // user message
  messages.value.push({
    role: "user",
    text: msg,
    time: new Date().toLocaleTimeString(),
  });

  ws.value.send(JSON.stringify({ message: msg }));

  input.value = "";

  scrollBottom();
};

const scrollBottom = async () => {
  await nextTick();
  if (chatBox.value) {
    chatBox.value.scrollTop = chatBox.value.scrollHeight;
  }
};
</script>

<template>
  <div class="h-screen flex bg-[#313338] text-white">

    <!-- Sidebar -->
    <div class="w-60 bg-[#2b2d31] p-3 flex flex-col justify-between">
      <div>
        <h2 class="text-gray-300 font-bold mb-4">💬 Channels</h2>
        <div class="text-gray-400 hover:text-white cursor-pointer mb-2"># general</div>
        <div class="text-gray-400 hover:text-white cursor-pointer"># ai-chat</div>
      </div>
      
      <!-- Logout Button -->
      <button 
        @click="handleLogout"
        class="flex items-center gap-2 text-gray-400 hover:text-red-400 transition mb-4"
      >
        <span>🚪</span>
        <span>登出</span>
      </button>
    </div>

    <!-- Chat area -->
    <div class="flex-1 flex flex-col">

      <!-- header -->
      <div class="h-12 border-b border-gray-700 flex items-center px-4">
        <span class="font-bold"># ai-chat</span>
      </div>

      <!-- messages -->
      <div
        ref="chatBox"
        class="flex-1 overflow-y-auto p-4 space-y-4"
      >
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >

          <div
            class="max-w-[60%] px-3 py-2 rounded-lg"
            :class="msg.role === 'user'
              ? 'bg-blue-600'
              : 'bg-[#2b2d31]'"
          >
            <div class="text-sm">
              {{ msg.text }}
            </div>

            <div class="text-[10px] text-gray-300 mt-1 text-right">
              {{ msg.time }}
            </div>
          </div>

        </div>
      </div>

      <!-- input -->
      <div class="p-3 border-t border-gray-700 flex gap-2">
        <input
          v-model="input"
          @keyup.enter="sendMessage"
          placeholder="輸入訊息..."
          class="flex-1 bg-[#1e1f22] p-2 rounded text-white outline-none"
        />
        <button
          @click="sendMessage"
          class="bg-blue-600 px-4 rounded"
        >
          送出
        </button>
      </div>

    </div>
  </div>
</template>