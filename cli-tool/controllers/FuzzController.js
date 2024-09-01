import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';
import FuzzResult from '../models/FuzzModel.js';
import os from 'os';

const homeDir = os.homedir();
const TOKEN_PATH = path.resolve(homeDir, '.fizzbuzz_token');

const saveFuzzResult = async (fuzzResultData) => {

    try {
        const token = fs.readFileSync(TOKEN_PATH, 'utf8');
        const decodedToken = jwt.verify(token);

        const userId = decodedToken.id;
        console.log(userId);

        const fuzzResult = new FuzzResult({
            user: userId,
            output: {
                response: fuzzResultData.output.response,
                lines: fuzzResultData.output.lines,
                words: fuzzResultData.output.words,
                chars: fuzzResultData.output.chars,
                timeTaken: fuzzResultData.output.timeTaken,
                payload: fuzzResultData.output.payload
            },
            targetUrl: fuzzResultData.targetUrl,
            fuzzType: fuzzResultData.fuzzType
            // "targetUrl": sys.argv[1], 
            // "fuzzType": sys.argv[2] 
        });

    await fuzzResult.save();

    res.status(201).json({
        message: 'Fuzz result saved successfully',
        data: fuzzResult,
        success: true
    });
    process.exit(1);
} catch (error) {
    console.error('Error saving fuzz result:', error);
    res.status(500).json({
        error: 'Failed to save fuzz result',
        success: false
    });
    process.exit(0);
}
}

export { saveFuzzResult };
