import mongoose from "mongoose";

const jobSchema = new mongoose.Schema(
  {
    recruiterId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },

    title: String,
    description: String,

    requirements: {
      skills: [String],
      minExperience: Number
    },

    status: {
      type: String,
      enum: ["open", "closed"],
      default: "open"
    }
  },
  {
    timestamps: true
  }
);

export default mongoose.model("Job", jobSchema);
