<template>
  <div class="signup-view">
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="row w-100" style="max-width: 450px;">
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-body p-4 p-sm-5">
              <div class="language-toggle text-end mb-3" v-if="languageStore && texts">
                  <button @click="languageStore.toggleLanguage" class="btn btn-sm btn-outline-secondary py-1 px-2">
                      <small>{{ languageStore.langToggleText }}</small>
                  </button>
              </div>
              <h3 class="card-title text-center fw-bold mb-4">{{ texts.signUpTitle || 'Create Account' }}</h3>

              <!-- Email/Password Sign Up Form -->
              <form @submit.prevent="handleSignUp">
                <div class="mb-3">
                  <label for="signUpEmail" class="form-label">{{ texts.emailLabel || 'Email Address' }}</label>
                  <input
                    type="email"
                    class="form-control form-control-lg"
                    id="signUpEmail"
                    v-model="email"
                    required
                    :placeholder="texts.emailPlaceholder || 'Enter your email'"
                  >
                </div>
                <div class="mb-3">
                  <label for="signUpPassword" class="form-label">{{ texts.passwordLabel || 'Password' }}</label>
                  <input
                    type="password"
                    class="form-control form-control-lg"
                    id="signUpPassword"
                    v-model="password"
                    required
                    :placeholder="texts.passwordPlaceholder || 'Create a password'"
                  >
                </div>
                <div class="mb-4">
                  <label for="confirmPassword" class="form-label">{{ texts.confirmPasswordLabel || 'Confirm Password' }}</label>
                  <input
                    type="password"
                    class="form-control form-control-lg"
                    id="confirmPassword"
                    v-model="confirmPassword"
                    required
                    :placeholder="texts.confirmPasswordPlaceholder || 'Confirm your password'"
                  >
                </div>
                <button
                  type="submit"
                  class="btn btn-primary w-100 btn-lg"
                  :disabled="authStore.loading"
                >
                  <span v-if="authStore.loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span>{{ texts.signUpButton || 'Sign Up' }}</span>
                </button>
              </form>

              <!-- Social Sign Up Section -->
              <div class="d-flex align-items-center my-4">
                <hr class="flex-grow-1">
                <span class="px-3 text-muted">{{ texts.orDivider || 'OR' }}</span>
                <hr class="flex-grow-1">
              </div>

              <div class="d-grid gap-3">
                <button
                  type="button"
                  class="btn btn-lg btn-outline-secondary social-login-btn google-login-btn"
                  @click="handleGoogleSignIn"
                  :disabled="authStore.loading"
                >
                  <i class="bi bi-google me-2"></i>
                  <span>{{ texts.signInWithGoogleButton || 'Sign up with Google' }}</span>
                </button>
                <button
                  type="button"
                  class="btn btn-lg btn-outline-secondary social-login-btn linkedin-login-btn"
                  @click="handleLinkedInSignIn"
                  :disabled="authStore.loading"
                >
                  <i class="bi bi-linkedin me-2"></i>
                  <span>{{ texts.signInWithLinkedInButton || 'Sign up with LinkedIn' }}</span>
                </button>
              </div>

              <!-- Messages and Login Prompt -->
              <div v-if="signUpMessage" class="alert alert-info mt-4" role="alert">
                {{ signUpMessage }}
              </div>
              <div v-if="authStore.error" class="alert alert-danger mt-4" role="alert">
                {{ authStore.error && (typeof authStore.error === 'string' ? authStore.error : authStore.error.message) || (texts.generalSignUpError || 'An error occurred during sign up.') }}
              </div>
              <p class="mt-4 mb-0 text-center text-muted">
                <span>{{ texts.alreadyAccountPrompt || "Already have an account?" }}</span>
                <router-link to="/login" class="fw-medium ms-1">{{ texts.loginLink || 'Log In' }}</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useLanguageStore } from '@/stores/languageStore';
import router from '@/router';

const authStore = useAuthStore();
const languageStore = useLanguageStore();

const texts = computed(() => {
  const defaultTexts = {
    signUpTitle: 'Create Account',
    emailLabel: 'Email Address',
    passwordLabel: 'Password',
    confirmPasswordLabel: 'Confirm Password',
    signUpButton: 'Sign Up',
    orDivider: 'OR', // Re-use from LoginView
    signInWithGoogleButton: 'Sign up with Google', // Adapted for signup
    signInWithLinkedInButton: 'Sign up with LinkedIn', // Adapted for signup
    alreadyAccountPrompt: 'Already have an account?',
    loginLink: 'Log In',
    emailPlaceholder: 'Enter your email',
    passwordPlaceholder: 'Create a password',
    confirmPasswordPlaceholder: 'Confirm your password',
    passwordMismatchError: 'Passwords do not match.',
    signUpSuccessConfirmEmail: 'Sign up successful! Please check your email for a confirmation link.',
    generalSignUpError: 'An error occurred during sign up. Please try again.',
    errorRequired: (fieldName: string) => `${fieldName} is required.`,
  };
  if (languageStore && languageStore.texts) {
    return { ...defaultTexts, ...languageStore.texts };
  }
  return defaultTexts;
});

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const signUpMessage = ref<string | null>(null);

const handleSignUp = async () => {
  authStore.error = null;
  signUpMessage.value = null;

  if (!email.value || !password.value || !confirmPassword.value) {
    authStore.error = { name: 'ValidationError', message: texts.value.errorRequired ? texts.value.errorRequired('All fields') : 'All fields are required.' };
    return;
  }

  if (password.value !== confirmPassword.value) {
    authStore.error = { name: 'PasswordMismatch', message: texts.value.passwordMismatchError };
    return;
  }

  // Use the signUp method from your authStore
  const result = await authStore.signUp(email.value, password.value);

  if (result && result.user) {
    if (result.session) {
      router.push('/');
    } else {
      signUpMessage.value = texts.value.signUpSuccessConfirmEmail;
      email.value = '';
      password.value = '';
      confirmPassword.value = '';
    }
  } else if (!authStore.error) {
    authStore.error = { name: 'SignUpFailed', message: texts.value.generalSignUpError };
  }
};

// --- NEW Social Sign-Up Methods ---
const handleGoogleSignIn = async () => {
  // Use the signInWithOAuth method from your authStore
  // Ensure the redirect URLs are configured in Supabase.
  await authStore.signInWithOAuth('google');
};

const handleLinkedInSignIn = async () => {
  // Use the signInWithOAuth method from your authStore
  // Ensure the redirect URLs are configured in Supabase.
  await authStore.signInWithOAuth('linkedin_oidc');
};
// --- END NEW Social Sign-Up Methods ---

</script>