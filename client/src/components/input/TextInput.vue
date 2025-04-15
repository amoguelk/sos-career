<script setup>
import { computed } from "vue";

const props = defineProps({
  name: { type: String, required: true },
  label: [String, null],
  placeholder: [String, null],
  type: {
    type: String,
    default: "text",
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  min: { type: [Number, null], default: null },
  extraRules: {
    type: Array,
    default: () => [],
  },
});
const model = defineModel();

const rules = computed(() => {
  const arr = [];
  if (props.required) arr.push((value) => !!value || "Field is required");
  if (props.min !== null)
    arr.push(
      (value) =>
        value.length >= props.min || `Must be at least ${props.min} characters`,
    );
  if (props.type === "email")
    arr.push((value) => {
      const pattern =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return pattern.test(value) || "Invalid e-mail.";
    });

  return arr;
});
</script>

<template>
  <div>
    <v-text-field
      :name="name"
      :label="label"
      :type="type"
      :placeholder="placeholder"
      v-model="model"
      :required="required"
      :disabled="disabled"
      :rules="[...rules, ...extraRules]"
    ></v-text-field>
  </div>
</template>
