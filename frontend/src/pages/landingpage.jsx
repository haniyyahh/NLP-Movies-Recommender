import React from "react";
import "./landingpage.css";
import pickieLogo from "../assets/pickie-logo.png";

function LandingPage({ onBegin }) {
  return (
    <div className="landing-container">
      <img src={pickieLogo} alt="Pickie Logo" className="logo" />
      <h1 className="title">PICKIE</h1>
      <p className="subtitle">HELPS PICK YOU A MOVIE!</p>
      <button className="begin-button" onClick={onBegin}>BEGIN!</button>
    </div>
  );
}

export default LandingPage;
