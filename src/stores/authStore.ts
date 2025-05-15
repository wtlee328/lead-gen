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
                        router.push(redirectPath);
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
                await router.push(redirectPath);
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

    // --- MODIFIED signOut ACTION ---
    const signOut = async () => {
        loading.value = true;
        error.value = null;
        // const currentSessionForArchive = session.value; // Capture session before it's cleared by signOut

        // It's better to get a fresh session token specifically for this call,
        // as the one in store might be just about to be invalidated by signOut() itself.
        // However, supabase.functions.invoke automatically uses the current client's auth header.
        // The key is that the user IS STILL AUTHENTICATED when this invoke call is made.

        if (isAuthenticated.value) { // Check if user is authenticated before trying to call the function
            console.log('AuthStore: Attempting to archive new leads before sign out for user:', user.value?.id);
            try {
                const { data: archiveResult, error: archiveError } = await supabase.functions.invoke(
                    'archive-new-leads-on-logout', // Your Edge Function name
                    {
                        // No body is needed if the Edge Function gets the user_id from the JWT context
                        // The Authorization header with the user's JWT is automatically included by
                        // the Supabase client when invoking a function if the user is authenticated.
                    }
                );

                if (archiveError) {
                    // Log this error but don't let it block the sign-out process
                    console.error('AuthStore: Error invoking archive-new-leads-on-logout Edge Function:', archiveError.message, archiveResult);
                    // You might want to set a non-critical error message here for the user if needed
                } else {
                    console.log('AuthStore: archive-new-leads-on-logout Edge Function invoked successfully:', archiveResult);
                }
            } catch (e: any) {
                // Catch any unexpected errors during the function invocation
                console.error('AuthStore: Exception while invoking archive-new-leads-on-logout:', e.message);
            }
        } else {
            console.warn('AuthStore: User not authenticated, skipping archive new leads call on sign out.');
        }

        // Now, proceed with the actual Supabase sign out
        try {
            const { error: signOutError } = await supabase.auth.signOut();
            if (signOutError) {
                // This error is more critical for the sign-out process itself
                throw signOutError;
            }
            // user.value and session.value will be set to null by onAuthStateChange,
            // and onAuthStateChange will also handle the redirect to /login.
            console.log('AuthStore: Supabase signOut call successful.');
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
        signOut,
    };
});