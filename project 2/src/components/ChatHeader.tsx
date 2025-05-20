import React from 'react';
import { User } from '../types/chat';
import { MessageSquare } from 'lucide-react';

interface ChatHeaderProps {
  otherUser: User;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ otherUser }) => {
  return (
    <div className="flex items-center px-4 py-3 bg-gradient-to-r from-[#17408B] to-[#C8102E] text-white shadow-md">
      <div className="flex-1 flex items-center">
        <div className="mr-3">
          <MessageSquare size={24} className="text-white" />
        </div>
        <div className="flex items-center">
          <img 
            src={otherUser.avatar} 
            alt={`${otherUser.name}'s avatar`} 
            className="w-10 h-10 rounded-full border-2 border-white object-cover"
          />
          <div className="ml-3">
            <h1 className="text-lg font-bold tracking-wide">{otherUser.name}</h1>
            <p className="text-xs text-gray-200">Online</p>
          </div>
        </div>
      </div>
      <div className="w-8 h-8 flex items-center justify-center rounded-full bg-white/10">
        <span className="text-xs font-bold">NBA</span>
      </div>
    </div>
  );
};

export default ChatHeader;