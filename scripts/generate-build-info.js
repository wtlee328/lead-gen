// scripts/generate-build-info.js
import fs from 'fs'; // Use ES module import if your Node version supports it and package.json has "type": "module"
import path from 'path';
import { fileURLToPath } from 'url';

// Get package.json version
// Since this script might be run directly by node and `package.json` has "type": "module",
// `require` might not be available directly for JSON if not careful with context.
// A more robust way is to read and parse it.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packageJsonPath = path.resolve(__dirname, '../package.json'); // Go up one level to project root
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
const appVersion = packageJson.version;

const buildTimestamp = new Date().getTime();

const buildInfo = {
  version: appVersion,
  buildTimestamp: buildTimestamp,
};

// Ensure the 'public' directory exists
const publicDir = path.resolve(__dirname, '../public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

const filePath = path.resolve(publicDir, 'build-info.json');

try {
  fs.writeFileSync(filePath, JSON.stringify(buildInfo, null, 2));
  console.log(`Build info generated successfully at ${filePath}`);
  console.log('Build Info:', buildInfo);
} catch (error) {
  console.error('Error generating build info:', error);
  process.exit(1); // Exit with error code if script fails
}