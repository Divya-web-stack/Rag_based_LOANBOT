// src/pages/ChatPage.tsx
import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import ChatBox from "../components/ChatBox";
import ChatInput from "../components/ChatInput";
import type { Message } from "../types";

const API_URL = "http://127.0.0.1:8000/chat";

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "👋 Hello! I'm your Loan Assistant. Ask me anything about personal, home, or gold loans.", sender: "bot" },
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    setMessages((prev) => [...prev, { text, sender: "user" }]);
    setIsTyping(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const dataText = await res.text();
      const data = JSON.parse(dataText);
      setMessages((prev) => [...prev, { text: data.reply || "🤖 No reply received.", sender: "bot" }]);
    } catch (err: any) {
      setMessages((prev) => [...prev, { text: `⚠️ Server Error: ${err.message}`, sender: "bot" }]);
    } finally {
      setIsTyping(false);
    }
  };

  const newChat = () => {
    setMessages([{ text: "👋 Hello! I'm your Loan Assistant. Ask me anything about personal, home, or gold loans.", sender: "bot" }]);
  };

  return (
    <div className="flex h-screen" style={{ background: "linear-gradient(135deg, #EEE2DF 0%, #DECIDE 100%)" }}>
      <Sidebar onNewChat={newChat} />
      <main className="flex flex-col flex-1 p-8">
        <div className="mb-6 pb-4 border-b-2" style={{ borderColor: "rgba(88, 97, 178, 0.2)" }}>
          <h2 className="text-2xl font-bold" style={{ color: "#5861B2" }}>Chat with LoanBot</h2>
          <p className="text-sm mt-1" style={{ color: "#6DA0E1" }}>Get instant answers to all your loan queries</p>
        </div>
        <ChatBox messages={messages} isTyping={isTyping} />
        <ChatInput onSend={sendMessage} />
      </main>
    </div>
  );
};

export default ChatPage;