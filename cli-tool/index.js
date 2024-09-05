#!/usr/bin/env node

import { program } from 'commander';
import connectDb from './config/db.js';
import { readToken, login, logout } from './lib/Auth.js';
import { greetUser } from './lib/Greet.js';
import { runWfuzz } from './lib/wfuzz.js';

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

program
    .command('fuzz <url>')
    // .description('Fuzz a target URL using wfuzz')
    .option('-w, --wordlist <path>', 'Path to the wordlist')
    .option('-f, --fuzzType <type>', 'Type of fuzzing (e.g., API endpoints, virtual hosts, SQL injection)')
    .option('-H, --header <header>', 'Add headers to the request')
    .option('-b, --cookie <cookie>', 'Add cookies to the request')
    .option('-d, --data <data>', 'Send data in the body of the request (for POST requests)')
    .option('-X, --method <method>', 'Specify the HTTP method (GET, POST, etc.)')
    .option('-c, --color', 'Show output in color')

    .action((url, options) => {
        const flags = [];

        if (options.wordlist) {
            flags.push(`-z file,${options.wordlist}`);
        }
        if (options.fuzzType) {
            flags.push(`-f "${options.fuzzType}"`)
        }
        if (options.header) {
            flags.push(`-H "${options.header}"`);
        }
        if (options.cookie) {
            flags.push(`-b "${options.cookie}"`);
        }
        if (options.data) {
            flags.push(`-d "${options.data}"`);
        }
        if (options.method) {
            flags.push(`-X ${options.method}`);
        }
       
        if (options.color) {
            flags.push('-c');
        }

        

        runWfuzz(url, flags);
});


program.parse(process.argv);

if (!process.argv.slice(2).length) {
    program.outputHelp();
    process.exit(1);
}