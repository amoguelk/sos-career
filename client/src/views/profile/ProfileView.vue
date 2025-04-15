<script setup>
import { storeToRefs } from "pinia";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores";
import { getCurrentUser } from "@/services/users";
import { getCurrentProfile } from "@/services/profiles";
import UserForm from "./UserForm.vue";
import ProfileForm from "./ProfileForm.vue";

const authStore = useAuthStore();
const { isLoggedIn } = storeToRefs(authStore);

const isLoading = ref(true);
const user = ref(null);
const profile = ref(null);
const hasProfile = ref(true);

const handleLoad = () => {
  if (isLoggedIn) {
    isLoading.value = true;
    const userPromise = getCurrentUser();
    const profilePromise = getCurrentProfile();

    Promise.all([
      userPromise,
      profilePromise.catch((profileError) => {
        if (profileError.response.status !== 404) {
          console.error("🚩 Error getting profile", profileError);
          throw profileError;
        }
        hasProfile.value = false;
      }),
    ])
      .then((values) => {
        user.value = values[0]?.data ?? null;
        profile.value = values[1]?.data ?? null;
        isLoading.value = false;
        hasProfile.value = Boolean(values[1]?.data);
      })
      .catch((error) => {
        console.error("🚩 Error getting user or profile", error);
        isLoading.value = false;
      });
  }
};

onMounted(handleLoad);
</script>

<template>
  <v-container fluid fill-height class="d-flex align-center justify-center">
    <v-card class="py-8" width="50vw">
      <v-skeleton-loader
        v-if="isLoading"
        type="subtitle, paragraph, subtitle, paragraph"
        width="50vw"
      ></v-skeleton-loader>
      <v-card-text v-else>
        <UserForm
          :fullName="user?.full_name"
          :email="user?.email"
          :id="user?.id"
          :handle-reload="handleLoad"
        />
        <ProfileForm
          :interests="profile?.interests"
          :skills="profile?.skills"
          :educationLevel="profile?.education_level"
          :goals="profile?.goals"
          :userId="user?.id"
          :hasProfile="hasProfile"
          :handle-reload="handleLoad"
        />
      </v-card-text>
    </v-card>
  </v-container>
</template>
