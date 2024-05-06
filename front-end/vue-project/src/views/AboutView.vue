<template>
  <div class="about">
    <InputComponent />
  </div>
</template>
<script setup>
import InputComponent from '../components/Input.vue'
</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
