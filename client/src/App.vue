<script setup>
import { RouterView, RouterLink } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores";
import NavButton from "@/components/nav/NavButton.vue";

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
      <NavButton to="/">Home</NavButton>
      <!-- <NavButton to="/about">About</NavButton> -->
      <div v-if="isLoggedIn">
        <NavButton to="/profile">My profile</NavButton>
        <NavButton to="/tool">AI tool</NavButton>
        <NavButton @click="logoutAction" is-highlighted> Log out </NavButton>
      </div>
      <div v-else>
        <NavButton to="/login" is-highlighted>Log in</NavButton>
        <NavButton to="/signup" is-highlighted>Sign up</NavButton>
      </div>
    </v-app-bar>
    <v-main class="d-flex">
      <RouterView />
    </v-main>
  </v-app>
</template>
