import asyncHandler from 'express-async-handler';
import Resolution from '../models/ResolutionModel.js';

const getAllResolutions = asyncHandler(async (req, res) => {
    try {
        const resolutions = await Resolution.find()
            .populate({
                path: 'vulnerability',
                select: 'targetUrl severity fuzzType',
            });
        res.status(200).json({
            success: true,
            message: "Fetched all resolutions",
            resolutions
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }
});

const getResolutionById = asyncHandler(async (req, res) => {
    try {
        const resolution = await Resolution.findById(req.params.id)
            .populate({
                path: 'vulnerability',
                select: 'targetUrl severity fuzzType',
            });
        if (!resolution) {
            return res.status(404).json({
                success: false,
                message: 'Resolution not found'
            });
        }
        res.status(200).json({
            success: true,
            resolution,
            message: "Fetched resolution by id"
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }
});

export { getAllResolutions, getResolutionById };
