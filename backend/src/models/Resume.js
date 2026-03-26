import mongoose from "mongoose";

const ResumeSchema = new mongoose.Schema(
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

    status: {
      type: String,
      enum: ["uploaded", "processing", "parsed", "failed"],
      default: "uploaded"
    },

    parsedData: {
      skills: [String],
      experience: {
        years: Number,
        roles: [String]
      },
      education: {
        degree: String,
        field: String
      }
    }
  },
  { timestamps: true }
);

export default mongoose.model("Resume", ResumeSchema);
