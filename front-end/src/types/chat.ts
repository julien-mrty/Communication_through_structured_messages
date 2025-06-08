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

export interface ChatState {
  messages: Message[];
  users: {
    currentUser: User;
    otherUser: User;
  };
  isTyping: boolean;
}

export interface StructuredComponent {
  type: string;
  [key: string]: any;
}

export interface Message {
  id: string;
  thread_id?: string;
  timestamp: string;
  sender: string;
  receiver: string;
  text: string;
  components: StructuredComponent[];
  extensions: Record<string, any>;
}
