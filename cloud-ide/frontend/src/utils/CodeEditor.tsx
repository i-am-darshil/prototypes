"use client"
import Editor from "@monaco-editor/react";
import { useWebSocket } from "@/contexts/WebSocketContext"
import React, { useState, useEffect, useRef } from "react";


export function CodeEditorComponent({project_name}: {project_name: string}) {

  const { socket } = useWebSocket();
  const [fileContent, setFileContent] = useState<string>("# Start coding..");
  const [filePath, setFilePath] = useState<string>("");

  const fileContentRef = useRef(fileContent);
  const filePathRef = useRef(filePath);

  useEffect(() => {
    fileContentRef.current = fileContent;
    filePathRef.current = filePath;
  }, [fileContent, filePath]);

  useEffect(() => {
    console.log(`CodeEditorComponent socket: ${socket?.id}`);
  
    const handler = (data: any) => {
      console.log(`fileContent: ${fileContentRef.current}, filePath: ${filePathRef.current}, project_name: ${project_name}: ${filePath.includes(project_name)}`)
      console.log(`code-editor-details-response event received: ${JSON.stringify(data)}`);
  
      if (filePathRef.current.includes(project_name)) {
        socket?.emit("save-file-content-request", {
          name: project_name,
          filePath: filePathRef.current,
          fileContent: fileContentRef.current
        });
      }
  
      setFileContent(data.output);
      setFilePath(data.filePath);
    };
  
    socket?.on("file-content-response", handler);
  
    return () => {
      socket?.off("file-content-response", handler);
    };
  }, [socket, project_name]);
  

  function onCodeChange(newValue: any, e: any){
    // console.log(`fileContent: ${fileContent}, filePath: ${filePath}, project_name: ${project_name}: ${filePath.includes(project_name)}`)
    // console.log('onChange', newValue, e)
    setFileContent(newValue)
  }

  return (
    <div className="border border-solid border-gray-400 h-screen w-full">
        <Editor
          height="100%"
          defaultLanguage="python"
          defaultValue="# Start coding.."
          theme="vs-dark"
          onChange={onCodeChange}
          value={fileContent}
          // onMount={editorDidMount}
        />
    </div>
    
  );
}