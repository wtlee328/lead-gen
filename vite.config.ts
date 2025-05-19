// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path'; // Already imported
import fs from 'fs';   // Import the 'fs' module from Node.js

// Helper function to read the version from package.json
const getAppVersion = () => {
  try {
    // Assuming vite.config.ts is in the project root alongside package.json
    const packageJson = JSON.parse(fs.readFileSync(path.resolve(__dirname, 'package.json'), 'utf-8'));
    return packageJson.version;
  } catch (error) {
    console.error("Failed to read app version from package.json:", error);
    return '0.0.0'; // Fallback version in case of an error
  }
};

const appVersion = getAppVersion();
const buildTimestamp = new Date().getTime().toString(); // Get current timestamp as string

// https://vitejs.dev/config/
export default defineConfig(() => { // Add mode if you plan to use loadEnv, otherwise it's optional
  // If you need to load other .env files:
  // const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'), // Set '@' to point to the 'src' directory
      },
    },
    // Define global constants for client-side code
    // These will be statically replaced during build
    define: {
      'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion),
      'import.meta.env.VITE_APP_BUILD_TIMESTAMP': JSON.stringify(buildTimestamp),
    },
  };
});