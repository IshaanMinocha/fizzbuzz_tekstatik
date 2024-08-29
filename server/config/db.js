import mongoose from "mongoose";
import envConfig from './dotenv.js';

envConfig();

const mongoUri = process.env.MONGO_URI;

const connectDb = async () => {
    try {
        const conn = await mongoose.connect(mongoUri)
        console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (error) {
        console.error('Error connecting to MongoDB:', error.message);
        process.exit(1);
    }
}

export default connectDb;