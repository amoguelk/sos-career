<script setup>
defineProps({
  to: String,
  click: {
    type: Function,
    default: () => {},
  },
  isHighlighted: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <v-btn
    @click="click"
    :to="to"
    :variant="isHighlighted ? 'flat' : 'text'"
    class="mr-2"
  >
    <slot></slot>
  </v-btn>
</template>
