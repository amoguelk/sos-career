<script setup>
import { RouterView, RouterLink } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores";

const authStore = useAuthStore();
const { isLoggedIn } = storeToRefs(authStore);
const { logoutAction } = authStore;
</script>

<template>
  <v-app>
    <v-app-bar :elevation="0" color="secondary">
      <v-app-bar-title class="text-h5"
        ><RouterLink class="text-decoration-none text-surface" to="/"
          >SOS! Career</RouterLink
        ></v-app-bar-title
      >
      <v-btn to="/">Home</v-btn>
      <v-btn to="/about">About</v-btn>
      <div v-if="isLoggedIn">
        <v-btn to="/profile">My profile</v-btn>
        <v-btn @click="logoutAction" variant="flat" class="mr-2">
          Log out
        </v-btn>
      </div>
      <div v-else>
        <v-btn to="/login" variant="flat" class="mr-2">Log in</v-btn>
        <v-btn to="/signup" variant="flat" class="mr-2">Sign up</v-btn>
      </div>
    </v-app-bar>
    <v-main class="d-flex">
      <RouterView />
    </v-main>
  </v-app>
</template>
