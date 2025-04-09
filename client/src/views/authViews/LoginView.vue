<script setup>
import { useAuthStore } from "@/stores";
import { ref } from "vue";

const username = ref("");
const password = ref("");
const hasError = ref(false);

const handleLogin = async () => {
  hasError.value = false;
  const store = useAuthStore();

  store.loginAction(username.value, password.value).catch((error) => {
    console.error("🚩", error);
    if (error.response.status === 401) hasError.value = true;
  });
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
          <div class="d-flex flex-column align-center">
            <v-chip
              prepend-icon="mdi-alert-circle"
              color="error"
              v-show="hasError"
              >Incorrect username or password</v-chip
            >
            <v-btn type="submit" class="mt-4" color="primary" value="log in"
              >Login</v-btn
            >
          </div>
        </form>
      </v-card-text>
    </v-card>
  </v-container>
</template>
