#!/usr/bin/env node

import { program } from 'commander';
import connectDb from './config/db.js';
import { readToken, login, logout } from './lib/Auth.js';
import { greetUser } from './lib/Greet.js';

await connectDb();

program
    .command('login')
    .description('Login to the fizzbuzz tool')
    .action(async () => {
        await login();
        process.exit(0);
    });

program
    .command('logout')
    .description('Logout from the fizzbuzz tool')
    .action(() => {
        logout();
        process.exit(0);
    });

program
    .option('-g, --greet <name>', 'Greet the user')
    .action(async (options) => {
        if (options.greet) {
            const token = readToken();
            
            if (!token) {
                console.log('Login first using >> fizzbuzz login');
                process.exit(1);
            }

            await greetUser(options.greet);
            process.exit(0);
        }
    });

program.parse(process.argv);

if (!process.argv.slice(2).length) {
    program.outputHelp();
    process.exit(1);
}