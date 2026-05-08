<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const ws = ref(null);
const input = ref("");
const messages = ref([]);
const chatBox = ref(null);
const currentChannel = ref("general");

const token = localStorage.getItem("token");

const handleLogout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};

const fetchHistory = async (channel) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/history?channel=${channel}`);
    const history = await res.json();
    messages.value = history.map(m => ({
      role: m.user === 'User' ? 'user' : 'ai',
      text: m.message,
      time: new Date(m.time).toLocaleTimeString(),
    }));
    scrollBottom();
  } catch (e) {
    console.error("Fetch history error:", e);
  }
};

const connectWS = (channel) => {
  if (ws.value) {
    ws.value.close();
  }

  ws.value = new WebSocket(`ws://127.0.0.1:8000/ws/${channel}?token=${token}`);

  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // 如果是自己傳出的 User 訊息，其實在 sendMessage 已經 push 過了
    // 這裡我們只處理來自 AI 或其他人的訊息 (在這個簡單實作中)
    if (data.user === "AI" || (data.user === "User" && currentChannel.value === "general")) {
       // 為了簡單起見，如果是 general 頻道，我們會收到廣播
       // 但為了避免重複顯示自己的訊息，這裡加個簡單判斷
       // (實際專案通常會用 message ID 或 sender ID)
    }

    messages.value.push({
      role: data.user === "AI" ? "ai" : "user",
      text: data.message,
      time: new Date().toLocaleTimeString(),
    });

    scrollBottom();
  };
};

const switchChannel = (channel) => {
  currentChannel.value = channel;
};

// 監聽頻道切換
watch(currentChannel, (newChannel) => {
  messages.value = [];
  fetchHistory(newChannel);
  connectWS(newChannel);
}, { immediate: true });

onBeforeUnmount(() => {
  ws.value?.close();
});

const sendMessage = () => {
  if (!input.value.trim()) return;

  const msg = input.value;

  // 在 general 頻道，我們等 WS 廣播回來再顯示，避免重複
  // 在 ai-chat 頻道，我們手動 push User 訊息
  if (currentChannel.value === "ai-chat") {
    messages.value.push({
      role: "user",
      text: msg,
      time: new Date().toLocaleTimeString(),
    });
  }

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
        <div 
          @click="switchChannel('general')"
          :class="currentChannel === 'general' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-white'"
          class="cursor-pointer mb-2 p-2 rounded transition"
        >
          # general
        </div>
        <div 
          @click="switchChannel('ai-chat')"
          :class="currentChannel === 'ai-chat' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-white'"
          class="cursor-pointer p-2 rounded transition"
        >
          # ai-chat
        </div>
      </div>
      
      <!-- Logout Button -->
      <button 
        @click="handleLogout"
        class="flex items-center gap-2 text-gray-400 hover:text-red-400 transition mb-4 p-2"
      >
        <span>🚪</span>
        <span>登出</span>
      </button>
    </div>

    <!-- Chat area -->
    <div class="flex-1 flex flex-col">

      <!-- header -->
      <div class="h-12 border-b border-gray-700 flex items-center px-4">
        <span class="font-bold"># {{ currentChannel }}</span>
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
          :placeholder="`在 #${currentChannel} 輸入訊息...`"
          class="flex-1 bg-[#1e1f22] p-2 rounded text-white outline-none"
        />
        <button
          @click="sendMessage"
          class="bg-blue-600 px-4 rounded hover:bg-blue-500 transition"
        >
          送出
        </button>
      </div>

    </div>
  </div>
</template>
