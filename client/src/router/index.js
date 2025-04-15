import { createRouter, createWebHistory } from "vue-router";
import { HomeView, AboutView } from "@/views/home";
import { ProfileView } from "@/views/profile";
import { LoginView, SignUpView, LogoutView } from "@/views/auth";
import {
  CareerPathView,
  JobInsightView,
  RoadmapView,
  ToolsView,
} from "@/views/tools";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: "/about",
    name: "About",
    component: AboutView,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: "/profile",
    name: "MyProfile",
    component: ProfileView,
    meta: {
      allowAnonymous: false,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    meta: {
      allowAnonymous: true,
    },
    props: true,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUpView,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: "/logout",
    name: "Logout",
    component: LogoutView,
    meta: {
      allowAnonymous: true,
    },
  },
  {
    path: "/tool",
    name: "ToolHome",
    component: ToolsView,
    meta: {
      allowAnonymous: false,
    },
    children: [
      {
        path: "career-path",
        name: "CareerPath",
        component: CareerPathView,
      },
      {
        path: "job-insight",
        name: "JobInsight",
        component: JobInsightView,
      },
      {
        path: "roadmap",
        name: "Roadmap",
        component: RoadmapView,
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/views/NotFoundView.vue"),
    meta: {
      allowAnonymous: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = JSON.parse(localStorage.getItem("access_token"));
  if (!to.meta.allowAnonymous && !token) {
    next({
      path: "/login",
    });
  } else next();
});

export default router;
