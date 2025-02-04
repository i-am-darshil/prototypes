"use client"
import React, { createContext, useContext, useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

type WebSocketContextType = {
  socket: Socket | null;
};

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    // Connect to the Socket.IO server
    const socketInstance = io("http://localhost:4000"); // Replace with your backend URL

    socketInstance.on("connect", () => {
      console.log("Socket.IO connection established:", socketInstance.id);
      setSocket(socketInstance);
    });

    socketInstance.on("disconnect", () => {
      console.log("Socket.IO connection disconnected");
      setSocket(socketInstance);
    });

    // setSocket(socketInstance);

    // Cleanup the socket connection on unmount
    return () => {
      socketInstance.disconnect();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={{ socket }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return context;
};
