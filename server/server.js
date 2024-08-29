import express from 'express';
import envConfig from './config/dotenv.js';
import connectDb from './config/db.js';
import cors from 'cors';
import userRouter from './routes/UserRoute.js'

envConfig();

const server = express();

const port = process.env.PORT || 8000;

server.use(cors({
    origin: '*'
}));
server.use(express.json());

server.use('/user', userRouter);

const startServer = async () => {
    try {
        await connectDb();
        server.listen(port, () =>
            console.log(`Server running on port http://localhost:${port}`)
        )
    } catch (error) {
        console.error('DB connection failed:', error.message);
    }
};

startServer();

server.get('/', (req, res) => {
    res.json({ success: true, message: 'server up!' })
})