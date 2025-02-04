type createProjectEvent = {
  name: string,
  type: string,
  host:string
}

type projectDetailsEvent = {
  name: string,
  sender: string,
}

type TerminalRunEvent = {
  name: string,
  input: string,
}

type FileDirectoryRunEvent = {
  name: string,
}

type FileSelectedRequestEvent = {
  name: string,
  filePath: string,
}

type FileSaveContentRequestEvent = {
  name: string,
  filePath: string,
  fileContent: string
}

export {
  createProjectEvent,
  projectDetailsEvent,
  TerminalRunEvent,
  FileDirectoryRunEvent,
  FileSelectedRequestEvent,
  FileSaveContentRequestEvent
}