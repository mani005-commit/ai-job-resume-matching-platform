import Resume from "../models/Resume.js";
import axios from "axios";
import fs from "fs";
import FormData from "form-data";

// 🔹 Upload Resume (already working)
export const uploadResume = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }

    const resume = await Resume.create({
      userId: req.user.id,
      file: {
        fileName: req.file.originalname,
        fileType: req.file.mimetype,
        fileUrl: req.file.path
      },
      status: "uploaded"
    });

    res.status(201).json({
      message: "Resume uploaded successfully",
      resume
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};


// 🔥 Analyze Resume (NEW)
export const analyzeResume = async (req, res) => {
  try {
    const { id } = req.params;

    const resume = await Resume.findById(id);

    if (!resume) {
      return res.status(404).json({ message: "Resume not found" });
    }

    // Update status → processing
    resume.status = "processing";
    await resume.save();

    // Prepare file for AI service
    const formData = new FormData();
    formData.append(
      "file",
      fs.createReadStream(resume.file.fileUrl)
    );

    // Call AI Service
    const aiResponse = await axios.post(
      "http://127.0.0.1:8000/parse",
      formData,
      {
        headers: formData.getHeaders()
      }
    );

    // Save parsed data
    resume.parsedData = {
      skills: aiResponse.data.skills_extracted || [],
      experience: aiResponse.data.experience || {},
      education: aiResponse.data.education || {}
    };

    resume.status = "parsed";
    await resume.save();

    res.json({
      message: "Resume analyzed successfully",
      parsedData: resume.parsedData
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Resume analysis failed" });
  }
};
