import User from '../models/UserModel.js';
import asyncHandler from 'express-async-handler';
import jwt from 'jsonwebtoken';

const jwtSecret = process.env.JWT_SECRET;
const jwtExpiresIn = process.env.JWT_EXPIRES_IN;

const generateToken = (id) => {
    return jwt.sign({ id }, jwtSecret, {
        expiresIn: jwtExpiresIn,
    });
};

const registerUser = asyncHandler(async (req, res) => {

    try {

        const { email, password, name } = req.body;
        const userExists = await User.findOne({ email });

        if (userExists) {
            res.status(400).json({
                message: 'User already exists',
                success: false
            });
        }

        const user = await User.create({ email, password, name });

        if (user) {
            res.status(201).json({
                user: user,
                token: generateToken(user._id),
                success: true,
                message: "User created successfully"
            });

        } else {
            res.status(400).json({
                message: 'Invalid user data',
                success: false
            })
        }
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }

});

const loginUser = asyncHandler(async (req, res) => {
    try {

        const { email, password } = req.body;
        const user = await User.findOne({ email });

        if (!user) {
            res.status(401).json({
                message: 'User not found',
                success: false
            });
        }

        if (user && (await user.matchPassword(password))) {
            res.status(201).json({
                user: user,
                token: generateToken(user._id),
                success: true,
                message: "Logged in successfully"
            });

        } else {
            res.status(401).json({
                message: 'Invalid email or password',
                success: false
            })
        }

    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Server error',
            error: error.message
        });
    }
});

const getUserProfile = asyncHandler(async (req, res) => {

    const user = await User.findById(req.user._id).select('-password');

    if (!user) {
        res.status(404).json({
            message: 'User not found',
            success: false
        });
    }

    if (user) {
        res.status(200).json({
            user,
            message: "Profile retrieved successfully",
            success: true
        });
    }

});

export { registerUser, loginUser, getUserProfile };
