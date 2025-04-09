<script setup>
import { RouterView } from "vue-router";
</script>

<template>
  <v-app>
    <v-app-bar :elevation="0" color="secondary">
      <v-app-bar-title class="text-h5">SOS! Career</v-app-bar-title>
      <v-btn to="/">Home</v-btn>
      <v-btn to="/about">About</v-btn>
      <v-btn to="/login" variant="flat">Log in</v-btn>
    </v-app-bar>
    <v-main class="d-flex">
      <RouterView />
    </v-main>
  </v-app>
</template>
