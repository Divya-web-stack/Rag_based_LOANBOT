// src/components/Sidebar.tsx
import React from "react";

interface SidebarProps {
  onNewChat: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onNewChat }) => (
  <aside className="w-72 p-6 flex flex-col shadow-2xl" style={{ background: "linear-gradient(180deg, #5861B2 0%, #2F80E4 100%)" }}>
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-lg" style={{ backgroundColor: "#EEE2DF" }}>
          💼
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">LoanBot</h1>
          <p className="text-sm opacity-90" style={{ color: "#DECIDE" }}>AI Banking Assistant</p>
        </div>
      </div>
    </div>

    <button
      onClick={onNewChat}
      className="w-full py-3 px-4 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 mb-6"
      style={{ backgroundColor: "#EEE2DF", color: "#5861B2" }}
    >
      <span className="text-lg mr-2">+</span> New Conversation
    </button>

    <div className="flex-1" />

    <div className="space-y-4 p-4 rounded-xl" style={{ backgroundColor: "rgba(238, 226, 223, 0.1)" }}>
      <div className="flex items-center gap-2 text-white text-sm opacity-90">
        <span className="text-lg">🔒</span>
        <span>Secure & Encrypted</span>
      </div>
      <div className="flex items-center gap-2 text-white text-sm opacity-90">
        <span className="text-lg">⚡</span>
        <span>Instant Responses</span>
      </div>
      <div className="flex items-center gap-2 text-white text-sm opacity-90">
        <span className="text-lg">🎯</span>
        <span>Personalized Advice</span>
      </div>
    </div>
  </aside>
);

export default Sidebar;