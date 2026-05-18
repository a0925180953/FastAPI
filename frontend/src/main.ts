import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
import { logRemote } from "./api/api";

const app = createApp(App);

// 捕捉 Vue 元件錯誤
app.config.errorHandler = (err: any) => {
  console.error("Vue Error:", err);
  logRemote("error", `[Vue] ${err.message}`, err.stack);
};

// 捕捉非同步錯誤 (例如 Promise reject)
window.addEventListener("unhandledrejection", (event) => {
  console.error("Unhandled Promise Rejection:", event.reason);
  logRemote("error", `[Promise] ${event.reason?.message || event.reason}`, event.reason?.stack);
});

app.use(router).mount("#app");