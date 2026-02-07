import mongoose from "mongoose";

const resumeSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },

    file: {
      fileName: String,
      fileType: String,
      fileUrl: String
    },

    extractedText: String,

    parsedData: {
      skills: [String],
      education: [String],
      experience: [
        {
          role: String,
          company: String,
          years: Number
        }
      ]
    },

    resumeScore: Number,

    status: {
      type: String,
      enum: ["uploaded", "parsed"],
      default: "uploaded"
    }
  },
  {
    timestamps: true
  }
);

export default mongoose.model("Resume", resumeSchema);
