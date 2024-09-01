import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// console.log(path.join(__dirname, '../../pyscripts/wfuzz_script.py'))

export const runWfuzz = (url, flags) => {
    const pythonScriptPath = path.join(__dirname, '../../pyscripts/wfuzz_script.py');

    const command = `python "${pythonScriptPath}" ${url} ${flags.join(' ')}`; //win
    // const command = `python3 ${pythonScriptPath} ${url} ${flags.join(' ')}`; //mac

    console.log(`Running command: ${command}`);

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing wfuzz: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error: ${stderr}`);
            return;
        }
        console.log(`Fuzzing results in JSON format:\n${stdout}`);
    });
};
