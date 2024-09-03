import mongoose from 'mongoose';

const fuzzResultSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    output: {
        response: {
            type: String,
            required: true
        },
        lines: {
            type: Number,
            required: true
        },
        words: {
            type: Number,
            required: true
        },
        chars: {
            type: Number, 
            required: true
        },
        timeTaken: {
            type: String,
            required: true
        },
        payload: {
            type: String,
            required: true
        }
    },
    targetUrl: {
        type: String,
        required: true
    },
    fuzzType: {
        type: String,
        required: true
    },
},
    {
        timestamps: true,
        collection: 'FuzzResult'
    });

const FuzzResult = mongoose.model('FuzzResult', fuzzResultSchema);

export default FuzzResult;