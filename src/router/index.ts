// src/router/index.ts
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import LeadGenFormView from '../views/LeadGenFormView.vue'; // Your main prospecting dashboard
import LoginView from '../views/LoginView.vue';         // Login page
import SignUpView from '../views/SignUpView.vue';       // Sign up page

// Import Supabase client for direct session check in the guard
import { supabase } from '@/services/supabaseClient';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'LeadProspecting', // Changed name to be more descriptive of the dashboard
        component: LeadGenFormView,
        meta: {
            requiresAuth: true,
            hideNavbar: false // MODIFIED: Explicitly set, though default would be false
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: {
            guestOnly: true, // This route is for guests (unauthenticated users) only
            hideNavbar: true   // ADDED: Hide navbar for this route
        }
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUpView,
        meta: {
            guestOnly: true, // This route is for guests only
            hideNavbar: true   // ADDED: Hide navbar for this route
        }
    },
    // Example of another protected route you might add later:
    // {
    //   path: '/my-profile',
    //   name: 'MyProfile',
    //   component: () => import('../views/UserProfileView.vue'), // Lazy loading
    //   meta: { requiresAuth: true, hideNavbar: false } // Navbar visible
    // },
    // Catch-all route for 404 Not Found (optional)
    // {
    //   path: '/:pathMatch(.*)*',
    //   name: 'NotFound',
    //   component: () => import('../views/NotFoundView.vue'), // Create a NotFoundView.vue
    //   meta: { hideNavbar: true } // Or false, depending on your 404 page design
    // }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL), // Uses HTML5 history mode
    routes, // short for `routes: routes`
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
    // Fetch the current session directly to ensure up-to-date auth state
    const { data: { session } } = await supabase.auth.getSession();
    const isAuthenticated = !!session; // True if session exists, false otherwise
    // console.log('AuthGuard: Navigating to', to.fullPath, 'IsAuthenticated:', isAuthenticated); // Keep for debugging if needed

    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const guestOnly = to.matched.some(record => record.meta.guestOnly);

    if (requiresAuth && !isAuthenticated) {
        // console.log('AuthGuard: Route requires auth, user NOT authenticated. Redirecting to /login.');
        next({ name: 'Login', query: { redirect: to.fullPath } });
    } else if (guestOnly && isAuthenticated) {
        // console.log('AuthGuard: Guest-only route, user IS authenticated. Redirecting to /.');
        next({ name: 'LeadProspecting' });
    } else {
        next();
    }
});

export default router;