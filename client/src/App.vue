<script setup>
import { RouterView } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores";

const authStore = useAuthStore();
const { isLoggedIn } = storeToRefs(authStore);
const { logoutAction } = authStore;
</script>

<template>
  <v-app>
    <v-app-bar :elevation="0" color="secondary">
      <v-app-bar-title class="text-h5">SOS! Career</v-app-bar-title>
      <v-btn to="/">Home</v-btn>
      <v-btn to="/about">About</v-btn>
      <v-btn @click="logoutAction" variant="flat" v-if="isLoggedIn">
        Log out
      </v-btn>
      <v-btn to="/login" variant="flat" v-else>Log in</v-btn>
    </v-app-bar>
    <v-main class="d-flex">
      <RouterView />
    </v-main>
  </v-app>
</template>
