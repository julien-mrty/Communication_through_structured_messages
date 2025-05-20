import React from 'react';
import { User } from '../types/chat';

interface TypingIndicatorProps {
  user: User;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ user }) => {
  return (
    <div className="flex items-end mb-4">
      <img 
        src={user.avatar} 
        alt={`${user.name}'s avatar`}
        className="w-8 h-8 rounded-full object-cover"
      />
      <div className="ml-2 px-4 py-3 bg-white rounded-2xl rounded-bl-none shadow-sm">
        <div className="flex space-x-1">
          <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;