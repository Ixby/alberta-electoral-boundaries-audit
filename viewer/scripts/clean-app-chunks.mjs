import { rmSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const appDir = resolve(__dirname, '../../docs/_app');

if (existsSync(appDir)) {
  rmSync(appDir, { recursive: true, force: true });
  console.log('Cleaned docs/_app/');
}
