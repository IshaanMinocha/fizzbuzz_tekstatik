
import { exec } from 'child_process';
import path from 'path';

export const runWfuzz = (url, flags) => {
    // resolve path to the Python script
    const pythonScriptPath = path.resolve('pyscripts/wfuzz_script.py');
    
    const command = `python3 ${pythonScriptPath} ${url} ${flags.join(' ')}`;
    
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
        console.log(`Fuzzing results:\n${stdout}`);
    });
};
