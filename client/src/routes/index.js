import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import BpmPage from "../views/BpmPage.vue";
import QuestionsPage from "../views/QuestionsPage.vue";
import MusicPage from "../views/MusicPage.vue";
import ErrorPage from "../views/ErrorPage.vue";

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
  {
    path: "/questions",
    name: "Question",
    component: QuestionsPage,
  },
  {
    path: "/music",
    name: "Music",
    component: MusicPage,
  },
  {
    path: "/:catchAll(.*)",
    name: "Error",
    component: ErrorPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
