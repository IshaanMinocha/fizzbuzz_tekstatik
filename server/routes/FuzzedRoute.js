import express from 'express';
import { getAllFuzzResults, getFuzzResultById, getUserGroups } from '../controllers/FuzzedController.js';
import { protect } from '../middlewares/AuthMiddleware.js'

const router = express.Router();

router.route('/').get(protect, getAllFuzzResults);
router.route('/get/:id').get(protect, getFuzzResultById);
router.route('/g').get(protect, getUserGroups)

export default router;