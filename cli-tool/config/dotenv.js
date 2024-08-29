import dotenv from 'dotenv';

const envConfig = () => {
    dotenv.config({
        path: './.env'
    })
}

export default envConfig;