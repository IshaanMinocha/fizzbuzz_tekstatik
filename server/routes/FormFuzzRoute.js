import express from 'express';
import { exec } from 'child_process';
import { promisify } from 'util';

const router = express.Router();
const execPromise = promisify(exec);
// const payloadFilePath = "/mnt/c/Users/Ishaan Minocha/Desktop/sih24/fizzbuzz/payloads/payload-form.txt";
const payloadFilePath = "/mnt/c/Users/acer/Desktop/Projects/fizzbuzz_tekstatic/payloads/payload-form.txt";

// code to parse stdout to return proper json output
const parseWfuzzOutput = (output) => {
    const lines = output.split('\n').map(line => line.trim()).filter(line => line);
    const results = [];
    let processing = false;
    for (const line of lines) {
      if (line.startsWith('ID')) {
        processing = true;
        continue;
      }
      if (line.startsWith('Total time')) {
        processing = false;
        continue;
      }
      if (processing) {
        const cleanLine = line.replace(/\x1b\[[0-9;]*m/g, '');
        const parts = cleanLine.split(/\s+/).filter(part => part);
        if (parts.length >= 5) {
          const id = parts[0].replace(':', '').trim();
          const response = parts[1].trim();
          const lines = parts[2];
          const word = parts[4] ;
          const chars = parts[6] ;
          results.push({
            id,
            response,
            lines,
            word,
            chars
          });
        }
      }
    }
    return results;
  };
  
router.post('/', async (req, res) => {
    const { endpoint, method, fields } = req.body;

    if (!endpoint || !method || !Array.isArray(fields)) {
        return res.status(400).json({ error: 'Invalid input' });
    }

    try {
        const fieldArgs = fields.map(field => `"${field}": "FUZZ"`).join(', ');
        const wfuzzCommand = `wsl wfuzz -z file,"${payloadFilePath}" -X ${method} -d '{${fieldArgs}}' -H "Content-Type: application/json" ${endpoint}`;

        console.log("exec: " + wfuzzCommand);

        const { stdout, stderr } = await execPromise(wfuzzCommand);

        if (stderr) {
            console.error(`wfuzz stderr: ${stderr}`);
        }

        const formattedOutput = parseWfuzzOutput(stdout);
        res.json({ results: formattedOutput });

    } catch (error) {
        console.error(`Error executing wfuzz: ${error}`);
        res.status(500).json({ error: 'Error executing wfuzz' });
    }
});

export default router;
