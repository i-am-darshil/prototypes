import {FileTreeView} from "@/utils/FileTreeView";
import { CodeEditorComponent } from "@/utils/CodeEditor";
import Terminal from "@/components/custom-terminal"
import { useWebSocket } from "@/contexts/WebSocketContext"
import React from "react";

export default async function Page({
  params,
}: {
  params: Promise<{ project_name: string }>
}) {

  const project_name = (await params).project_name
  console.log(`project_id: ${project_name}`)

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-2 border border-solid border-gray-400">
        <h2 className="text-lg font-bold mb-2">File Explorer</h2>
        <FileTreeView project_name={project_name}/>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Code Editor */}
        <CodeEditorComponent project_name={project_name} />

        {/* Terminal */}
        {/* <div id="terminal-container" className="h-30 bg-black" /> */}
        <Terminal project_name={project_name}/>
      </div>
    </div>
  );
}