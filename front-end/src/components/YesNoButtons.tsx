import React from 'react';

interface YesNoButtonsProps {
  onReply: (isYes: boolean) => void;
}

const YesNoButtons: React.FC<YesNoButtonsProps> = ({ onReply }) => {
  return (
    <div className="flex space-x-2 animate-fadeIn">
      <button
        className="px-4 py-2 rounded-full bg-[#007A33] text-white text-sm font-medium transition-transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#007A33]"
        onClick={() => onReply(true)}
      >
        Yes
      </button>
      <button
        className="px-4 py-2 rounded-full bg-[#C8102E] text-white text-sm font-medium transition-transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#C8102E]"
        onClick={() => onReply(false)}
      >
        No
      </button>
    </div>
  );
};

export default YesNoButtons;