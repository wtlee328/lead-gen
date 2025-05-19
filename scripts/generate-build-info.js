// scripts/generate-build-info.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get package.json version
const packageJsonPath = path.resolve(__dirname, '../package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
const appVersion = packageJson.version;

const buildTimestamp = new Date().getTime().toString(); // Generate timestamp here

const buildInfo = {
  version: appVersion,
  buildTimestamp: buildTimestamp, // Use the generated timestamp
};

const publicDir = path.resolve(__dirname, '../public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

const filePath = path.resolve(publicDir, 'build-info.json');

try {
  fs.writeFileSync(filePath, JSON.stringify(buildInfo, null, 2));
  console.log(`Build info generated for /build-info.json:`, buildInfo);
} catch (error) {
  console.error('Error generating /build-info.json:', error);
  process.exit(1);
}