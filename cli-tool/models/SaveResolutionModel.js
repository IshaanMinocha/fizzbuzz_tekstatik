import mongoose from "mongoose";

const resolutionSchema = new mongoose.Schema({
    vulnerability : {
        type: mongoose.Schema.Types.ObjectId,
        ref : 'Vulnerability',
        required: true
    },
    solution: {
        type: String,
        required: true
    },
    code: {
        type: String,
        required: true
    }
}, {
    timestamps: true,
    collection: 'Resolution'
})

const Resolution = mongoose.model('Resolution', resolutionSchema);

export default Resolution;