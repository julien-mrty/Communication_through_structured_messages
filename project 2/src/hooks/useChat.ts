import { useState, useCallback, useEffect } from 'react';
import { ChatState, Message, QuickReply } from '../types/chat';
import { initialState } from '../data/initialData';

export const useChat = () => {
  const [chatState, setChatState] = useState<ChatState>(initialState);

  // Function to send a new message
  const sendMessage = useCallback((text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: chatState.users.currentUser,
      timestamp: new Date(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage],
    }));

    // Simulate the other user typing
    setChatState(prev => ({ ...prev, isTyping: true }));

    // Simulate a response after a delay
    setTimeout(() => {
      const responseMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: getRandomResponse(text),
        sender: chatState.users.otherUser,
        timestamp: new Date(),
        isQuestion: Math.random() > 0.5,
        requiresYesNo: Math.random() > 0.7,
        quickReplies: Math.random() > 0.5 ? getRandomQuickReplies() : undefined,
      };

      setChatState(prev => ({
        ...prev,
        isTyping: false,
        messages: [...prev.messages, responseMessage],
      }));
    }, 1500 + Math.random() * 1500); // Random delay between 1.5-3s
  }, [chatState.users]);

  // Function to send a quick reply
  const sendQuickReply = useCallback((reply: QuickReply) => {
    sendMessage(reply.text);
  }, [sendMessage]);

  // Function to send Yes/No response
  const sendYesNo = useCallback((isYes: boolean) => {
    sendMessage(isYes ? 'Yes' : 'No');
  }, [sendMessage]);

  // Function to get random responses
  const getRandomResponse = (text: string): string => {
    const responses = [
      `That's interesting about "${text.substring(0, 20)}..."`,
      "I agree with you on that!",
      "Let's talk more about this next game.",
      "I'm not sure I follow your point about the game.",
      "The coach needs to work on their strategy.",
      "Did you see the highlights from yesterday?",
      "What did you think about the referee calls?",
      "That player is definitely MVP material this season.",
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  // Function to get random quick replies
  const getRandomQuickReplies = (): QuickReply[] => {
    const allReplies = [
      { id: 'qr1', text: 'Great play yesterday!' },
      { id: 'qr2', text: 'Who\'s your MVP pick?' },
      { id: 'qr3', text: 'That referee was terrible' },
      { id: 'qr4', text: 'Did you get tickets yet?' },
      { id: 'qr5', text: 'Let\'s watch the next game together' },
      { id: 'qr6', text: 'That last shot was amazing' },
    ];
    
    // Shuffle and take 2-3 random quick replies
    const shuffled = [...allReplies].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, 2 + Math.floor(Math.random() * 2));
  };

  // Scroll to the bottom when messages change
  useEffect(() => {
    const chatContainer = document.getElementById('message-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [chatState.messages]);

  return {
    chatState,
    sendMessage,
    sendQuickReply,
    sendYesNo,
  };
};