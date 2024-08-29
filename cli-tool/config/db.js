import mongoose from 'mongoose';
import envConfig from './dotenv.js';

envConfig();

const mongoUri = process.env.MONGO_URI;
// console.log(mongoUri);

const connectDb = async () => {
    try {
        await mongoose.connect(mongoUri).then(() => {
            console.log("Connected to MongoDB");
        })
    } catch (error) {
        console.error('Error connecting to MongoDB:', error.message);
        process.exit(1);
    }
}

export default connectDb;