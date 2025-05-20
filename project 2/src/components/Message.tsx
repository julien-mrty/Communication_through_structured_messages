import React from 'react';
import { Message as MessageType } from '../types/chat';
import YesNoButtons from './YesNoButtons';
import QuickReplyOptions from './QuickReplyOptions';

interface MessageProps {
  message: MessageType;
  onYesNoReply: (isYes: boolean) => void;
  onQuickReply: (replyId: string, replyText: string) => void;
}

const Message: React.FC<MessageProps> = ({ 
  message, 
  onYesNoReply,
  onQuickReply 
}) => {
  const isCurrentUser = message.sender.isCurrentUser;
  
  const formattedTime = new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(message.timestamp);

  return (
    <div className={`mb-4 ${isCurrentUser ? 'flex justify-end' : 'flex justify-start'}`}>
      <div className="flex flex-col max-w-[80%]">
        <div className="flex items-end gap-2">
          {!isCurrentUser && (
            <img 
              src={message.sender.avatar} 
              alt={`${message.sender.name}'s avatar`}
              className="w-8 h-8 rounded-full object-cover"
            />
          )}
          
          <div 
            className={`
              px-4 py-3 rounded-2xl shadow-sm
              ${isCurrentUser 
                ? 'bg-[#17408B] text-white rounded-br-none' 
                : 'bg-white text-black rounded-bl-none border border-gray-200'}
            `}
            style={{
              animation: `${isCurrentUser ? 'slideInRight' : 'slideInLeft'} 0.3s ease-out`
            }}
          >
            <p className="text-sm md:text-base">{message.text}</p>
          </div>

          {isCurrentUser && (
            <img 
              src={message.sender.avatar} 
              alt={`${message.sender.name}'s avatar`}
              className="w-8 h-8 rounded-full object-cover"
            />
          )}
        </div>

        <div className={`mt-1 text-xs text-gray-500 ${isCurrentUser ? 'text-right mr-10' : 'text-left ml-10'}`}>
          {formattedTime}
        </div>

        {message.requiresYesNo && !isCurrentUser && (
          <div className="mt-2 ml-10">
            <YesNoButtons onReply={onYesNoReply} />
          </div>
        )}
        
        {message.quickReplies && message.quickReplies.length > 0 && !isCurrentUser && (
          <div className="mt-2 ml-10">
            <QuickReplyOptions 
              replies={message.quickReplies} 
              onSelectReply={(id, text) => onQuickReply(id, text)} 
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;