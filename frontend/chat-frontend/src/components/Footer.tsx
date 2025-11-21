// src/components/Footer.tsx
import React from "react";

const Footer: React.FC = () => (
  <footer className="text-center text-sm py-6 mt-auto" style={{ backgroundColor: "rgba(238, 226, 223, 0.6)", color: "#5861B2" }}>
    <p className="mb-2">© {new Date().getFullYear()} LoanBot. Built with care using Bleu de France & Liberty.</p>
    <div className="flex gap-4 justify-center text-xs opacity-75">
      <a href="#privacy" className="hover:opacity-100 transition">Privacy Policy</a>
      <span>•</span>
      <a href="#terms" className="hover:opacity-100 transition">Terms of Service</a>
      <span>•</span>
      <a href="#support" className="hover:opacity-100 transition">Support</a>
    </div>
  </footer>
);

export default Footer;