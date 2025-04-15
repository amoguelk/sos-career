import { createRouter, createWebHistory } from "vue-router";
import { HomeView, AboutView } from "@/views/home";
import { ProfileView } from "@/views/profile";
import { LoginView, SignUpView, LogoutView } from "@/views/auth";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "About",
    component: AboutView,
  },
  {
    path: "/profile",
    name: "MyProfile",
    component: ProfileView,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    props: true,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUpView,
  },
  {
    path: "/logout",
    name: "Logout",
    component: LogoutView,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/views/NotFoundView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
