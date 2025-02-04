"use client"
import React, { useEffect, useState } from "react";
import { useWebSocket } from "@/contexts/WebSocketContext"

const Terminal = ({project_name}: {project_name: string}) => {
  const [output, setOutput] = useState<string[]>([]); // Stores terminal output
  const [input, setInput] = useState<string>(""); // Stores current user input
  const { socket } = useWebSocket();

  // React.useEffect(() => {
  //   console.log(`Terminal useEffect socket?.id: ${socket?.id}`)
  //   // if (!socket?.hasListeners("terminal-run-command-response")) {
  //     socket?.on("terminal-run-command-response", (data) => {
  //       console.log(JSON.stringify(data))
  //       console.log("terminal-run-command-response event recieved")
  //       setOutput((prev) => [...prev, `=> ${data.output.trim()}`]); // Show command in terminal
  //     })
  //   // }
  // }, [socket])


  // Handle user input submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!socket?.hasListeners("terminal-run-command-response")) {
      socket?.on("terminal-run-command-response", (data) => {
        console.log(JSON.stringify(data))
        console.log("terminal-run-command-response event recieved")
        setOutput((prev) => [...prev, `=> ${data.output.trim()}`]); // Show command in terminal
      })
    }

    console.log(`Terminal socket: ${socket?.id}, project_name: ${project_name}, ${socket?.hasListeners("terminal-run-command-response")}, input: ${input}`)

    // const { socket } = useWebSocket();
    if (input.trim()) {
      if (input == "clear") {
        setOutput((prev) => []);
        setInput("");
        return
      }
      setOutput((prev) => [...prev, `$ ${input}`]); // Show command in terminal
      if (!socket) return;
      socket.emit("terminal-run-command", {name: project_name, input}); // Send command to backend
      setInput(""); // Clear input
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#000",
        color: "#0f0",
        fontFamily: "monospace",
        height: "400px",
        overflowY: "auto",
        padding: "10px",
        border: "solid gray"
      }}
    >
      <div>
        {output.map((line, index) => (
          <div className="" key={index}>{line}</div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ display: "flex" }}>
        <span style={{ color: "#0f0", marginRight: "5px" }}>$</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            backgroundColor: "black",
            color: "#0f0",
            border: "none",
            outline: "none",
            flexGrow: 1,
            marginLeft: "3px"
          }}
        />
      </form>
    </div>
  );
};

export default Terminal;
