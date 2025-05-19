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

    <!-- Update Notification -->
    <div v-if="updateAvailable" class="update-notification card shadow-sm">
      <div class="card-body">
        <p class="mb-2 small">{{ texts.updateAvailableMessage || 'A new version of the application is available.' }}</p>
        <button @click="applyUpdate" class="btn btn-sm btn-primary w-100">
          <i class="bi bi-arrow-clockwise me-1"></i>
          {{ texts.refreshNowButton || 'Refresh Now' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import AppNavigationSidebar from '@/components/AppNavigationSidebar.vue';
import { onMounted, ref, computed } from 'vue';
import { useLanguageStore } from '@/stores/languageStore';

// Log immediately when the script setup runs
console.log('APP.VUE SCRIPT SETUP - EXECUTING'); // General log to see if setup runs

const route = useRoute();

const clientAppVersion = import.meta.env.VITE_APP_VERSION;
const clientBuildTimestamp = import.meta.env.VITE_APP_BUILD_TIMESTAMP;

// Log the values after they are assigned
console.log('App.vue setup: CLIENT APP VERSION:', clientAppVersion);
console.log('App.vue setup: CLIENT BUILD TIMESTAMP:', clientBuildTimestamp);

const updateAvailable = ref(false);

const languageStore = useLanguageStore();
const texts = computed(() => {
  const defaults = {
    updateAvailableMessage: 'A new version of the application is available.',
    refreshNowButton: 'Refresh Now'
  };
  return { ...defaults, ...languageStore.texts };
});

async function checkForUpdates() {
  if (import.meta.env.DEV) {
    // console.log('Update check skipped in dev.'); // Optional: uncomment if you want this log in dev
    return;
  }
  try {
    const response = await fetch(`/build-info.json?t=${new Date().getTime()}`);
    if (response.ok) {
      const serverBuildInfo = await response.json();
      if (
        (serverBuildInfo.version && clientAppVersion && serverBuildInfo.version !== clientAppVersion) ||
        (serverBuildInfo.buildTimestamp && clientBuildTimestamp && serverBuildInfo.buildTimestamp.toString() !== clientBuildTimestamp.toString())
      ) {
        console.log('New version detected! Client Build Timestamp:', clientBuildTimestamp, 'Server Build Timestamp:', serverBuildInfo.buildTimestamp);
        updateAvailable.value = true;
      } else {
        // console.log('App is up to date. Client TS:', clientBuildTimestamp, 'Server TS:', serverBuildInfo.buildTimestamp);
        updateAvailable.value = false;
      }
    } else {
      console.error('Failed to fetch build-info.json:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error checking for application updates:', error);
  }
}

function applyUpdate() {
  window.location.reload(); // Changed from reload(true)
}

onMounted(() => {
  console.log('App.vue onMounted: Component has mounted.'); // General onMounted log
  // You can also log them here if you prefer, or if you need to ensure they are accessed after define has definitely run
  // console.log('App.vue onMounted: CLIENT APP VERSION (confirm):', import.meta.env.VITE_APP_VERSION);
  // console.log('App.vue onMounted: CLIENT BUILD TIMESTAMP (confirm):', import.meta.env.VITE_APP_BUILD_TIMESTAMP);

  checkForUpdates();
  setInterval(checkForUpdates, 15 * 60 * 1000);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      checkForUpdates();
    }
  });
});
</script>