import express from 'express';
import { registerUser, loginUser, getUserProfile } from '../controllers/UserController.js';
import { protect } from '../middlewares/AuthMiddleware.js';

const router = express.Router();

router.route('/register').post(registerUser);
router.route('/login').post(loginUser);
router.route('/profile').get(protect, getUserProfile);

export default router;
