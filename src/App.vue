<!-- src/App.vue-->
<template>
  <div class="app-layout-wrapper">
    <!-- Conditionally render the new navigation sidebar component -->
    <AppNavigationSidebar v-if="!route.meta.hideNavbar" />

    <div class="app-main-content-area" :class="{ 'full-width': route.meta.hideNavbar }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import AppNavigationSidebar from '@/components/AppNavigationSidebar.vue'; // Import the new component

const route = useRoute(); // To access route.meta for conditional rendering
</script>

<!-- No <style> tag needed here if all styles are global or in AppNavigationSidebar.vue's global styles -->
<!-- The .app-layout-wrapper and .app-main-content-area styles should be in your global.css -->