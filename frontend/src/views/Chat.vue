<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js";
import "highlight.js/styles/github-dark.css";

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) {}
    }
    return ""; // use external default escaping
  },
});

const router = useRouter();
const ws = ref(null);
const input = ref("");
const messages = ref([]);
const chatBox = ref(null);
const currentChannel = ref("general");
const typingUsers = ref(new Set());
let typingTimeout = null;

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
      role: m.user === 'AI' ? 'ai' : 'user',
      user: m.user,
      nickname: m.nickname,
      avatar: m.avatar,
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
    
    if (data.type === "typing") {
      if (data.is_typing) {
        typingUsers.value.add(data.user);
      } else {
        typingUsers.value.delete(data.user);
      }
      return;
    }

    if (data.type === "message") {
      // 獲取目前使用者的 username (簡單起見從 localStorage 或解析 token，這裡假設我們知道自己是誰)
      // 但其實只要判斷 data.user 即可
      
      messages.value.push({
        role: data.user === "AI" ? "ai" : "user",
        user: data.user,
        nickname: data.nickname,
        avatar: data.avatar,
        text: data.message,
        time: new Date().toLocaleTimeString(),
      });

      scrollBottom();
    }
  };
};

const switchChannel = (channel) => {
  currentChannel.value = channel;
  typingUsers.value.clear();
};

// 監聽頻道切換
watch(currentChannel, (newChannel) => {
  messages.value = [];
  fetchHistory(newChannel);
  connectWS(newChannel);
}, { immediate: true });

// 監聽輸入框以發送正在輸入狀態
watch(input, (newVal) => {
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    if (newVal.length > 0) {
      ws.value.send(JSON.stringify({ type: "typing", is_typing: true }));
      
      if (typingTimeout) clearTimeout(typingTimeout);
      typingTimeout = setTimeout(() => {
        ws.value.send(JSON.stringify({ type: "typing", is_typing: false }));
      }, 2000);
    }
  }
});

onBeforeUnmount(() => {
  ws.value?.close();
  if (typingTimeout) clearTimeout(typingTimeout);
});

const sendMessage = () => {
  if (!input.value.trim()) return;

  const msg = input.value;

  ws.value.send(JSON.stringify({ type: "message", message: msg }));
  
  // 立即停止輸入狀態
  if (typingTimeout) clearTimeout(typingTimeout);
  ws.value.send(JSON.stringify({ type: "typing", is_typing: false }));

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
      <div class="flex flex-col gap-1">
        <button 
          @click="router.push('/settings')"
          class="flex items-center gap-2 text-gray-400 hover:text-white transition p-2"
        >
          <span>⚙️</span>
          <span>設定</span>
        </button>
        <button 
          @click="handleLogout"
          class="flex items-center gap-2 text-gray-400 hover:text-red-400 transition mb-4 p-2"
        >
          <span>🚪</span>
          <span>登出</span>
        </button>
      </div>
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
        class="flex-1 overflow-y-auto p-4 space-y-6"
      >
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="flex items-start gap-3"
        >
          <!-- Avatar -->
          <img 
            :src="msg.avatar" 
            alt="avatar" 
            class="w-10 h-10 rounded-full object-cover bg-gray-600 mt-1"
          />

          <div class="flex-1 min-w-0">
            <!-- Header: Nickname + Time -->
            <div class="flex items-baseline gap-2 mb-1">
              <span class="font-bold text-blue-400">{{ msg.nickname }}</span>
              <span class="text-[10px] text-gray-500">{{ msg.time }}</span>
            </div>

            <!-- Content bubble -->
            <div
              class="max-w-[90%] px-3 py-2 rounded-lg"
              :class="msg.role === 'ai' ? 'bg-[#2b2d31]' : 'bg-[#383a40]'"
            >
              <!-- 使用 markdown 解析內容 -->
              <div class="prose prose-invert prose-sm max-w-none" v-html="md.render(msg.text)">
              </div>
            </div>
          </div>

        </div>

        <!-- Typing Indicator -->
        <div v-if="typingUsers.size > 0" class="flex justify-start">
          <div class="text-xs text-gray-400 italic bg-[#2b2d31] px-3 py-1 rounded-full animate-pulse">
            {{ Array.from(typingUsers).join(', ') }} 正在輸入中...
          </div>
        </div>
      </div>

      <!-- input -->
      <div class="p-3 border-t border-gray-700 flex flex-col gap-2">
        <div class="flex gap-2">
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
  </div>
</template>

<style>
/* 針對 Markdown 代碼區塊的額外樣式 */
.prose pre {
  background-color: #1e1f22 !important;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}
.prose code {
  color: #e2e8f0;
  background-color: transparent;
  padding: 0;
}
.prose p {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
