import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';
import FuzzResult from '../models/FuzzModel.js';
import os from 'os';
import express from 'express';

const homeDir = os.homedir();
const TOKEN_PATH = path.resolve(homeDir, '.fizzbuzz_token');

const JWT_SECRET = process.env.JWT_SECRET;  // You should define this in your .env file or environment

const saveFuzzResult = async (fuzzResultData) => {

    try {
        const token = fs.readFileSync(TOKEN_PATH, 'utf8');
        const decodedToken = jwt.verify(token, JWT_SECRET);

        const userId = decodedToken.id;
        console.log(userId);

        const group = await FuzzResult.getNextGroup(userId);

        if (isNaN(group)) {
            throw new Error("Group value is NaN. Unable to proceed.");
        }
        console.log(`Group value assigned: ${group}`);  // Debugging

        const fuzzResult = new FuzzResult({
            user: userId,
            output: fuzzResultData.output,  // This is the array of results
            targetUrl: fuzzResultData.targetUrl,
            fuzzType: fuzzResultData.fuzzType,
            group: group  
        });

        // for (const result of fuzzResultData.output) {
        //     // Ensure each field is correctly populated and not null
        //     console.log("Saving result:", result);
            
        //     if (!result.payload || !result.response || !result.lines || !result.words || !result.chars) {
        //         throw new Error(`Invalid result data: ${JSON.stringify(result)}`);
        //     }

        //     const fuzzResult = new FuzzResult({
        //         user: userId,
        //         output: {
        //             response: result.response,
        //             lines: result.lines,
        //             words: result.words,
        //             chars: result.chars,
        //             payload: result.payload
        //         },
        //         targetUrl: fuzzResultData.targetUrl,
        //         fuzzType: fuzzResultData.fuzzType
        //     });
    await fuzzResult.save();
    //console.log('Fuzz result saved successfully:', fuzzResult);

        return {
            message: 'Fuzz result saved successfully',
            success: true
        };
    } catch (error) {
        console.error('Error saving fuzz result:', error);
        throw new Error('Failed to save fuzz result');
    }
}

export { saveFuzzResult };
