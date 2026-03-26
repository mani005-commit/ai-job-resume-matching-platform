import express from "express";
import upload from "../config/multer.js";
import {
  uploadResume,
  analyzeResume
} from "../controllers/resumeController.js";
import { protect } from "../middleware/authMiddleware.js";

const router = express.Router();

router.post("/upload", protect, upload.single("resume"), uploadResume);

router.post("/analyze/:id", protect, analyzeResume);

export default router;
