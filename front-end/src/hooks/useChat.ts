import { useEffect, useState } from "react";
import { Message } from "../types/chat";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);

  useEffect(() => {
    const startConversation = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/start");
        const data = await res.json();
        setThreadId(data.thread_id);
        setMessages([data]);
      } catch (err) {
        console.error("Erreur lors de l'initialisation :", err);
      }
    };

    startConversation();
  }, []);

  const sendMessage = async (text: string) => {
    if (!threadId) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      thread_id: threadId,
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
        body: JSON.stringify(userMessage),
      });

      const data = await res.json();
      console.log("🎯 Données reçues du back-end :", data);

      setMessages((prev) => [...prev, data]);
    } catch (err) {
      console.error("Erreur lors de l'envoi :", err);
    } finally {
      setIsTyping(false);
    }
  };

  const sendYesNo = async (answer: boolean) => {
    await sendMessage(answer ? "oui" : "non");
  };

  const sendQuickReply = async (_replyId: string, replyText: string) => {
    await sendMessage(replyText);
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
    sendYesNo,
    sendQuickReply,
  };
}
