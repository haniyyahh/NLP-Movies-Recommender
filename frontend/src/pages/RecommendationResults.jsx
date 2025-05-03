import React from "react";
import { motion } from "framer-motion";  // Import Framer Motion
import "./recommendationresults.css";

function RecommendationResults({ recommendations, onBack }) {
  return (
    <div className="results-container">
      <h1 className="results-title">Recommended Movies</h1>
      <p className="results-subtitle">Here are some movie recommendations for you!</p>

      <ul className="recommendation-list">
        {recommendations.map((movie, index) => (
          <motion.li
            key={index}
            className="recommendation-item"
            initial={{ opacity: 0, x: -100 }}  // Start off-screen to the left
            animate={{ opacity: 1, x: 0 }}     // Slide to its original position
            transition={{ delay: index * 0.1, type: "spring", stiffness: 100 }}  // Delay each animation slightly
          >
            <img 
              src={movie.large_thumbnail} 
              alt={movie.title} 
              className="recommendation-image"
            />
            <div className="recommendation-info">
              <h2 className="recommendation-title">{movie.title}</h2>
              <p className="recommendation-description">{movie.description}</p>
              <button className="recommendation-button">More Info</button>
            </div>
          </motion.li>
        ))}
      </ul>

      <button className="back-button" onClick={onBack}>Back</button>
    </div>
  );
}

export default RecommendationResults;
