<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <h1>Not Found</h1>
  <div style="display: flex; flex-direction: column; align-items: center">
    <p>This page does not exist</p>
    <RouterLink to="/">Go home</RouterLink>
  </div>
</template>
