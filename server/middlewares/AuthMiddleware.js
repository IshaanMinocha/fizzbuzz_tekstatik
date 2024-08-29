import jwt from 'jsonwebtoken';
import User from '../models/UserModel.js';
import asyncHandler from 'express-async-handler';

const jwtSecret = process.env.JWT_SECRET;

const protect = asyncHandler(async (req, res, next) => {
  let token;

  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    try {
      token = req.headers.authorization.split(' ')[1];
      const decoded = jwt.verify(token, jwtSecret);

      req.user = await User.findById(decoded.id).select('-password');

      if (!req.user) {
        return res.status(401).json({
          message: 'User not found',
          success: false,
        });
      }

      next();
    } catch (error) {
      console.error(error);
      res.status(401).json({
        message: 'Not authorized, token failed',
        success: false,
      });
    }
  } else {
    res.status(401).json({
      message: 'Not authorized, no token',
      success: false,
    });
  }
});

export { protect };
