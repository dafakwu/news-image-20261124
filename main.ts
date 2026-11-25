// Copy the image that ships beside this script into the requested output folder.
import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptFolder = dirname(fileURLToPath(import.meta.url));
const outputFolder = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destination = join(outputFolder, 'entry.png');

mkdirSync(outputFolder, { recursive: true });
copyFileSync(join(scriptFolder, 'entry.png'), destination);
console.log(`Copied entry.png (${statSync(destination).size} bytes) to ${destination}`);
