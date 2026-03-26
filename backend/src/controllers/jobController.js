import Job from "../models/Job.js";

// ✅ Create Job (Recruiter only)
export const createJob = async (req, res) => {
  try {
    const { title, description, skills, minExperience } = req.body;

    const job = await Job.create({
      recruiterId: req.user.id,
      title,
      description,
      requirements: {
        skills,
        minExperience
      }
    });

    res.status(201).json({
      message: "Job created successfully",
      job
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Failed to create job" });
  }
};


// ✅ Get All Jobs
export const getJobs = async (req, res) => {
  try {
    const jobs = await Job.find().populate("recruiterId", "name email");

    res.json(jobs);

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Failed to fetch jobs" });
  }
};


// ✅ Get Single Job
export const getJobById = async (req, res) => {
  try {
    const job = await Job.findById(req.params.id)
      .populate("recruiterId", "name email");

    if (!job) {
      return res.status(404).json({ message: "Job not found" });
    }

    res.json(job);

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error fetching job" });
  }
};