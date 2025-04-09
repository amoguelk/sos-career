<script setup>
import { login } from "@/services/auth";
import { ref } from "vue";

const username = ref("");
const password = ref("");

const handleLogin = async () => {
  const params = new URLSearchParams();
  params.append("username", username.value);
  params.append("password", password.value);
  try {
    const response = await login(params);
    console.log("🪲 response:", response);
  } catch (error) {
    console.error("🚩 ", error);
  }
};
</script>

<template>
  <v-container fluid fill-height class="d-flex align-center justify-center">
    <v-card class="text-center py-8" width="50vw">
      <v-card-text>
        <form ref="form" @submit.prevent="handleLogin()">
          <v-text-field
            v-model="username"
            name="username"
            label="Username"
            type="text"
            placeholder="Username"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            name="password"
            label="Password"
            type="password"
            placeholder="Password"
            required
          ></v-text-field>
          <v-btn type="submit" class="mt-4" color="primary" value="log in"
            >Login</v-btn
          >
        </form>
      </v-card-text>
    </v-card>
  </v-container>
</template>
