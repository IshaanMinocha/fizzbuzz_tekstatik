import mongoose from 'mongoose';

const FuzzOutputSchema = new mongoose.Schema({
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
    payload: { 
        type: String, 
        required: true 
    }
});

const fuzzResultSchema = new mongoose.Schema({
    user: { 
        type: mongoose.Schema.Types.ObjectId, 
        ref: 'User', 
        required: true 
    },
    output: { 
        type: [FuzzOutputSchema], 
        required: true 
    }, 
    targetUrl: { 
        type: String, 
        equired: true 
    },
    fuzzType: { 
        type: String, 
        required: true 
    },
    //createdAt: { type: Date, default: Date.now }
},
    {
        timestamps: true,
        collection : 'FuzzResult'
    });

const FuzzResult = mongoose.model('FuzzResult', fuzzResultSchema);

export default FuzzResult;