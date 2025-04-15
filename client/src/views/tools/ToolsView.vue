<script setup lang="ts">
import NavButton from "@/components/nav/NavButton.vue";
import { RouterView } from "vue-router";
</script>

<template>
  <v-app-bar :elevation="0" class="align-center">
    <NavButton to="/tool/career-path">Create career path</NavButton>
    <NavButton to="/tool/job-insight">Investigate job insights</NavButton>
    <NavButton to="/tool/roadmap">Create roadmap</NavButton>
  </v-app-bar>
  <v-main class="d-flex">
    <RouterView />
  </v-main>
</template>
