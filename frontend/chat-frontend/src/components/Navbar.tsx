// src/components/Navbar.tsx
import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => (
  <nav className="flex justify-between items-center px-10 md:px-20 py-6 bg-transparent font-medium">
    <Link to="/" className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-lg flex items-center justify-center text-xl shadow-md" style={{ backgroundColor: "#5861B2" }}>
        💼
      </div>
      <h1 className="text-2xl font-bold" style={{ color: "#5861B2" }}>LoanBot</h1>
    </Link>
    <div className="flex gap-6">
      <Link to="/" className="transition-colors hover:scale-105 transition-transform" style={{ color: "#5861B2" }}>Home</Link>
      <a href="#about" className="transition-colors hover:scale-105 transition-transform" style={{ color: "#5861B2" }}>About</a>
      <a href="#contact" className="transition-colors hover:scale-105 transition-transform" style={{ color: "#5861B2" }}>Contact</a>
    </div>
  </nav>
);

export default Navbar;