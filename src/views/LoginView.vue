<template>
  <div class="landing-login-view">
    <header class="landing-header py-3 sticky-top">
      <div class="container d-flex justify-content-between align-items-center">
        <div class="logo-area-landing">
          <img src="@/assets/prospecwithdot.svg" alt="Prospecwithdot Logo" class="landing-logo-img" />
        </div>
        <div class="language-toggle" v-if="languageStore && texts">
          <button @click="languageStore.toggleLanguage" class="btn btn-sm btn-outline-secondary py-1 px-2">
            <small>{{ languageStore.langToggleText }}</small>
          </button>
        </div>
      </div>
    </header>

    <main class="landing-content container my-4 my-lg-5">
      <div class="row align-items-center g-lg-5 py-5">
        <!-- Product Info Column (remains the same) -->
        <div class="col-lg-7 text-center text-lg-start product-info-section mb-5 mb-lg-0">
          <h1 class="display-4 fw-bold lh-1 mb-3">{{ texts.landingHeadline || 'Supercharge Your Outreach with AI' }}</h1>
          <p class="col-lg-10 fs-5 lead mb-4">
            {{ texts.landingSubheadline || 'Discover, qualify, and engage prospects like never before. Prospec uses cutting-edge AI to find your ideal customers and personalize communication, saving you time and boosting conversions.' }}
          </p>
          <div class="features-list text-start mb-4 mx-auto mx-lg-0" style="max-width: 500px;">
            <h4 class="mb-3 text-center text-lg-start">{{ texts.landingFeaturesTitle || 'Why Choose Prospec?' }}</h4>
            <ul class="list-unstyled">
              <li class="d-flex align-items-start mb-2">
                <i class="bi bi-magic text-primary me-2 mt-1 fs-5"></i>
                <span><strong>{{ texts.landingFeature1Title || 'AI-Powered Prospecting:' }}</strong> {{ texts.landingFeature1Desc || 'Uncover hidden gems and high-intent leads.' }}</span>
              </li>
              <li class="d-flex align-items-start mb-2">
                <i class="bi bi-person-check-fill text-primary me-2 mt-1 fs-5"></i>
                <span><strong>{{ texts.landingFeature2Title || 'Intelligent Qualification:' }}</strong> {{ texts.landingFeature2Desc || 'Focus on leads that matter with smart scoring.' }}</span>
              </li>
              <li class="d-flex align-items-start mb-2">
                <i class="bi bi-envelope-paper-heart-fill text-primary me-2 mt-1 fs-5"></i>
                <span><strong>{{ texts.landingFeature3Title || 'Personalized Engagement:' }}</strong> {{ texts.landingFeature3Desc || 'Craft compelling outreach that resonates.' }}</span>
              </li>
               <li class="d-flex align-items-start">
                <i class="bi bi-graph-up-arrow text-primary me-2 mt-1 fs-5"></i>
                <span><strong>{{ texts.landingFeature4Title || 'Boost Conversions:' }}</strong> {{ texts.landingFeature4Desc || 'Turn more prospects into loyal customers.' }}</span>
              </li>
            </ul>
          </div>
          <div class="d-grid gap-2 d-lg-flex justify-content-lg-start">
            <router-link to="/signup" class="btn btn-primary btn-lg px-4 me-lg-2">{{ texts.signUpNowButton || 'Get Started Free' }}</router-link>
          </div>
        </div>

        <!-- Login Form Column -->
        <div class="col-lg-5 mx-auto">
          <div class="card shadow-lg login-card-wrapper">
            <div class="card-body p-4 p-md-5">
              <h3 class="card-title text-center fw-bold mb-4">{{ texts.loginTitle || 'Welcome Back!' }}</h3>

              <!-- Email/Password Form -->
              <form @submit.prevent="handleLogin" class="login-form-fields">
                <div class="mb-3">
                  <label for="loginEmail" class="form-label">{{ texts.emailLabel || 'Email Address' }}</label>
                  <input
                    type="email"
                    class="form-control form-control-lg"
                    id="loginEmail"
                    v-model="email"
                    required
                    :placeholder="texts.emailPlaceholder || 'you@example.com'"
                  >
                </div>
                <div class="mb-3">
                  <label for="loginPassword" class="form-label">{{ texts.passwordLabel || 'Password' }}</label>
                  <input
                    type="password"
                    class="form-control form-control-lg"
                    id="loginPassword"
                    v-model="password"
                    required
                    :placeholder="texts.passwordPlaceholder || 'Enter your password'"
                  >
                </div>
                <button
                  type="submit"
                  class="btn btn-primary w-100 btn-lg mt-4"
                  :disabled="authStore.loading"
                >
                  <span v-if="authStore.loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span>{{ texts.loginButton || 'Log In' }}</span>
                </button>
              </form>

              <!-- Social Login Section -->
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
                  <span>{{ texts.signInWithGoogleButton || 'Sign in with Google' }}</span>
                </button>
                <button
                  type="button"
                  class="btn btn-lg btn-outline-secondary social-login-btn linkedin-login-btn"
                  @click="handleLinkedInSignIn"
                  :disabled="authStore.loading"
                >
                  <i class="bi bi-linkedin me-2"></i>
                  <span>{{ texts.signInWithLinkedInButton || 'Sign in with LinkedIn' }}</span>
                </button>
              </div>

              <!-- Error and Signup Prompt -->
              <div v-if="authStore.error" class="alert alert-danger mt-4" role="alert">
                {{ authStore.error && (typeof authStore.error === 'string' ? authStore.error : authStore.error.message) || (texts.loginErrorDefault || 'An error occurred.') }}
              </div>
              <p class="mt-4 mb-0 text-center text-muted">
                <span>{{ texts.noAccountPrompt || "Don't have an account?" }}</span>
                <router-link to="/signup" class="fw-medium ms-1">{{ texts.signUpLink || 'Sign up here' }}</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="landing-footer text-center py-4">
      <div class="container">
        <p class="mb-0 text-muted small">© {{ new Date().getFullYear() }} Prospec. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useLanguageStore } from '@/stores/languageStore';

const authStore = useAuthStore();
const languageStore = useLanguageStore();

const texts = computed(() => {
  const defaultTexts = {
    productName: 'Prospec',
    landingHeadline: 'Supercharge Your Outreach with AI',
    landingSubheadline: 'Discover, qualify, and engage prospects like never before. Prospec uses cutting-edge AI to find your ideal customers and personalize communication, saving you time and boosting conversions.',
    landingFeaturesTitle: 'Why Choose Prospec?',
    landingFeature1Title: 'AI-Powered Prospecting:',
    landingFeature1Desc: 'Uncover hidden gems and high-intent leads.',
    landingFeature2Title: 'Intelligent Qualification:',
    landingFeature2Desc: 'Focus on leads that matter with smart scoring.',
    landingFeature3Title: 'Personalized Engagement:',
    landingFeature3Desc: 'Craft compelling outreach that resonates.',
    landingFeature4Title: 'Boost Conversions:',
    landingFeature4Desc: 'Turn more prospects into loyal customers.',
    signUpNowButton: 'Get Started Free',
    loginTitle: 'Welcome Back!',
    emailLabel: 'Email Address',
    passwordLabel: 'Password',
    loginButton: 'Log In',
    orDivider: 'OR', // NEW
    signInWithGoogleButton: 'Sign in with Google', // NEW
    signInWithLinkedInButton: 'Sign in with LinkedIn', // NEW
    noAccountPrompt: "Don't have an account?",
    signUpLink: 'Sign up here',
    emailPlaceholder: 'you@example.com',
    passwordPlaceholder: 'Enter your password',
    loginErrorDefault: 'An unknown error occurred during login.',
    errorRequired: (fields: string) => `${fields} are required.`,
  };
  if (languageStore && languageStore.texts) {
    return { ...defaultTexts, ...languageStore.texts };
  }
  return defaultTexts;
});

const email = ref('');
const password = ref('');

const handleLogin = async () => {
  if (!email.value || !password.value) {
    authStore.error = { name: 'ValidationError', message: texts.value.errorRequired ? texts.value.errorRequired('Email and Password') : 'Email and Password are required.' };
    return;
  }
  await authStore.signIn(email.value, password.value);
};

// --- NEW Social Sign-In Methods ---
const handleGoogleSignIn = async () => {
  // Ensure the redirect URL is correctly configured in your Supabase Auth settings
  // (typically your app's base URL, e.g., https://lead-gen-vwb1.vercel.app/)
  // And that Google provider is enabled in Supabase.
  await authStore.signInWithOAuth('google');
};

const handleLinkedInSignIn = async () => {
  // Ensure the redirect URL is correctly configured in your Supabase Auth settings
  // And that LinkedIn OIDC provider is enabled in Supabase.
  await authStore.signInWithOAuth('linkedin_oidc'); // Use 'linkedin_oidc' for LinkedIn
};
// --- END NEW Social Sign-In Methods ---

</script>