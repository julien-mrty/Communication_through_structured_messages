import React from 'react';
import { QuickReply } from '../types/chat';

interface QuickReplyOptionsProps {
  replies: QuickReply[];
  onSelectReply: (id: string, text: string) => void;
}

const QuickReplyOptions: React.FC<QuickReplyOptionsProps> = ({ replies, onSelectReply }) => {
  return (
    <div className="flex flex-wrap gap-2 animate-fadeIn">
      {replies.map((reply) => (
        <button
          key={reply.id}
          onClick={() => onSelectReply(reply.id, reply.text)}
          className="px-3 py-2 bg-[#FDB927] text-black text-sm rounded-full font-medium transition-transform hover:scale-105 active:scale-95 shadow-sm hover:shadow flex items-center"
        >
          <span className="mr-1">🏀</span> {reply.text}
        </button>
      ))}
    </div>
  );
};

export default QuickReplyOptions;