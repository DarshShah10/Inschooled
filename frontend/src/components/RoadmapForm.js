// src/components/RoadmapForm.js
import React, { useState } from "react";
import axios from "axios";

const RoadmapForm = ({ setRoadmap, setSessionId }) => {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    location: "",
    career_goal: "",
    standard: "",
    interests_and_hobbies: "",
    academic_strengths: "",
    weaknesses: "",
    learning_style: "",
    other_details: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const user_info = {
      name: formData.name,
      age: formData.age,
      location: formData.location,
      career_goal: formData.career_goal,
      additional_info: {
        standard: formData.standard,
        interests_and_hobbies: formData.interests_and_hobbies,
        academic_strengths: formData.academic_strengths,
        weaknesses: formData.weaknesses,
        learning_style: formData.learning_style,
        other_details: formData.other_details,
      },
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/generate-roadmap",
        { user_info }
      );
      setRoadmap(response.data.roadmap);
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error("Error generating roadmap:", error);
      alert("Failed to generate roadmap. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Provide Your Information</h2>
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="age"
        placeholder="Age"
        value={formData.age}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="location"
        placeholder="Location"
        value={formData.location}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="career_goal"
        placeholder="Career Goal"
        value={formData.career_goal}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="standard"
        placeholder="Current Grade/Standard"
        value={formData.standard}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="interests_and_hobbies"
        placeholder="Interests/Hobbies (comma-separated)"
        value={formData.interests_and_hobbies}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="academic_strengths"
        placeholder="Academic Strengths"
        value={formData.academic_strengths}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="weaknesses"
        placeholder="Areas for Improvement"
        value={formData.weaknesses}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="learning_style"
        placeholder="Preferred Learning Style"
        value={formData.learning_style}
        onChange={handleChange}
        required
      />
      <textarea
        name="other_details"
        placeholder="Any Other Relevant Details"
        value={formData.other_details}
        onChange={handleChange}
        required
      />
      <button type="submit">Generate Roadmap</button>
    </form>
  );
};

export default RoadmapForm;
