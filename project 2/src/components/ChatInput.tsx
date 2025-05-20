import React, { useState, KeyboardEvent } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (text: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = () => {
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="bg-white border-t border-gray-200 px-4 py-3">
      <div className="relative flex items-center">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className="flex-1 border border-gray-300 rounded-full py-2 pl-4 pr-10 focus:outline-none focus:ring-2 focus:ring-[#17408B] focus:border-transparent"
        />
        <button
          onClick={handleSubmit}
          disabled={!message.trim()}
          className={`absolute right-2 w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
            message.trim() 
              ? 'bg-[#17408B] text-white' 
              : 'bg-gray-200 text-gray-400'
          }`}
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;