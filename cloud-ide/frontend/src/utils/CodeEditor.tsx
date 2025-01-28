"use client"
import Editor from "@monaco-editor/react";
import { useWebSocket } from "@/contexts/WebSocketContext"
import React, { useState, useEffect } from "react";


export function CodeEditorComponent({project_name}: {project_name: string}) {

  // function editorDidMount(editor:any, monaco:any) {
  //   console.log('editorDidMount', editor);
  //   editor.focus();
  // }
  const { socket } = useWebSocket();
  const [state, setState] = useState<string>("");

  

  useEffect(() => {
    console.log(`CodeEditorComponent socket: ${socket?.id}`)
    socket?.emit("code-editor-details", {sender: "codeEditor", name: project_name})

    socket?.on("code-editor-details-response", (data) => {
      console.log("code-editor-details-response event recieved")
      console.log(JSON.stringify(data))
    })

    socket?.on("create-project-success", (data) => {
      console.log("create-project-success event recieved")
      console.log(JSON.stringify(data))
    })
  }, [])

  function onCodeChange(newValue: any, e: any){
    console.log('onChange', newValue, e)
  }

  return (
    <div className="border border-solid border-gray-400 h-screen w-full">
        <Editor
          height="100%"
          defaultLanguage="python"
          defaultValue="# Start coding..."
          theme="vs-dark"
          onChange={onCodeChange}
          // onMount={editorDidMount}
        />
    </div>
    
  );
}