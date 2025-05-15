<template>
  <div class="signup-view"> <!-- Removed container here for full-width background if desired -->
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="row w-100" style="max-width: 450px;"> <!-- Slightly wider for more fields -->
        <div class="col-12">
          <div class="card shadow-lg">
            <div class="card-body p-4 p-sm-5">
              <div class="language-toggle text-end mb-3" v-if="languageStore && texts">
                  <button @click="languageStore.toggleLanguage" class="btn btn-sm btn-outline-secondary py-1 px-2">
                      <small>{{ languageStore.langToggleText }}</small>
                  </button>
              </div>
              <h3 class="card-title text-center fw-bold mb-4">{{ texts.signUpTitle || 'Create Account' }}</h3>
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
                <div class="mb-4"> <!-- Increased margin bottom -->
                  <label for="confirmPassword" class="form-label">{{ texts.confirmPasswordLabel || 'Confirm Password' }}</label>
                  <input
                    type="password"
                    class="form-control form-control-lg"
                    id="confirmPassword"
                    v-model="confirmPassword"
                    required
                    :placeholder="texts.confirmPasswordPlaceholder || 'Confirm your password'"
                  > <!-- Moved comment here, or remove it -->
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
import router from '@/router'; // Needed for router.push('/')

const authStore = useAuthStore();
const languageStore = useLanguageStore();

// More robust computed for texts with proper fallback structure
const texts = computed(() => {
  const defaultTexts = {
    signUpTitle: 'Create Account',
    emailLabel: 'Email Address',
    passwordLabel: 'Password',
    confirmPasswordLabel: 'Confirm Password',
    signUpButton: 'Sign Up',
    alreadyAccountPrompt: 'Already have an account?',
    loginLink: 'Log In',
    emailPlaceholder: 'Enter your email',
    passwordPlaceholder: 'Create a password',
    confirmPasswordPlaceholder: 'Confirm your password',
    passwordMismatchError: 'Passwords do not match.',
    signUpSuccessConfirmEmail: 'Sign up successful! Please check your email for a confirmation link.',
    generalSignUpError: 'An error occurred during sign up. Please try again.',
    // Add other keys from your language.ts Translations interface if needed as fallback
    errorRequired: (fieldName: string) => `${fieldName} is required.`, // Fallback for errorRequired
  };
  if (languageStore && languageStore.texts) {
    return { ...defaultTexts, ...languageStore.texts };
  }
  console.warn("SignUpView: languageStore.texts not available, using fallback texts.");
  return defaultTexts;
});

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const signUpMessage = ref<string | null>(null); // For success/info messages specifically from sign-up process

const handleSignUp = async () => {
  // Clear previous messages
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

  const result = await authStore.signUp(email.value, password.value);

  if (result && result.user) {
    // User object exists, sign up was successful with Supabase
    if (result.session) {
      // Session also exists, meaning user is immediately logged in (e.g., email confirmation disabled)
      router.push('/'); // Navigate to dashboard
    } else {
      // No session, but user object exists: Email confirmation likely required
      signUpMessage.value = texts.value.signUpSuccessConfirmEmail;
      // Clear form for good UX after successful submission awaiting confirmation
      email.value = '';
      password.value = '';
      confirmPassword.value = '';
    }
  } else if (!authStore.error) {
    // This case means authStore.signUp didn't throw an error captured by its try/catch,
    // but also didn't return a user (which is unusual for Supabase signUp).
    // Set a generic error message.
    authStore.error = { name: 'SignUpFailed', message: texts.value.generalSignUpError };
  }
  // If authStore.signUp itself set an error (e.g., email already taken), it will be displayed by `v-if="authStore.error"`
};

// Ensure these keys are in your language.ts:
// signUpTitle, emailLabel, passwordLabel, confirmPasswordLabel, signUpButton,
// alreadyAccountPrompt, loginLink, emailPlaceholder, passwordPlaceholder, confirmPasswordPlaceholder,
// passwordMismatchError, signUpSuccessConfirmEmail, generalSignUpError
</script>

<style scoped>
/* signup-view can be empty if global body styles and container centering is enough */
/* .signup-view {} */

.card {
  border: none;
}

.language-toggle button {
    font-size: 0.8rem;
}

.btn .spinner-border {
    vertical-align: middle;
}
</style>