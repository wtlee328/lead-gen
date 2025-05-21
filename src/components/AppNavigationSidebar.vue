<!-- src/components/AppNavigationSidebar.vue -->
<template>
  <nav
    class="app-navigation-sidebar"
    :class="{ 'sidebar-collapsed': isSidebarCollapsed }"
    @mouseenter="handleSidebarMouseEnter"
    @mouseleave="handleSidebarMouseLeave"
  >
    <div class="logo-area">
      <img
        :src="isSidebarCollapsed ? '/Pwithdot.svg' : '/Prospecwithdot.svg'"
        alt="App Logo"
        class="app-logo"
        :class="{ 'app-logo-collapsed': isSidebarCollapsed }"
      />
    </div>
    <ul class="nav-links">
      <li class="nav-item">
        <router-link to="/" class="nav-link-item" :title="isSidebarCollapsed ? 'Prospects' : undefined">
          <i class="bi bi-people-fill"></i>
          <span class="nav-link-text">Prospects</span>
        </router-link>
      </li>

      <li class="nav-item">
        <div class="dropdown">
          <a
            ref="settingsDropdownToggleRef"
            href="#"
            class="nav-link-item"
            id="settingsDropdownMenuLink"
            data-bs-toggle="dropdown"
            data-bs-auto-close="outside"
            aria-expanded="false"
            role="button"
            :title="isSidebarCollapsed ? 'Settings' : undefined"
            @click.prevent
          >
            <i class="bi bi-gear-fill"></i>
            <span class="nav-link-text">Settings</span>
          </a>
          <ul
            class="dropdown-menu dropdown-menu-dark shadow"
            aria-labelledby="settingsDropdownMenuLink"
            style="min-width: 230px;"
          >
            <li><h6 class="dropdown-header">Language</h6></li>
            <li class="px-2 pb-1">
              <div class="btn-group w-100 language-toggle-group" role="group" aria-label="Language toggle">
                <button
                  type="button"
                  class="btn btn-sm language-toggle-btn"
                  :class="{ 'active': languageStore.currentLang === 'en' }"
                  @click="setLanguage('en')"
                  title="English"
                >
                  English
                </button>
                <button
                  type="button"
                  class="btn btn-sm language-toggle-btn"
                  :class="{ 'active': languageStore.currentLang === 'zh' }"
                  @click="setLanguage('zh')"
                  title="繁體中文"
                >
                  繁體中文
                </button>
              </div>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li><h6 class="dropdown-header">Theme</h6></li>
            <li class="px-2">
              <div class="btn-group w-100 theme-toggle-group" role="group" aria-label="Theme toggle">
                <button
                  type="button"
                  class="btn btn-sm theme-toggle-btn"
                  :class="{ 'active': currentThemePreference === 'light' }"
                  @click="setAppThemePreference('light')"
                  title="Light Theme"
                >
                  <i class="bi bi-sun-fill"></i>
                </button>
                <button
                  type="button"
                  class="btn btn-sm theme-toggle-btn"
                  :class="{ 'active': currentThemePreference === 'dark' }"
                  @click="setAppThemePreference('dark')"
                  title="Dark Theme"
                >
                  <i class="bi bi-moon-stars-fill"></i>
                </button>
                <button
                  type="button"
                  class="btn btn-sm theme-toggle-btn"
                  :class="{ 'active': currentThemePreference === 'system' }"
                  @click="setAppThemePreference('system')"
                  title="System Preference"
                >
                  <i class="bi bi-display-fill"></i>
                </button>
              </div>
            </li>
          </ul>
        </div>
      </li>
    </ul>

    <div class="user-profile-area">
      <div v-if="authStore.user" class="dropdown dropup w-100">
        <button
          class="btn user-profile-toggle d-flex align-items-center w-100"
          type="button"
          id="userActionsDropdown"
          data-bs-toggle="dropdown"
          aria-expanded="false"
          :title="isSidebarCollapsed && authStore.user ? authStore.user.email : 'User Actions'"
        >
          <i class="bi bi-person-circle me-2"></i>
          <span v-show="!isSidebarCollapsed" class="user-info-text">{{ authStore.user.email }}</span>
        </button>
        <ul
          class="dropdown-menu dropdown-menu-dark dropdown-menu-start"
          aria-labelledby="userActionsDropdown"
          style="min-width: max-content;"
        >
          <li>
            <button class="dropdown-item d-flex align-items-center" type="button" @click="goToUserSettingsPage">
              <i class="bi bi-person-gear me-2"></i><span>User Settings Page</span>
            </button>
          </li>
          <li>
            <button class="dropdown-item d-flex align-items-center" type="button" @click="handleSignOut">
              <i class="bi bi-box-arrow-right me-2"></i><span>Sign Out</span>
            </button>
          </li>
        </ul>
      </div>
      <div v-else-if="!authStore.isAuthenticated" class="p-2 text-center">
        <!-- Content for non-authenticated users, if any, in the sidebar profile area -->
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router'; // useRoute is not directly needed here
import { useAuthStore } from '@/stores/authStore';
import { useLanguageStore } from '@/stores/languageStore';
import { Dropdown } from 'bootstrap';

const authStore = useAuthStore();
const languageStore = useLanguageStore();
const router = useRouter();

const isSidebarCollapsed = ref(true);
const settingsDropdownToggleRef = ref<HTMLElement | null>(null);
let settingsDropdownInstance: Dropdown | null = null;

// Theme settings logic
type ThemePreference = 'light' | 'dark' | 'system';
const currentThemePreference = ref<ThemePreference>('system');
const THEME_PREFERENCE_STORAGE_KEY = 'app-theme-preference';

function getEffectiveTheme(preference: ThemePreference): 'light' | 'dark' {
  if (preference === 'light' || preference === 'dark') {
    return preference;
  }
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyThemeToDocument(effectiveTheme: 'light' | 'dark') {
  document.documentElement.dataset.bsTheme = effectiveTheme;
}

function setAppThemePreference(preference: ThemePreference) {
  currentThemePreference.value = preference;
  localStorage.setItem(THEME_PREFERENCE_STORAGE_KEY, preference);
  applyThemeToDocument(getEffectiveTheme(preference));
}

// Language settings logic
function setLanguage(lang: 'en' | 'zh') {
  languageStore.setLanguage(lang);
}

// User actions
async function handleSignOut() {
  await authStore.signOut();
  router.push({ name: 'Login' }).catch(err => {
    if (err.name !== 'NavigationDuplicated' && !err.message.includes('cancelled')) {
      console.error('Router push error during sign out:', err);
    }
  });
}

function goToUserSettingsPage() {
  router.push('/settings').catch(err => { // Ensure '/settings' route exists
    if (err.name !== 'NavigationDuplicated' && !err.message.includes('cancelled')) {
      console.error('Router push error to settings page:', err);
    }
  });
}

// Sidebar collapse/expand logic
function handleSidebarMouseEnter() {
  isSidebarCollapsed.value = false;
}

function handleSidebarMouseLeave() {
  isSidebarCollapsed.value = true;
  if (settingsDropdownInstance) {
    const menuElement = settingsDropdownToggleRef.value?.nextElementSibling;
    if (menuElement && menuElement.classList.contains('show')) {
      settingsDropdownInstance.hide();
    }
  }
}

// System theme change listener
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
const systemThemeChangeHandler = () => {
  if (currentThemePreference.value === 'system') {
    applyThemeToDocument(getEffectiveTheme('system'));
  }
};

onMounted(async () => {
  // Initialize theme
  const savedThemePreference = localStorage.getItem(THEME_PREFERENCE_STORAGE_KEY) as ThemePreference | null;
  if (savedThemePreference) {
    setAppThemePreference(savedThemePreference);
  } else {
    setAppThemePreference('system'); // Default to system preference
  }
  mediaQuery.addEventListener('change', systemThemeChangeHandler);

  // Initialize Bootstrap dropdown
  await nextTick();
  if (settingsDropdownToggleRef.value) {
    settingsDropdownInstance = Dropdown.getOrCreateInstance(settingsDropdownToggleRef.value);
  }
});

onUnmounted(() => {
  mediaQuery.removeEventListener('change', systemThemeChangeHandler);
  if (settingsDropdownInstance) {
    settingsDropdownInstance.dispose();
  }
});
</script>
