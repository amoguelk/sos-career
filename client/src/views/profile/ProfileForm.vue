<script setup>
import { ref, computed } from "vue";
import { editProfile, createProfile } from "@/services/profiles";

const props = defineProps({
  interests: String,
  skills: String,
  educationLevel: String,
  goals: String,
  userId: Number,
  hasProfile: Boolean,
  handleReload: Function,
});

const profileRef = ref({
  interests: props.interests ?? "",
  skills: props.skills ?? "",
  educationLevel: props.educationLevel ?? "",
  goals: props.goals ?? "",
});
const isSaving = ref(false);
const isEdited = computed(() => {
  return Object.keys(profileRef.value).some((key) => {
    if (profileRef.value[key] !== props[key]) return true;
    return false;
  });
});

const handleSaveProfile = () => {
  if (props.userId && isEdited) {
    isSaving.value = true;
    const data = {
      interests: profileRef.value.interests,
      skills: profileRef.value.skills,
      goals: profileRef.value.goals,
      education_level: profileRef.value.educationLevel,
    };
    const service = props.hasProfile
      ? editProfile(props.userId, data)
      : createProfile(data);
    service
      .then(() => {
        isSaving.value = false;
        props.handleReload?.();
      })
      .catch((error) => {
        console.error("🚩", error);
        isSaving.value = false;
      });
  }
};
</script>

<template>
  <div class="d-flex justify-space-between">
    <h4 class="text-h4 mb-2">Profile information</h4>
    <v-btn
      color="primary"
      :loading="isSaving"
      :disabled="!userId || !isEdited"
      @click="handleSaveProfile()"
      >Save</v-btn
    >
  </div>
  <v-text-field
    name="interests"
    label="Interests"
    type="text"
    v-model="profileRef.interests"
  ></v-text-field>
  <v-text-field
    name="skills"
    label="Skills"
    type="text"
    v-model="profileRef.skills"
  ></v-text-field>
  <v-text-field
    name="educationLevel"
    label="Education level"
    type="text"
    v-model="profileRef.educationLevel"
  ></v-text-field>
  <v-text-field
    name="goals"
    label="Goals"
    type="text"
    v-model="profileRef.goals"
  ></v-text-field>
</template>
