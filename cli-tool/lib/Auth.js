import fs from 'fs';
import path from 'path';
import axios from 'axios';
import readline from 'readline';
import envConfig from '../config/dotenv.js';
import os from 'os';

envConfig();

const backendUrl = process.env.BACKEND_URL;
const homeDir = os.homedir();

const tokenFilePath = path.resolve(homeDir, '.fizzbuzz_token');

export const readToken = () => {
    if (fs.existsSync(tokenFilePath)) {
        return fs.readFileSync(tokenFilePath, 'utf-8');
    }
    return null;
};

export const saveToken = (token) => {
    fs.writeFileSync(tokenFilePath, token, 'utf-8');
};

export const deleteToken = () => {
    if (fs.existsSync(tokenFilePath)) {
        fs.unlinkSync(tokenFilePath);
    }
};

const promptInput = (query) => {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    return new Promise((resolve) => rl.question(query, (ans) => {
        rl.close();
        resolve(ans);
    }));
};

export const login = async () => {
    const email = await promptInput('Email: ');
    const password = await promptInput('Password: ');

    try {
        const response = await axios.post(`${backendUrl}/user/login`, { email, password });
        saveToken(response.data.token);
        console.log('Login successful');
    } catch (error) {
        console.error('Login failed:', error.response?.data?.message || error.message);
        process.exit(1);
    }
};

export const logout = () => {
    deleteToken();
    console.log('Logged out successfully');
    process.exit(1);
};
