// src/stores/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { supabase } from '@/services/supabaseClient';
import type { User, Session, AuthError, AuthChangeEvent } from '@supabase/supabase-js';
import router from '@/router'; // Import router for navigation FROM WITHIN THE STORE

export const useAuthStore = defineStore('auth', () => {
    // --- STATE ---
    const user = ref<User | null>(null);
    const session = ref<Session | null>(null);
    const loading = ref(false); // For UI feedback during auth operations
    const error = ref<AuthError | { name: string; message: string } | null>(null);

    // --- GETTERS ---
    const isAuthenticated = computed(() => !!user.value && !!session.value);

    // --- ACTIONS ---

    const initializeAuth = async () => {
        console.log('AuthStore: Initializing auth...');
        loading.value = true;
        error.value = null;
        try {
            const { data: { session: activeSession }, error: sessionError } = await supabase.auth.getSession();
            if (sessionError) {
                console.error("AuthStore: Error getting initial session:", sessionError.message);
                error.value = sessionError;
            } else {
                session.value = activeSession;
                user.value = activeSession?.user ?? null;
                console.log('AuthStore: Initial session loaded:', activeSession ? 'Session found' : 'No session');
            }
        } catch (e: any) {
            console.error("AuthStore: Catch block error during initial session fetch:", e.message);
            error.value = { name: "InitializationError", message: e.message };
        } finally {
            loading.value = false;
        }

        // --- onAuthStateChange listener (already handles routing after sign-in/out) ---
        supabase.auth.onAuthStateChange((event: AuthChangeEvent, activeSession: Session | null) => {
            console.log('AuthStore: Auth state changed:', event, activeSession ? 'Session present' : 'No session');
            session.value = activeSession;
            user.value = activeSession?.user ?? null;

            if (event === 'SIGNED_OUT') {
                console.log('AuthStore: User signed out, redirecting to /login.');
                router.push({ name: 'Login' });
            } else if (event === 'SIGNED_IN' || (event === 'INITIAL_SESSION' && activeSession) || (event === 'TOKEN_REFRESHED' && activeSession)) {
                console.log('AuthStore: User signed in or session refreshed.');
                if (router.currentRoute.value.meta.guestOnly && user.value) {
                    console.log('AuthStore: User is on a guest-only page, redirecting.');
                    const redirectPath = router.currentRoute.value.query.redirect as string | undefined;
                    if (redirectPath) {
                        // Check if redirectPath is an absolute URL or relative path
                        // If it's an absolute URL, ensure it's on your domain to prevent open redirect vulnerabilities
                        const isAbsolute = redirectPath.startsWith('http://') || redirectPath.startsWith('https://');
                        const isSameOrigin = isAbsolute ? new URL(redirectPath).origin === window.location.origin : true;

                        if (isAbsolute && !isSameOrigin) {
                            console.warn('AuthStore: Redirect to external origin detected, redirecting to LeadProspecting instead.');
                            router.push({ name: 'LeadProspecting' });
                        } else {
                            router.push(redirectPath);
                        }
                    } else {
                        router.push({ name: 'LeadProspecting' }); // Your main dashboard route name
                    }
                }
            }
        });
    };

    const signUp = async (emailInput: string, passwordInput: string) => {
        loading.value = true;
        error.value = null;
        try {
            const { data, error: signUpError } = await supabase.auth.signUp({
                email: emailInput,
                password: passwordInput,
            });
            if (signUpError) throw signUpError;
            console.log('AuthStore: Sign up successful data:', data);
            return data;
        } catch (e: any) {
            console.error("AuthStore: Sign up error:", e.message);
            error.value = { name: e.name || "SignUpError", message: e.message };
            return null;
        } finally {
            loading.value = false;
        }
    };

    const signIn = async (emailInput: string, passwordInput: string) => {
        loading.value = true;
        error.value = null;
        try {
            const { data, error: signInError } = await supabase.auth.signInWithPassword({
                email: emailInput,
                password: passwordInput,
            });
            if (signInError) throw signInError;
            console.log('AuthStore: Sign in successful:', data.user);
            const redirectPath = router.currentRoute.value.query.redirect as string | undefined;
            if (redirectPath) {
                console.log('AuthStore: Redirecting to originally intended path:', redirectPath);
                const isAbsolute = redirectPath.startsWith('http://') || redirectPath.startsWith('https://');
                const isSameOrigin = isAbsolute ? new URL(redirectPath).origin === window.location.origin : true;

                if (isAbsolute && !isSameOrigin) {
                    console.warn('AuthStore: Redirect to external origin detected, redirecting to LeadProspecting instead.');
                    await router.push({ name: 'LeadProspecting' });
                } else {
                    await router.push(redirectPath);
                }
            } else {
                console.log('AuthStore: Redirecting to dashboard (LeadProspecting).');
                await router.push({ name: 'LeadProspecting' }); // Your main dashboard route name
            }
            return data;
        } catch (e: any) {
            console.error("AuthStore: Sign in error:", e.message);
            error.value = { name: e.name || "SignInError", message: e.message };
            return null;
        } finally {
            loading.value = false;
        }
    };

    // --- NEW: signInWithOAuth action ---
    const signInWithOAuth = async (provider: 'google' | 'linkedin_oidc') => {
        loading.value = true;
        error.value = null;
        try {
            const { data, error: oauthError } = await supabase.auth.signInWithOAuth({
                provider: provider,
                options: {
                    // Supabase will redirect to this URL after successful authentication with the provider.
                    // This URL must be configured in your Supabase Dashboard -> Authentication -> URL Configuration
                    // under "Site URL" and "Redirect URLs".
                    redirectTo: window.location.origin, // Dynamically redirects back to your app's current origin
                },
            });

            if (oauthError) {
                error.value = oauthError;
                console.error(`AuthStore: OAuth sign-in error with ${provider}:`, oauthError);
            } else {
                // For OAuth, data.url will contain the URL to redirect the user to the provider's login page.
                // Supabase.js handles this redirect automatically if `data.url` is present.
                // The user state will then be updated by the onAuthStateChange listener when they are redirected back.
                console.log(`AuthStore: Redirecting to ${provider} for sign-in...`, data);
            }
        } catch (e: any) {
            // Catch any unexpected client-side errors during the process
            error.value = { name: e.name || "OAuthError", message: e.message || `An unexpected OAuth sign-in error occurred with ${provider}.` };
            console.error(`AuthStore: Unexpected OAuth sign-in error with ${provider}:`, e);
        } finally {
            // Note: In case of a successful OAuth redirect, this `finally` block might not be fully executed
            // before the browser leaves the page. It's more relevant for immediate errors.
            loading.value = false;
        }
    };
    // --- END NEW: signInWithOAuth action ---


    const signOut = async () => {
        loading.value = true;
        error.value = null;

        if (isAuthenticated.value && user.value?.id) { // Ensure user is authenticated and has an ID
            console.log('AuthStore: Attempting to archive new leads before sign out for user:', user.value.id);
            try {
                const { data: archiveResult, error: archiveError } = await supabase.functions.invoke(
                    'archive-new-leads-on-logout', // Your Edge Function name
                    {
                        // No body is needed if the Edge Function gets the user_id from the JWT context
                    }
                );

                if (archiveError) {
                    console.error('AuthStore: Error invoking archive-new-leads-on-logout Edge Function:', archiveError.message, archiveResult);
                } else {
                    console.log('AuthStore: archive-new-leads-on-logout Edge Function invoked successfully:', archiveResult);
                }
            } catch (e: any) {
                console.error('AuthStore: Exception while invoking archive-new-leads-on-logout:', e.message);
            }
        } else {
            console.warn('AuthStore: User not authenticated or ID missing, skipping archive new leads call on sign out.');
        }

        try {
            const { error: signOutError } = await supabase.auth.signOut();
            if (signOutError) {
                throw signOutError;
            }
            console.log('AuthStore: Supabase signOut call successful.');
            // user.value and session.value will be set to null by onAuthStateChange,
            // and onAuthStateChange will also handle the redirect to /login.
        } catch (e: any) {
            console.error("AuthStore: Supabase signOut call error:", e.message);
            error.value = { name: e.name || "SignOutError", message: e.message };
        } finally {
            loading.value = false;
        }
    };

    return {
        user,
        session,
        loading,
        error,
        isAuthenticated,
        initializeAuth,
        signUp,
        signIn,
        signInWithOAuth, // Make the new action available
        signOut,
    };
});