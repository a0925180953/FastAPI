import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Chat from "../views/Chat.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/chat", component: Chat, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from) => {
  const token = localStorage.getItem("token");

  // 需要登入但沒 token
  if (to.meta.requiresAuth && !token) {
    return "/login";
  }

  // 已登入還去 login → 導向 chat
  if (to.path === "/login" && token) {
    return "/chat";
  }

  // 放行
  return true;
});

export default router;