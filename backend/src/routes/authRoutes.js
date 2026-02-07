import express from "express";

console.log("✅ AUTH ROUTES FILE LOADED");
import { 
    registerUser,
    loginUser
 } from "../controllers/authController.js";

const router = express.Router();

router.post("/register", registerUser);
router.post("/login", loginUser);

export default router;
