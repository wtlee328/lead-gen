// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import fs from 'fs';

const getAppVersion = () => {
  try {
    const packageJson = JSON.parse(fs.readFileSync(path.resolve(__dirname, 'package.json'), 'utf-8'));
    return packageJson.version;
  } catch (error) {
    console.error("Failed to read app version from package.json:", error);
    return '0.0.0';
  }
};

const appVersion = getAppVersion();
// This timestamp is for when Vite config is processed, will be embedded in client JS
const clientBuildTimestamp = new Date().getTime().toString(); 
console.log(`vite.config.ts: Embedding VITE_APP_VERSION=${appVersion}, VITE_APP_BUILD_TIMESTAMP=${clientBuildTimestamp}`);

export default defineConfig(() => {
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    define: {
      'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion),
      'import.meta.env.VITE_APP_BUILD_TIMESTAMP': JSON.stringify(clientBuildTimestamp)
    },
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
    },
  };
});