<script setup>
import { editUser } from "@/services/users";
import { ref, computed } from "vue";

const props = defineProps({
  fullName: String,
  email: String,
  id: Number,
  handleReload: Function,
});

const userRef = ref({
  fullName: props.fullName ?? "",
  email: props.email ?? "",
});
const isSaving = ref(false);
const isEdited = computed(() => {
  return Object.keys(userRef.value).some((key) => {
    if (userRef.value[key] !== props[key]) return true;
    return false;
  });
});
const isValid = computed(() => {
  return userRef.value.fullName.length > 0 && userRef.value.email.length > 0;
});

const handleSaveUser = () => {
  if (props.id && isValid && isEdited) {
    isSaving.value = true;
    editUser(props.id, {
      email: userRef.value.email,
      full_name: userRef.value.fullName,
    })
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
    <h4 class="text-h4 mb-2">Account information</h4>
    <v-btn
      :loading="isSaving"
      color="primary"
      :disabled="!isEdited || !isValid || !id"
      @click="handleSaveUser()"
      >Save</v-btn
    >
  </div>
  <v-text-field
    name="name"
    label="Name"
    type="text"
    required
    v-model="userRef.fullName"
  ></v-text-field>
  <v-text-field
    name="email"
    label="Email"
    type="email"
    v-model="userRef.email"
    required
    disabled
  ></v-text-field>
</template>
