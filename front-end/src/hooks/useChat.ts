import { useState } from "react";
import { Message } from "../types/chat";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async (text: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      sender: "frontend@localhost",
      receiver: "bot@localhost",
      timestamp: new Date().toISOString(),
      text,
      components: [],
      extensions: {},
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:8000/api/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text }),
      });

      const data = await res.json();
      console.log("Réponse du backend :", data);

      const botMessage: Message = {
        id: data.response.id,
        sender: data.response.sender,
        receiver: data.response.receiver,
        timestamp: data.response.timestamp,
        text: data.response.text,
        components: data.response.components || [],
        extensions: data.response.extensions || {},
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error("Erreur lors de l'envoi :", err);
    } finally {
      setIsTyping(false);
    }
  };

  return {
    chatState: {
      messages,
      users: {
        currentUser: "frontend@localhost",
        otherUser: "bot@localhost",
      },
      isTyping,
    },
    sendMessage,
    sendYesNo: () => {},
    sendQuickReply: () => {},
  };
}
