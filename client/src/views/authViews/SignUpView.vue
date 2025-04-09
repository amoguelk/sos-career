<script setup>
import { createUser } from "@/services/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const passwordVerify = ref("");
const hasError = ref(false);
const errorText = ref("");

const router = useRouter();

const handleLogin = async () => {
  hasError.value = false;
  if (password.value.length < 8) {
    hasError.value = true;
    errorText.value = "Password must be at least 8 characters long";
    return;
  }

  if (password.value !== passwordVerify.value) {
    hasError.value = true;
    errorText.value = "Passwords don't match";
    return;
  }

  createUser({
    email: email.value,
    full_name: name.value,
    plain_password: password.value,
  })
    .then(() => {
      router.push({ name: "Login", query: { newUser: true } });
    })
    .catch((error) => {
      console.error("🚩", error);
      if (error.response.status === 400) {
        hasError.value = true;
        errorText.value = "An account with that email already exists";
      }
    });
};
</script>

<template>
  <v-container fluid fill-height class="d-flex align-center justify-center">
    <v-card class="text-center py-8" width="50vw">
      <v-card-text>
        <form ref="form" @submit.prevent="handleLogin()">
          <v-text-field
            v-model="name"
            name="name"
            label="Your name"
            type="text"
            placeholder="John Doe"
            required
          ></v-text-field>

          <v-text-field
            v-model="email"
            name="email"
            label="Email"
            type="email"
            placeholder="jdoe@email.com"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            name="password"
            label="Password"
            type="password"
            required
          ></v-text-field>

          <v-text-field
            v-model="passwordVerify"
            name="passwordVerify"
            label="Verify password"
            type="password"
            required
          ></v-text-field>
          <div class="d-flex flex-column align-center">
            <v-chip
              prepend-icon="mdi-alert-circle"
              color="error"
              v-show="hasError"
              >{{ errorText }}</v-chip
            >
            <v-btn type="submit" class="mt-4" color="primary" value="log in"
              >Sign Up</v-btn
            >
          </div>
        </form>
      </v-card-text>
    </v-card>
  </v-container>
</template>
