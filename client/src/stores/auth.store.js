import { defineStore } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/services/users";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(JSON.parse(localStorage.getItem("access_token")));
  const isLoggedIn = ref(token.value !== null);
  const router = useRouter();

  const loginAction = async (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);
    const { data } = await login(params);
    token.value = data.access_token;
    isLoggedIn.value = true;
    localStorage.setItem("access_token", JSON.stringify(data.access_token));
    router.push({ name: "Home" });
  };

  const logoutAction = async () => {
    token.value = null;
    isLoggedIn.value = null;
    localStorage.removeItem("access_token");
    router.push({ name: "Logout" });
  };

  return { token, isLoggedIn, loginAction, logoutAction };
});
