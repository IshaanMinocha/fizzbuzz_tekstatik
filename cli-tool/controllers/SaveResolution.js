import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';
import Resolution from '../models/SaveResolutionModel.js'
import os from 'os';
import express from 'express';

// const homeDir = os.homedir();
// const TOKEN_PATH = path.resolve(homeDir, '.fizzbuzz_token');

// const JWT_SECRET = process.env.JWT_SECRET;  

const saveResolutionResult = async (resolutionData) => {

    try {
        // const token = fs.readFileSync(TOKEN_PATH, 'utf8');
        // const decodedToken = jwt.verify(token, JWT_SECRET);

        // const userId = decodedToken.id;
        // console.log(vulnerabilityId);

        const resolutionResult = new Resolution({
            vulnerability: vulnerabilityId,
            solution: resolutionData.solution,  
            code: resolutionData.code,
        });

    await resolutionResult.save();

        return {
            message: 'Resolution result saved successfully',
            success: true
        };
    } catch (error) {
        console.error('Error saving resolution result:', error);
        throw new Error('Failed to save resolution result');
    }
}

export { saveResolutionResult };
