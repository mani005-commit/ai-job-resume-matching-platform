// backend/src/models/User.js

import mongoose from "mongoose";

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true
    },

    email: {
      type: String,
      required: true,
      unique: true
    },

    passwordHash: {
      type: String,
      required: true
    },

    role: {
      type: String,
      enum: ["job_seeker", "recruiter", "admin"],
      required: true
    },

    profile: {
      companyName: String,
      experienceYears: Number
    }
  },
  {
    timestamps: true
  }
);

export default mongoose.model("User", userSchema);
