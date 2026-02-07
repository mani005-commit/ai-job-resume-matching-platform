import mongoose from "mongoose";

const matchSchema = new mongoose.Schema(
  {
    jobId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Job",
      required: true
    },

    resumeId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Resume",
      required: true
    },

    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },

    scores: {
      skillMatch: Number,
      experienceMatch: Number,
      overallMatch: Number
    },

    explanation: [String]
  },
  {
    timestamps: true
  }
);

export default mongoose.model("Match", matchSchema);
