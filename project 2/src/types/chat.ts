export interface User {
  id: string;
  name: string;
  avatar: string;
  isCurrentUser: boolean;
}

export interface QuickReply {
  id: string;
  text: string;
}

export interface Message {
  id: string;
  text: string;
  sender: User;
  timestamp: Date;
  isQuestion?: boolean;
  quickReplies?: QuickReply[];
  requiresYesNo?: boolean;
}

export interface ChatState {
  messages: Message[];
  users: {
    currentUser: User;
    otherUser: User;
  };
  isTyping: boolean;
}