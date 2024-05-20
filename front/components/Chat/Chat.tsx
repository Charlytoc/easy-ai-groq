import { useState, useEffect, KeyboardEvent } from "react";
import "./chat.css";
import { SVGS } from "../../assets/svgs";
import toast from "react-hot-toast";

interface Message {
  content: string;
  role: "user" | "assistant";
}

const MessageComponent = ({
  content,
  role,
}: {
  content: string;
  role: "user" | "assistant";
}) => {
  const readMessage = () => {
    const utterance = new SpeechSynthesisUtterance(content);
    speechSynthesis.speak(utterance);
  };

  const copyMessage = () => {
    navigator.clipboard.writeText(content);
    toast.success("Message copied to clipboard!");
  };

  return (
    <div className={`message ${role}`}>
      <p>
        <strong>{role}:</strong> {content}
      </p>
      <button onClick={readMessage}>{SVGS.read}</button>
      <button onClick={copyMessage}>{SVGS.copy}</button>
    </div>
  );
};

export const Chat = () => {
  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const connectWebSocket = () => {
    const websocket = new WebSocket("ws://127.0.0.1:8000/message");

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === "chunk" && data.content) {
        console.log(data.content);

        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          if (
            updatedMessages.length > 0 &&
            updatedMessages[updatedMessages.length - 1].role === "assistant"
          ) {
            updatedMessages[updatedMessages.length - 1].content += data.content;
          } else {
            updatedMessages.push({ content: data.content, role: "assistant" });
          }
          return updatedMessages;
        });
      }
      if (data.event === "finish") {
        console.log("Finish event received");
      }
    };

    websocket.onclose = () => {
      console.log("WebSocket connection closed. Reconnecting...");
      setTimeout(() => connectWebSocket(), 1000);
    };

    setWs(websocket);

    const pingInterval = setInterval(() => {
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({ event: "ping" }));
      }
    }, 30000); // Ping every 30 seconds

    return () => {
      clearInterval(pingInterval);
      websocket.close();
    };
  };

  useEffect(() => {
    connectWebSocket();
  }, []);

  const sendMessage = () => {
    if (ws) {
      if (ws.readyState === WebSocket.OPEN) {
        const lastFourMessages = messages.slice(-4);
        toast.error(`${messages.length}`)
        const memory = lastFourMessages.map((msg) => {
          return {
            role: msg.role,
            content: msg.content,
          };
        });

        const payload = {
          prompt: message,
          memory: memory,
        };

        ws.send(JSON.stringify(payload));
        setMessages((prevMessages) => [
          ...prevMessages,
          { content: message, role: "user" },
          { content: "", role: "assistant" },
        ]);
        setMessage("");
      } else {
        console.log("WebSocket is not open. Reconnecting...");
        connectWebSocket();
      }
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-component">
      <h1>Easy chatbot</h1>
      <div className="chat-info">
        <small>Make your own AI application that is blazzingly fast with</small>
        <span> | </span>
        <a
          href="https://console.groq.com/docs/quickstart"
          target="_blank"
          rel="noopener noreferrer"
        >
          Groq
        </a>
        <span> | </span>
        <a
          href="https://vitejs.dev/"
          target="_blank"
          rel="noopener noreferrer"
        >ViteJs</a>
        <span> | </span>
        <a
          href="https://fastapi.tiangolo.com/"
          target="_blank"
          rel="noopener noreferrer"
          >FastAPI</a>
      </div>
      <div className="chat-input">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyUp={handleKeyPress}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <div className="messages">
        {messages.map((msg, index) => (
          <MessageComponent key={index} content={msg.content} role={msg.role} />
        ))}
      </div>
    </div>
  );
};
