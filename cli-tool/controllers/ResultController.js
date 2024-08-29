import Result from '../models/ResultModel.js';

const saveGreeting = async (message) => {
    try {
        const result = new Result({ message });
        await result.save();
        console.log(message);
    } catch (error) {
        console.error('Error saving greeting to database:', error);
        process.exit(1);
    }
};

export { saveGreeting };