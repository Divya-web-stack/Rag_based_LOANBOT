// src/components/HeroSection.tsx
import React from "react";

interface HeroProps {
  onStart: () => void;
}

const HeroSection: React.FC<HeroProps> = ({ onStart }) => {
  return (
    <section className="flex flex-col md:flex-row justify-between items-center px-10 md:px-20 py-24 gap-12 text-center md:text-left flex-1">
      <div className="flex-1">
        <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-4" style={{ color: "#5861B2" }}>
          Your Smart AI Loan Assistant
        </h1>
        <p className="text-lg mb-8 max-w-xl" style={{ color: "#5861B2", opacity: 0.8 }}>
          Experience a new way to explore personal, home, and gold loans —
          powered by intelligent conversations that understand your needs.
        </p>
        <button
          onClick={onStart}
          className="px-8 py-4 rounded-xl text-white font-semibold transition-all shadow-lg hover:shadow-xl hover:scale-105"
          style={{ backgroundColor: "#2F80E4" }}
        >
          Start Chatting
        </button>
        
        <div className="flex gap-8 mt-12 justify-center md:justify-start">
          <div className="text-center">
            <div className="text-3xl font-bold mb-1" style={{ color: "#2F80E4" }}>10K+</div>
            <div className="text-sm" style={{ color: "#5861B2", opacity: 0.7 }}>Happy Users</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold mb-1" style={{ color: "#2F80E4" }}>24/7</div>
            <div className="text-sm" style={{ color: "#5861B2", opacity: 0.7 }}>Support</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold mb-1" style={{ color: "#2F80E4" }}>Fast</div>
            <div className="text-sm" style={{ color: "#5861B2", opacity: 0.7 }}>Responses</div>
          </div>
        </div>
      </div>

      <div className="flex-1 relative">
        <div className="absolute inset-0 blur-3xl opacity-30 rounded-full" style={{ backgroundColor: "#6DA0E1" }}></div>
        <img
          src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
          alt="AI Assistant"
          className="w-72 md:w-96 mx-auto drop-shadow-2xl relative z-10 animate-float"
        />
      </div>
    </section>
  );
};

export default HeroSection;