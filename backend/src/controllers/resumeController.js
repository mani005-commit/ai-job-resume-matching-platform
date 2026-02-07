import Resume from "../models/Resume.js";

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
