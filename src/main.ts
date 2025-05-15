// src/main.ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router'; // Your router with guards
import { useAuthStore } from '@/stores/authStore'; // Import your auth store

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
// Import Bootstrap Icons CSS
import 'bootstrap-icons/font/bootstrap-icons.css';
// Your global styles
import './style.css';

// 1. Create the Vue application instance
const app = createApp(App);

// 2. Create and use Pinia
const pinia = createPinia();
app.use(pinia);

// 3. Use the router
app.use(router);

// 4. Initialize authentication state BEFORE mounting the app
//    This ensures that when the app first loads, the auth state is checked,
//    and the onAuthStateChange listener is set up.
//    The router guards will also have a more reliable initial state to work with.
const authStore = useAuthStore(); // Get the auth store instance (Pinia must be installed first)

async function initializeApp() {
    try {
        // Attempt to initialize authentication (checks for existing session, sets up listener)
        await authStore.initializeAuth();
        console.log('Authentication initialized.');
    } catch (error) {
        console.error('Error during auth initialization in main.ts:', error);
        // You might want to handle this error more gracefully in a production app,
        // but for now, logging it is important. The app will still mount.
    } finally {
        // 5. Mount the application to the DOM
        // This should happen after critical async setup like auth initialization.
        app.mount('#app');
        console.log('Vue app mounted.');
    }
}

initializeApp(); // Call the async function to start the initialization and mounting process