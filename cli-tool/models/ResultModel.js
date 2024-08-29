import mongoose from 'mongoose';

const resultSchema = new mongoose.Schema({
    message: String
},
    {
        collection: 'Result',
        timestamps: true
    });

const Result = mongoose.model('Result', resultSchema);

export default Result;