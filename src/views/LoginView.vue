<template>
  <div class="landing-login-view">
    <header class="landing-header py-3 sticky-top">
      <div class="container d-flex justify-content-between align-items-center">
        <div class="logo-area-landing">
          <img src="@/assets/Prospecwithdot.svg" alt="Prospecwithdot Logo" class="landing-logo-img" />
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
        <!-- Product Info Column -->
        <div class="col-lg-7 text-center text-lg-start product-info-section mb-5 mb-lg-0">
          <h1 class="display-4 fw-bold lh-1 mb-3">{{ texts.landingHeadline || 'Supercharge Your Outreach with AI' }}</h1>
          <p class="col-lg-10 fs-5 lead mb-4">
            {{ texts.landingSubheadline || 'Discover, qualify, and engage prospects like never before. Prospec uses cutting-edge AI to find your ideal customers and personalize communication, saving you time and boosting conversions.' }}
          </p>
          <div class="features-list text-start mb-4 mx-auto mx-lg-0" style="max-width: 500px;">
            <h4 class="mb-3 text-center text-lg-start">{{ texts.landingFeaturesTitle || 'Why Choose Prospec?' }}</h4>

            <!-- Feature Ticker Wrapper -->
            <div class="feature-ticker-wrapper">
              <Transition name="feature-slide" mode="out-in">
                <div :key="currentFeatureIndex" class="feature-ticker-item d-flex align-items-start">
                  <i :class="['text-primary me-2 mt-1 fs-5', currentFeature.icon]"></i>
                  <span>
                    <strong>{{ currentFeature.title || '' }}</strong> {{ currentFeature.desc || '' }}
                  </span>
                </div>
              </Transition>
            </div>
            <!-- End Feature Ticker Wrapper -->

          </div>
          <div class="d-grid gap-2 d-lg-flex justify-content-lg-start">
            <router-link to="/signup" class="btn btn-primary btn-lg px-4 me-lg-2">{{ texts.signUpNowButton || 'Get Started Free' }}</router-link>
          </div>
        </div>

        <!-- Login Form Column -->
        <div class="col-lg-5 mx-auto">
          <div class="card shadow-lg login-card-wrapper rounded-4">
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
                  <!-- Corrected Google 'G' logo SVG from Google's Identity Services documentation -->
                  <svg
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 48 48"
                    class="google-icon me-2"
                    width="20" height="20"
                    style="vertical-align: middle;"
                  >
                    <g>
                      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                      <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                      <path fill="none" d="M0 0h48v48H0z"/>
                    </g>
                  </svg>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useLanguageStore } from '@/stores/languageStore';

const authStore = useAuthStore();
const languageStore = useLanguageStore();

// Reactive properties for email and password input
const email = ref('');
const password = ref('');

// Computed property for localized texts
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
    orDivider: 'OR',
    signInWithGoogleButton: 'Sign in with Google',
    signInWithLinkedInButton: 'Sign in with LinkedIn',
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

// --- Feature Ticker Logic ---
const featuresList = computed(() => [
  { icon: 'bi-magic', title: texts.value.landingFeature1Title, desc: texts.value.landingFeature1Desc },
  { icon: 'bi-person-check-fill', title: texts.value.landingFeature2Title, desc: texts.value.landingFeature2Desc },
  { icon: 'bi-envelope-paper-heart-fill', title: texts.value.landingFeature3Title, desc: texts.value.landingFeature3Desc },
  { icon: 'bi-graph-up-arrow', title: texts.value.landingFeature4Title, desc: texts.value.landingFeature4Desc },
]);

const currentFeatureIndex = ref(0);
let tickerInterval: number | null = null; // Use `let` for reassignment with `null`

onMounted(() => {
  // Start the ticker animation when the component mounts
  tickerInterval = window.setInterval(() => {
    currentFeatureIndex.value = (currentFeatureIndex.value + 1) % featuresList.value.length;
  }, 4000); // Change feature every 4 seconds
});

onUnmounted(() => {
  // Clear the interval when the component is unmounted to prevent memory leaks
  if (tickerInterval !== null) { // Check if interval was set
    clearInterval(tickerInterval);
  }
});

const currentFeature = computed(() => featuresList.value[currentFeatureIndex.value]);
// --- End Feature Ticker Logic ---


const handleLogin = async () => {
  if (!email.value || !password.value) {
    authStore.error = { name: 'ValidationError', message: texts.value.errorRequired ? texts.value.errorRequired('Email and Password') : 'Email and Password are required.' };
    return;
  }
  await authStore.signIn(email.value, password.value);
};

const handleGoogleSignIn = async () => {
  await authStore.signInWithOAuth('google');
};

const handleLinkedInSignIn = async () => {
  await authStore.signInWithOAuth('linkedin_oidc');
};
</script>