// Alberta Electoral Boundary Audit — clean-app-chunks prebuild script
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
import { rmSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const appDir = resolve(__dirname, '../../docs/_app');

if (existsSync(appDir)) {
  rmSync(appDir, { recursive: true, force: true });
  console.log('Cleaned docs/_app/');
}
