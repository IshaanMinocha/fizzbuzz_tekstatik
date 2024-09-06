import asyncHandler from 'express-async-handler';
import FuzzResult from '../models/FuzzedModel.js';
// import FuzzResult from '../../cli-tool/models/FuzzModel.js';

const getAllFuzzResults = asyncHandler(async (req, res) => {

    // const groupNumber = req.params.group 

    try {
        // const fuzzResults = await FuzzResult.find().populate('user', 'name email');
        const fuzzResults = await FuzzResult.find({
            user: req.user._id,
            // group: groupNumber
        }).populate('user', 'name email');

        if (fuzzResults.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'No results found for the specified group'
            });
        }
        res.status(200).json(
            {
                success: true,
                message: "Fetched all results",
                fuzzResults
            });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server errorrtgrtg',
            error: error.message
        });
    }
});

const getFuzzResultById = asyncHandler(async (req, res) => {

    // const groupNumber = req.params.group;

    try {
        // const fuzzResult = await FuzzResult.findById(req.params.id).populate('user', 'name email');
        const fuzzResult = await FuzzResult.findOne({
            _id: req.params.id,
            user: req.user._id,
            // group: groupNumber
        }).populate('user', 'name email');

        if (!fuzzResult) {
            return res.status(404).json({
                success: false,
                message: 'Fuzz result not found for the specified group'
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
            message: 'Server errorgredg',
            error: error.message
        });
    }
});

const getUserGroups = asyncHandler(async (req, res) => {
    try {
        const userGroups = await FuzzResult.aggregate([
            {
                $match: { user: req.user._id }
            },
            {
                $unwind: "$output"
            },
            {
                $group: {
                    _id: "$group",
                    createdAt: { $first: "$createdAt" }
                }
            },
            {
                $sort: { createdAt: 1 }
            }
        ]);

        if (userGroups.length === 0) {
            return res.status(404).json({
                success: false,
                message: "No groups found for the user"
            });
        }

        res.status(200).json({
            success: true,
            message: "Fetched all unique groups",
            userGroups
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error43534',
            error: error.message
        });
    }
});

export { getAllFuzzResults, getFuzzResultById, getUserGroups };