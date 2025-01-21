"use client"
import React, { useEffect, useRef } from "react";
import { Terminal } from "xterm";

import "xterm/css/xterm.css";

const TerminalComponent = () => {
  const terminalRef = useRef<HTMLDivElement | null>(null);
  const term = useRef<Terminal | null>(null);

  useEffect(() => {
    if (terminalRef.current && !term.current) {
      // Initialize Terminal
      term.current = new Terminal({
        rows: 20,
        cols: 80,
        cursorBlink: true,
        theme: {
          background: 'black',  // Dark background color
          foreground: '#c5c8c6',   // Text color
          cursor: '#f8f8f0',       // Cursor color
          selectionBackground: 'rgba(255, 255, 255, 0.3)', // Selection color
        },
      });

      if (terminalRef.current) {
        term.current.open(terminalRef.current);

        // Welcome message
        term.current.writeln("Welcome to the Terminal!");
        term.current.write("$ ");
      }

      // // Resize the terminal to fit its container
      // term.current.fit();

      // Handle user input
      term.current.onData((data) => {
        handleUserInput(data);
      });

      return () => {
        term.current?.dispose();
      };
    }
  }, []);

  // Buffer for user input
  let inputBuffer = "";

  const handleUserInput = (data: string) => {
    // Handle Enter key
    if (data === "\r") {
      term.current?.writeln(""); // Move to the next line
      processCommand(inputBuffer.trim()); // Process the command
      inputBuffer = ""; // Reset buffer
      term.current?.write("$ "); // New prompt
    }
    // Handle Backspace
    else if (data === "\u007F") {
      if (inputBuffer.length > 0) {
        inputBuffer = inputBuffer.slice(0, -1); // Remove last character
        term.current?.write("\b \b"); // Remove from terminal display
      }
    }
    // Handle regular characters
    else {
      inputBuffer += data; // Add character to buffer
      term.current?.write(data); // Display character on terminal
    }
  };

  const processCommand = (command: string) => {
    switch (command) {
      case "help":
        term.current?.writeln("Available commands: help, echo <message>");
        break;
      case "":
        // No command entered
        break;
      default:
        if (command.startsWith("echo ")) {
          term.current?.writeln(command.slice(5));
        } else {
          term.current?.writeln(`Unknown command: ${command}`);
        }
        break;
    }
  };

  return (
    <div>
      <div
        ref={terminalRef}
        style={{
          height: "100%",
          width: "100%",
          backgroundColor: "black",
          color: "white",
          padding: "4px",
          border: "solid rgb(156 163 175)",
        }}
      />
    </div>
  );
};

export default TerminalComponent;
