#!/usr/bin/env node

import connectDb from './config/db.js'
import { saveGreeting } from './controllers/ResultController.js';
import { program } from 'commander';

await connectDb();

program
    .option('-g, --greet <name>', 'Greet the user');

program.parse(process.argv);

const options = program.opts();

if (options.greet) {
    const greetingMessage = `Hello, ${options.greet}!`;
    await saveGreeting(greetingMessage);
    console.log("greeting saved to database");
    process.exit(1);
}
