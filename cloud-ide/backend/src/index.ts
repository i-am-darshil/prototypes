import express, { Request, Response } from "express";
import cors from "cors";
import http from "http";
import { Server } from "socket.io";
import { createProjectEvent, projectDetailsEvent, TerminalRunEvent, FileDirectoryRunEvent } from "./interfaces";
import Project from "./project";

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000", // Replace with your frontend URL
    methods: ["GET", "POST"],
  },
});
const PORT = 4000;

const PROJECT_NAME_TO_PROJECT_MAP: { [key: string]: Project } = {};

app.use(cors());
app.use(express.json());

// Example API route
app.get("/api/hello", (req: Request, res: Response) => {
  res.json({ message: "Hello from TypeScript Express!" });
});

io.on("connection", (socket) => {
  console.log(`User connected: ${socket.id}`);

  socket.on("code-editor-details", (data: projectDetailsEvent) => {
    console.log("code-editor-details: ", data, socket.id);
    const project = PROJECT_NAME_TO_PROJECT_MAP[data.name]
    socket.emit("code-editor-details-response", {
      name: project?.name,
      type: project?.type,
      status: project?.status,
    });
  });

  socket.on("file-directory-request", async (data: FileDirectoryRunEvent) => {
    console.log("file-directory-request:", data, socket.id);
    const project = PROJECT_NAME_TO_PROJECT_MAP[data.name]
    let output: any = {}
    if (project) {
      output = await project.getFileDirectory()
    } 
    console.log(`file-directory-response: ${JSON.stringify(output)}`)
    socket.emit("file-directory-response", {
      name: project?.name,
      output: output
    });
  })

  socket.on("terminal-run-command", async (data: TerminalRunEvent) => {
    console.log("terminal-run-command:", data, socket.id);
    console.log(JSON.stringify(PROJECT_NAME_TO_PROJECT_MAP))

    const project = PROJECT_NAME_TO_PROJECT_MAP[data.name]

    let output = ""
    const command = data.input;

    if (!project) {
      output = "Project not found!"
    } else {
      const stream = await project.runCommand(command)
      if (stream) {
        // Get the output of the Python command
        let output = '';
        stream.on('data', (data: Buffer) => {
          output += data.toString();
        });

        stream.on('end', () => {
          console.log(`${command} command output:`, output);
          socket.emit("terminal-run-command-response", {
            name: project?.name,
            output: output
          });
        });

        return
      } else {
        output = "Environment not found!"
      }
    }
    socket.emit("terminal-run-command-response", {
      name: project?.name,
      output: output
    });
  });

  // Example event listener
  socket.on("create-project", async (data: createProjectEvent) => {
    console.log("Project Data:", data);
    const project = new Project(data.name, data.type, data.host);
    PROJECT_NAME_TO_PROJECT_MAP[project.name] = project;

    await project.create();

    socket.emit("create-project-success", {
      name: project.name,
      type: project.type,
      status: project.status,
    });

    console.log(JSON.stringify(PROJECT_NAME_TO_PROJECT_MAP))
  });

  socket.on("disconnect", () => {
    console.log(`User disconnected: ${socket.id}`);
  });
});

server.listen(PORT, () => {
  console.log(`Backend server running at http://localhost:${PORT}`);
});
