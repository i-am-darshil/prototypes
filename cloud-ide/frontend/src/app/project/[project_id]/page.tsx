import {FileTreeView} from "@/utils/FileTreeView";
import TerminalComponent from "@/utils/Terminal";
import { CodeEditorComponent } from "@/utils/CodeEditor";
// import dynamic from 'next/dynamic';

// const TerminalComponent = dynamic(() => import('@/utils/Terminal'), { ssr: false });

export default async function Page({
  params,
}: {
  params: Promise<{ project_id: string }>
}) {

  const project_id = (await params).project_id
  console.log(`project_id: ${project_id}`)

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-4 border border-solid border-gray-400">
        <h2 className="text-lg font-bold mb-2">File Explorer</h2>
        <FileTreeView />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Code Editor */}
        <CodeEditorComponent />

        {/* Terminal */}
        {/* <div id="terminal-container" className="h-30 bg-black" /> */}
        <TerminalComponent />
      </div>
    </div>
  );
}