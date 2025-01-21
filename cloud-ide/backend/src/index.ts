import express, { Request, Response } from 'express';
import cors from 'cors';
import http from "http";
import { Server } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000", // Replace with your frontend URL
    methods: ["GET", "POST"],
  },
});
const PORT = 4000;

app.use(cors());
app.use(express.json());

// Example API route
app.get('/api/hello', (req: Request, res: Response) => {
    res.json({ message: 'Hello from TypeScript Express!' });
});

io.on("connection", (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Example event listener
  socket.on("create-project", (data) => {
    console.log("Project Data:", data);
    // socket.emit("project-created", { success: true, projectName: data.name });
  });

  socket.on("disconnect", () => {
    console.log(`User disconnected: ${socket.id}`);
  });
});

server.listen(PORT, () => {
    console.log(`Backend server running at http://localhost:${PORT}`);
});
