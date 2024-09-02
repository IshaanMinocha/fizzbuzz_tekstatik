import express from 'express';
import { getAllResolutions, getResolutionById } from '../controllers/ResolutionController.js';
import { protect } from '../middlewares/AuthMiddleware.js';

const router = express.Router();

router.route('/').get(protect, getAllResolutions);
router.route('/:id').get(protect, getResolutionById);

export default router;