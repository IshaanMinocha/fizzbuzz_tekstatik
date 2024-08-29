import { saveGreeting } from '../controllers/ResultController.js';

export const greetUser = async (name) => {
    const greetingMessage = `Hello, ${name}!`;
    await saveGreeting(greetingMessage);
    console.log("Greeting saved to database");
};
