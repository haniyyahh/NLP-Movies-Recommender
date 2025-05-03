import React, { useState } from 'react';
import LandingPage from './pages/landingpage';
import RecommendationForm from './pages/RecommendationForm';
import RecommendationResults from './pages/RecommendationResults';

function App() {
  const [step, setStep] = useState(0);           // 0 = landing, 1 = form, 2 = results
  const [recommendations, setRecommendations] = useState([]);


  const handleBegin = () => setStep(1);

  const handleRecommend = async (userInput) => {
    // Ensure userInput is structured as an object with the correct fields
    const formattedInput = {
      query: userInput.query || "",    // default empty string
      category: userInput.category || "All",  // set to "All" if not provided
      tone: userInput.tone || "All",    // set to "All" if not provided
    };

    try {
      console.log("Sending request with input:", formattedInput); // debug
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formattedInput),  // use the formattedInput structure for any responses on frontend
      });

      console.log("Response Status:", response.status); // debug

      if (!response.ok) {
        throw new Error("Failed to fetch recommendations");
      }

      const data = await response.json();
      console.log("Recommendations:", data);  // debug

      // store the recommendations in state
      setRecommendations(data);

      // move to the results page after receiving recommendations
      setStep(2);
    } catch (error) {
      console.error("Error:", error);  
    }
  };

  // start with landing page, then form, then results
  return (
    <>
      {step === 0 && <LandingPage onBegin={handleBegin} />}

      {step === 1 && (
        <RecommendationForm onSubmit={handleRecommend} />
      )}

      {step === 2 && (
        <RecommendationResults recommendations={recommendations} />
      )}
    </>
  );
}

export default App;
