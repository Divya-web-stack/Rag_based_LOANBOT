// src/components/ChatInput.tsx
import React, { useState } from "react";

const ChatInput: React.FC<{ onSend: (text: string) => void }> = ({ onSend }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <div className="max-w-4xl mx-auto w-full">
      <div className="flex gap-3 p-2 rounded-2xl shadow-lg" style={{ backgroundColor: "#FFFFFF" }}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask me about loans, rates, eligibility..."
          className="flex-1 px-4 py-3 rounded-xl outline-none text-sm"
          style={{ backgroundColor: "#EEE2DF", color: "#5861B2" }}
        />
        <button
          onClick={handleSend}
          disabled={!text.trim()}
          className="px-6 py-3 rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          style={{ backgroundColor: "#2F80E4", color: "#FFFFFF" }}
        >
          Send
        </button>
      </div>
      
      <div className="flex gap-2 mt-4 flex-wrap justify-center">
        {["Personal Loan", "Home Loan", "Gold Loan", "Eligibility Check"].map((action) => (
          <button
            key={action}
            onClick={() => onSend(`Tell me about ${action}`)}
            className="px-4 py-2 rounded-lg text-xs font-medium transition-all duration-300 hover:shadow-md hover:scale-105"
            style={{ backgroundColor: "#DECIDE", color: "#5861B2" }}
          >
            {action}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ChatInput;