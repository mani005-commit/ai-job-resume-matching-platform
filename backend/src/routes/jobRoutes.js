import express from "express";
import {
  createJob,
  getJobs,
  getJobById
} from "../controllers/jobController.js";

import { protect, authorize } from "../middleware/authMiddleware.js";

const router = express.Router();

// ✅ Create job (protected)
router.post("/", protect,authorize("recruiter"), createJob);

// ✅ Get all jobs
router.get("/", getJobs);

// ✅ Get single job
router.get("/:id", getJobById);

export default router;