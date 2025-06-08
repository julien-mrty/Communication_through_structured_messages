import { ChatState, QuickReply } from '../types/chat';

export const QUICK_REPLIES: QuickReply[] = [
  { id: '1', text: 'Great game last night!' },
  { id: '2', text: 'Did you see that dunk?' },
  { id: '3', text: 'Who\'s your favorite player?' },
  { id: '4', text: 'Let\'s go to a game soon' }
];

export const initialState: ChatState = {
  messages: [
    {
      id: '1',
      text: 'Hey! Did you watch the Lakers game last night?',
      sender: {
        id: '2',
        name: 'Michael',
        avatar: 'https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=150',
        isCurrentUser: false,
      },
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
      isQuestion: true,
      requiresYesNo: true,
    },
    {
      id: '2',
      text: 'Yes! What an amazing comeback in the fourth quarter!',
      sender: {
        id: '1',
        name: 'Jessica',
        avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=150',
        isCurrentUser: true,
      },
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 1.5), // 1.5 hours ago
    },
    {
      id: '3',
      text: 'That three-pointer at the buzzer was incredible. Do you think they can make the playoffs this year?',
      sender: {
        id: '2',
        name: 'Michael',
        avatar: 'https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=150',
        isCurrentUser: false,
      },
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
      isQuestion: true,
      requiresYesNo: true,
    },
  ],
  users: {
    currentUser: {
      id: '1',
      name: 'Jessica',
      avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=150',
      isCurrentUser: true,
    },
    otherUser: {
      id: '2',
      name: 'Michael',
      avatar: 'https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=150',
      isCurrentUser: false,
    }
  },
  isTyping: false,
};