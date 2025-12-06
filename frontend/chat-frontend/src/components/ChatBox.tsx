// ChatBox.tsx — Demo Conversation (User Uploaded PDFs)
import React from "react";
import { FileText } from "lucide-react"; // if you're using lucide-react for icons

const ChatBox: React.FC = () => {
  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-[#EEE2DF] via-[#DEC1DB] to-[#EAE6F2] p-6 overflow-y-auto">
      
      {/* Agent message - introduction */}
      <div className="self-start max-w-[75%] bg-[#5861B2] text-white rounded-2xl rounded-bl-none p-4 mb-4 shadow-md">
        <p>
          Hello! 👋 Here are the insurance plans we offer:
          <br />• Health Insurance
          <br />• Life Insurance
          <br />• Car Insurance
          <br />• Travel Insurance
          <br />• Home Insurance
          <br />Which one would you like to explore today?
        </p>
      </div>

      {/* User message - selects car insurance */}
      <div className="self-end max-w-[75%] bg-[#2F80E4] text-white rounded-2xl rounded-br-none p-4 mb-4 shadow-md">
        <p>I’d like to apply for Car Insurance 🚗</p>
      </div>

      {/* Agent message - requirements */}
      <div className="self-start max-w-[85%] bg-white border border-[#E0D4F5] text-gray-800 rounded-2xl rounded-bl-none p-5 mb-6 shadow-sm">
        <p className="font-semibold text-[#5861B2] mb-2">
          Great choice! To proceed with your Car Insurance application, please upload the following documents:
        </p>

        <div className="mt-3 space-y-3">
          {/* Identity and Age Proof */}
          <div>
            <h3 className="text-[#2F80E4] font-semibold mb-1">
              Identity & Age Proof (any one)
            </h3>
            <ul className="list-disc list-inside text-sm text-gray-700">
              <li>Aadhaar Card</li>
              <li>PAN Card</li>
              <li>Passport</li>
              <li>Voter ID</li>
              <li>Driving License</li>
              <li>Birth Certificate</li>
              <li>10th or 12th Marksheet</li>
            </ul>
          </div>

          {/* Address Proof */}
          <div>
            <h3 className="text-[#2F80E4] font-semibold mb-1">
              Address Proof (any one)
            </h3>
            <ul className="list-disc list-inside text-sm text-gray-700">
              <li>Aadhaar Card</li>
              <li>Passport</li>
              <li>Driving License</li>
              <li>Utility Bills (Electricity / Telephone)</li>
              <li>Rent Agreement</li>
              <li>Voter ID</li>
              <li>Ration Card</li>
            </ul>
          </div>

          {/* Other Required Documents */}
          <div>
            <h3 className="text-[#2F80E4] font-semibold mb-1">
              Other Required Documents
            </h3>
            <ul className="list-disc list-inside text-sm text-gray-700">
              <li>Proposal Form (filled & signed)</li>
              <li>Passport-size photographs</li>
              <li>Income Proof (salary slips / bank statement)</li>
              <li>Medical Report (if applicable)</li>
              <li>Vehicle Registration Certificate (RC Book)</li>
            </ul>
          </div>
        </div>
      </div>

      {/* User message - uploaded PDFs */}
      <div className="self-end max-w-[75%] bg-[#F8F9FF] border border-[#D6D8F5] rounded-2xl rounded-br-none p-5 shadow-sm">
        <p className="text-gray-700 mb-3">
          Here are my documents for verification. 📎
        </p>

        <div className="grid grid-cols-2 gap-3">
          {[
            "AadhaarCard.pdf",
            "PANCard.pdf",
            "AddressProof.pdf",
            "IncomeProof.pdf",
            "VehicleRC.pdf",
          ].map((file, index) => (
            <div
              key={index}
              className="flex items-center gap-2 bg-white border border-[#C9D8F0] rounded-lg px-3 py-2 shadow-sm hover:shadow-md transition"
            >
              <FileText className="w-5 h-5 text-[#2F80E4]" />
              <span className="text-sm text-gray-800">{file}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Agent confirmation */}
      <div className="self-start max-w-[75%] bg-[#5861B2] text-white rounded-2xl rounded-bl-none p-4 mt-4 shadow-md">
        <p>
          Perfect! ✅ All documents received. Our verification team will review
          them shortly and notify you about the approval.
        </p>
      </div>
    </div>
  );
};

export default ChatBox;
