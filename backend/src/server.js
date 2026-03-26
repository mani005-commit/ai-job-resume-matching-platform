import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import connectDB from "./config/db.js";
import authRoutes from "./routes/authRoutes.js";
import resumeRoutes from "./routes/resumeRoutes.js";
import path from "path";
import jobRoutes from "./routes/jobRoutes.js";



dotenv.config();

const app = express(); // ✅ app FIRST


app.use("/uploads", express.static("uploads"));

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes); // ✅ app used AFTER creation
app.use("/api/resume", resumeRoutes);

app.use("/api/jobs", jobRoutes);

// Test route
app.get("/health", (req, res) => {
  res.json({ status: "OK", message: "Server running" });
});

// DB connect
connectDB();

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
