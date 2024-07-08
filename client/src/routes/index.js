import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import BpmPage from "../views/BpmPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/bpm",
    name: "BPM",
    component: BpmPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
