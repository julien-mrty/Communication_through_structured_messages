import * as React from 'react';
import { Message as MessageType } from '../types/chat';

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
  const isCurrentUser = message.sender === "frontend@localhost";

  const formattedTime = new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }).format(new Date(message.timestamp));

  return (
    <div className={`mb-4 ${isCurrentUser ? 'flex justify-end' : 'flex justify-start'}`}>
      <div className="flex flex-col max-w-[80%]">
        <div className="flex items-end gap-2">
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

            {message.components?.map((component, index) => {
              if (component.type === "binaryQuestion") {
                return (
                  <div key={index} className="mt-2">
                    <p className="text-sm">{component.question}</p>
                    <div className="flex gap-2 mt-1">
                      <button 
                        onClick={() => onYesNoReply(true)}
                        className="px-2 py-1 bg-green-200 text-green-900 rounded"
                      >
                        Oui
                      </button>
                      <button 
                        onClick={() => onYesNoReply(false)}
                        className="px-2 py-1 bg-red-200 text-red-900 rounded"
                      >
                        Non
                      </button>
                    </div>
                  </div>
                );
              }
              return null;
            })}
          </div>
        </div>

        <div className={`mt-1 text-xs text-gray-500 ${isCurrentUser ? 'text-right mr-10' : 'text-left ml-10'}`}>
          {formattedTime}
        </div>
      </div>
    </div>
  );
};

export default Message;
