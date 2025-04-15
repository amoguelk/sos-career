<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import TextInput from "@/components/input/TextInput.vue";
import { useAuthStore } from "@/stores";

const email = ref("");
const password = ref("");
const hasError = ref(false);

const route = useRoute();

const handleLogin = async () => {
  hasError.value = false;
  const store = useAuthStore();

  store.loginAction(email.value, password.value).catch((error) => {
    console.error("🚩", error);
    if (error.response.status === 401) hasError.value = true;
  });
};
</script>

<template>
  <v-container fluid fill-height class="d-flex align-center justify-center">
    <v-card class="py-8" width="50vw">
      <v-card-text>
        <v-chip color="success" class="mb-4" v-show="route.query.newUser">
          Please log in to your brand new account
        </v-chip>
        <form ref="form" @submit.prevent="handleLogin()">
          <TextInput
            v-model="email"
            name="email"
            label="Email"
            type="text"
            placeholder="Email"
            required
          />

          <TextInput
            v-model="password"
            name="password"
            label="Password"
            type="password"
            placeholder="Password"
            required
          />
          <div class="d-flex flex-column align-center">
            <v-chip
              prepend-icon="mdi-alert-circle"
              color="error"
              v-show="hasError"
            >
              Incorrect email or password
            </v-chip>
            <v-btn type="submit" class="mt-4" color="primary" value="log in">
              Login
            </v-btn>
          </div>
        </form>
      </v-card-text>
    </v-card>
  </v-container>
</template>
