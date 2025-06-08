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
            src={otherUser.avatar || "https://media.istockphoto.com/id/1437821111/fr/photo/service-%C3%A0-la-client%C3%A8le-heureux-et-communication-de-la-femme-au-centre-dappels-pc-parlant.jpg?s=612x612&w=0&k=20&c=p8jjC-QHvBaFx4T3Fk0Avwm5X6WSSs9pheZ0XuubSnA="}
            alt={`${otherUser.name}'s avatar`}
            className="w-10 h-10 rounded-full border-2 border-white object-cover"
          />
          <div className="ml-3">
            <h1 className="text-lg font-bold tracking-wide">{otherUser.name}</h1>
            <p className="text-xs text-gray-200">Online</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;