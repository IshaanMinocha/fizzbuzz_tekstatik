import asyncHandler from 'express-async-handler';
import FuzzResult from '../models/FuzzedModel.js';
// import FuzzResult from '../../cli-tool/models/FuzzModel.js';

const getAllFuzzResults = asyncHandler(async (req, res) => {
    try {
        const fuzzResults = await FuzzResult.find().populate('user', 'name email');
        res.status(200).json(
            {
                success: true,
                message: "Fetched all results",
                fuzzResults
            });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }
});

const getFuzzResultById = asyncHandler(async (req, res) => {
    try {
        const fuzzResult = await FuzzResult.findById(req.params.id).populate('user', 'name email');
        if (!fuzzResult) {
            return res.status(404).json({
                success: false,
                message: 'Fuzz result not found'
            });
        }
        res.status(200).json({
            success: true,
            fuzzResult,
            message: "Fetched fuzz result by id"
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }
});

export { getAllFuzzResults, getFuzzResultById };