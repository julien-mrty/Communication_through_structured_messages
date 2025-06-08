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

  const formattedTime = message.timestamp
    ? new Intl.DateTimeFormat('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      }).format(new Date(message.timestamp))
    : "";

  const safeText = typeof message.text === "string"
    ? message.text
    : typeof message.text?.text === "string"
    ? message.text.text
    : JSON.stringify(message.text);

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
            <p className="text-sm md:text-base">{safeText}</p>

            {message.components?.map((component, index) => {
              const key = `${component.type}-${index}`;

              switch (component.type) {
                case "binaryQuestion":
                  return (
                    <div key={key} className="mt-2">
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

                case "multiChoice":
                  return (
                    <div key={key} className="mt-2">
                      <p className="text-sm">{component.question}</p>
                      <div className="flex gap-2 flex-wrap mt-1">
                        {Array.isArray(component.choices) &&
                          component.choices.map((choice: any, idx: number) => {
                            const rawLabel = typeof choice === "string" ? choice : choice.text;
                            const label = typeof rawLabel === "string"
                              ? rawLabel
                              : typeof rawLabel?.fr === "string"
                                ? rawLabel.fr
                                : JSON.stringify(rawLabel);

                            const id = typeof choice === "string"
                              ? choice
                              : choice.id ?? label;

                            return (
                              <button
                                key={`choice-${id}-${idx}`}
                                onClick={() => onQuickReply(id, label)}
                                className="px-3 py-1 bg-gray-100 border border-gray-300 rounded"
                              >
                                {label}
                              </button>
                            );
                          })}
                      </div>
                    </div>
                  );

                case "reservation":
                  return (
                    <div key={key} className="mt-3 text-sm text-gray-700">
                      <p><strong>📍 Lieu :</strong> {component.location}</p>
                      <p><strong>📅 Date :</strong> {new Date(component.date).toLocaleString()}</p>
                      <p><strong>🎤 Événement :</strong> {component.event_name}</p>
                      <p><strong>👥 Nombre de personnes :</strong> {component.nb_of_people}</p>
                    </div>
                  );

                default:
                  return null;
              }
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
