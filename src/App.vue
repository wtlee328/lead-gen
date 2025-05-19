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
        <p class="mb-2 small">{{ texts.updateAvailableMessage }}</p> <!-- Relies on 'texts' computed -->
        <button @click="applyUpdate" class="btn btn-sm btn-primary w-100">
          <i class="bi bi-arrow-clockwise me-1"></i>
          {{ texts.refreshNowButton }} <!-- Relies on 'texts' computed -->
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

console.log('APP.VUE SCRIPT SETUP - EXECUTING (Updated CheckLogic)');

const route = useRoute();

const clientAppVersion = import.meta.env.VITE_APP_VERSION;
const clientBuildTimestamp = import.meta.env.VITE_APP_BUILD_TIMESTAMP;

console.log('App.vue setup: CLIENT APP VERSION:', clientAppVersion);
console.log('App.vue setup: CLIENT BUILD TIMESTAMP:', clientBuildTimestamp);

const updateAvailable = ref(false);

const languageStore = useLanguageStore();
const texts = computed(() => {
  // Ensure your languageStore and types/language.ts have these keys
  const defaults = {
    updateAvailableMessage: 'A new version of the application is available.',
    refreshNowButton: 'Refresh Now'
  };
  if (languageStore && typeof languageStore.texts === 'object' && languageStore.texts !== null) {
    // Ensure all keys in defaults are also in languageStore.texts or handle missing keys gracefully
    return { ...defaults, ...languageStore.texts };
  }
  return defaults;
});
// This log is useful to see if texts resolved correctly BEFORE the blank screen (if any)
console.log('App.vue setup: texts computed. Default message:', texts.value.updateAvailableMessage);


async function checkForUpdates() {
  // Skip in development to avoid HMR triggering it constantly
  if (import.meta.env.DEV) {
    // console.log('Update check skipped in development mode.');
    return;
  }

  try {
    // Fetch with cache-busting query parameter
    const response = await fetch(`/build-info.json?cacheBust=${new Date().getTime()}`);

    if (response.ok) {
      const serverBuildInfo = await response.json();

      console.log('Update Check - Client App Version:', clientAppVersion, 'Client Build TS:', clientBuildTimestamp);
      console.log('Update Check - Server /build-info.json Version:', serverBuildInfo.version, 'Server Build TS:', serverBuildInfo.buildTimestamp);

      let newVersionIsAvailable = false;

      // *** PRIMARY CHECK: VERSION STRING ***
      if (clientAppVersion && serverBuildInfo.version && clientAppVersion !== serverBuildInfo.version) {
        // For a more robust SemVer comparison, you might use a library,
        // but for now, any difference in version string triggers the update.
        console.warn(`VERSION MISMATCH! Client: ${clientAppVersion}, Server: ${serverBuildInfo.version}. Prompting update.`);
        newVersionIsAvailable = true;
      }
      // *** SECONDARY/FALLBACK CHECK: TIMESTAMP (ONLY IF VERSIONS ARE IDENTICAL) ***
      // This helps catch new builds of the *same version* (e.g., hotfixes, content changes).
      // Crucially, it only flags an update if the server's build timestamp is *strictly newer*.
      else if (
        clientAppVersion && serverBuildInfo.version && clientAppVersion === serverBuildInfo.version && // Versions must match
        clientBuildTimestamp && serverBuildInfo.buildTimestamp &&                                   // Both timestamps must exist
        BigInt(serverBuildInfo.buildTimestamp) > BigInt(clientBuildTimestamp)                        // Server timestamp must be newer
      ) {
        console.warn(`SAME VERSION (${clientAppVersion}) but newer server build timestamp detected. Client TS: ${clientBuildTimestamp}, Server TS: ${serverBuildInfo.buildTimestamp}. Prompting update.`);
        newVersionIsAvailable = true;
      }

      // Update the reactive ref based on the check
      if (newVersionIsAvailable) {
        updateAvailable.value = true;
      } else {
        // console.log('Application is up to date, or client has a timestamp that is not older than server for the same version.');
        updateAvailable.value = false; // Ensure it's reset if no update needed
      }

    } else {
      console.error('Failed to fetch build-info.json:', response.status, response.statusText);
      updateAvailable.value = false; // Assume no update if we can't check
    }
  } catch (error) {
    console.error('Error checking for application updates:', error);
    updateAvailable.value = false; // Assume no update on error
  }
}

function applyUpdate() {
  window.location.reload(); // Simple reload. For hard refresh: window.location.reload(true)
}

onMounted(() => {
  console.log('App.vue onMounted: Component has mounted.');
  checkForUpdates(); // Initial check
  setInterval(checkForUpdates, 15 * 60 * 1000); // Periodically check every 15 minutes
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      console.log('App.vue: Tab became visible, checking for updates.');
      checkForUpdates(); // Check when tab regains focus
    }
  });
});
</script>