import React from 'react';
import { useChat } from '../hooks/useChat';
import ChatHeader from './ChatHeader';
import Message from './Message';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';

const ChatContainer: React.FC = () => {
  const { chatState, sendMessage, sendYesNo, sendQuickReply } = useChat();
  const { messages, users, isTyping } = chatState;

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#FAFAFA] rounded-xl shadow-lg">
      <ChatHeader otherUser={users.otherUser} />
      
      <div 
        id="message-container" 
        className="flex-1 overflow-y-auto px-4 py-4 bg-[#F0F2F5] bg-opacity-80" 
        style={{
          backgroundImage: "url('https://images.pexels.com/photos/2277085/pexels-photo-2277085.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundBlendMode: "overlay"
        }}
      >
        {messages.map((message) => (
          <Message 
            key={message.id} 
            message={message} 
            onYesNoReply={sendYesNo}
            onQuickReply={(id, text) => sendQuickReply({ id, text })}
          />
        ))}
        
        {isTyping && <TypingIndicator user={users.otherUser} />}
      </div>
      
      <ChatInput onSendMessage={sendMessage} />

    </div>
  );
};

export default ChatContainer;