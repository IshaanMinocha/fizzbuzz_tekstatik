import express from 'express';
import { getAllFuzzResults, getFuzzResultById } from '../controllers/FuzzedController.js';
import { protect } from '../middlewares/AuthMiddleware.js'

const router = express.Router();

router.route('/').get(protect, getAllFuzzResults);
router.route('/:id').get(protect, getFuzzResultById);

export default router;