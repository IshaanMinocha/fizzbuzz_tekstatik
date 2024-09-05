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
    group: { 
        type: Number, 
        required: true 
    },  
},
    {
        timestamps: true,
        collection : 'FuzzResult'
    });

fuzzResultSchema.statics.getNextGroup = async function (userId) {
    const lastResult = await this.findOne({ user: userId }).sort({ group: -1 });
    
    if (!lastResult) {
        console.log(`No previous results found for user ${userId}, starting group at 1.`);
    } else {
        console.log(`Last group for user ${userId} is ${lastResult.group}. Incrementing group.`);
    }
    
    const nextGroup = lastResult ? lastResult.group + 1 : 1;
    return nextGroup;
};
    

const FuzzResult = mongoose.model('FuzzResult', fuzzResultSchema);

export default FuzzResult;