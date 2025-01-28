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

export {
  createProjectEvent,
  projectDetailsEvent,
  TerminalRunEvent,
  FileDirectoryRunEvent
}