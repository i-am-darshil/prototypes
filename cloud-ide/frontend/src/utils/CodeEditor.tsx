"use client"
import Editor from "@monaco-editor/react";

export function CodeEditorComponent() {
  return (
    <div className="border border-solid border-gray-400 h-screen w-full">
<Editor
          height="100%"
          defaultLanguage="python"
          defaultValue="# Start coding..."
          theme="vs-dark"
        />
    </div>
    
  );
}