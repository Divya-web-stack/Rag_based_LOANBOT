// src/pages/LandingPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import Footer from "../components/Footer";

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "linear-gradient(135deg, #EEE2DF 0%, #DECIDE 50%, #EEE2DF 100%)" }}>
      <Navbar />
      <HeroSection onStart={() => navigate("/chat")} />
      <Footer />
    </div>
  );
};

export default LandingPage;