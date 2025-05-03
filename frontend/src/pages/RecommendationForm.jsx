import React, { useState } from "react";
import "./recommendationform.css"; 

function RecommendationForm({ onSubmit }) {
  const [userInput, setUserInput] = useState({
    query: "",
    category: "All",
    tone: "All",
  });

  const handleChange = (e) => {
    setUserInput({
      ...userInput,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(userInput);  // pass the user input to the parent component
  };

  return (
    <div className="recommendation-container">
      <div className="form-container">
        <h1 className="form-title">Find Your Movie</h1>
        <p className="form-subtitle">Let us help you pick the best movie!</p>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="query"
            placeholder="Enter a keyword"
            value={userInput.query}
            onChange={handleChange}
            className="input-field"
          />
          
          <select
            name="category"
            value={userInput.category}
            onChange={handleChange}
            className="select-field"
          >
            <option value="All">All Categories</option>
            <option value="Action">Action</option>
            <option value="Comedy">Comedy</option>
            <option value="Drama">Drama</option>
            <option value="Horror">Action</option>
            <option value="Comedy">Comedy</option>
            <option value="Drama">Drama</option>
            {/* ADD MORE ACCURATE CATEGORIES */}
          </select>

          <select
            name="tone"
            value={userInput.tone}
            onChange={handleChange}
            className="select-field"
          >
            <option value="All">All Tones</option>
            <option value="Happy">Happy</option>
            <option value="Sad">Sad</option>
            <option value="Angry">Angry</option>
            {/* ADD MORE ACCURATE TONES */}
          </select>

          <button type="submit" className="submit-button">Get Recommendations</button>
        </form>
      </div>
    </div>
  );
}

export default RecommendationForm;
