// Authored Node 22 launcher for the standard-library Python forecaster.
import { spawnSync } from 'node:child_process';
const result = spawnSync('python3', ['-P', '-s', new URL('./main.py', import.meta.url).pathname], { stdio: 'inherit' });
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);
