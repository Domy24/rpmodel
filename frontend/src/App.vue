<template>
  <NavbarComponent/>
  <Toast />
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 font-sans">
    <RouterView/>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "App",
  components: {NavbarComponent},
  created() {
    this.$authStore.initializeAuthStore();
  }
}
</script>