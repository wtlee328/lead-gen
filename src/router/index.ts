// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router'; // Correct type-only import

import LeadGenFormView from '../views/LeadGenFormView.vue';
import LoginView from '../views/LoginView.vue';
import SignUpView from '../views/SignUpView.vue';
import EngagementCenterView from '../views/EngagementCenterView.vue'; // 1. IMPORT THE NEW VIEW

// Import Supabase client for direct session check in the guard
import { supabase } from '@/services/supabaseClient';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'LeadProspecting',
        component: LeadGenFormView,
        meta: {
            requiresAuth: true,
            hideNavbar: false
        }
    },
    // 2. ADD THE NEW ROUTE DEFINITION
    {
        path: '/engagement-hub', // Or your preferred path
        name: 'EngagementHub',    // Choose a unique name for the route
        component: EngagementCenterView,
        meta: {
            requiresAuth: true, // This view likely requires authentication
            hideNavbar: false   // The main app navbar should be visible
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: {
            guestOnly: true,
            hideNavbar: true
        }
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUpView,
        meta: {
            guestOnly: true,
            hideNavbar: true
        }
    },
    // Example of a settings route (if you have one from AppNavigationSidebar)
    {
      path: '/settings',
      name: 'UserSettings', // Make sure this name is unique
      // component: () => import('../views/UserSettingsView.vue'), // Lazy load if it's a separate view
      component: LeadGenFormView, // TEMPORARY: Point to an existing view if UserSettingsView doesn't exist yet
      meta: { requiresAuth: true, hideNavbar: false }
    },
    // Catch-all route for 404 Not Found (optional but recommended)
    // {
    //   path: '/:pathMatch(.*)*',
    //   name: 'NotFound',
    //   component: () => import('../views/NotFoundView.vue'), // Create a NotFoundView.vue
    //   meta: { hideNavbar: true } // Or false, or a specific layout for 404
    // }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

// Navigation Guard
router.beforeEach(async (to, _from, next) => { // _from to indicate it's intentionally unused
    const { data: { session } } = await supabase.auth.getSession();
    const isAuthenticated = !!session;

    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const guestOnly = to.matched.some(record => record.meta.guestOnly);

    if (requiresAuth && !isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } });
    } else if (guestOnly && isAuthenticated) {
        next({ name: 'LeadProspecting' }); // Or your main authenticated dashboard route
    } else {
        next();
    }
});

export default router;