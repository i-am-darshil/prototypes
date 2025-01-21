"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const http_1 = __importDefault(require("http"));
const socket_io_1 = require("socket.io");
const app = (0, express_1.default)();
const server = http_1.default.createServer(app);
const io = new socket_io_1.Server(server, {
    cors: {
        origin: "http://localhost:3000", // Replace with your frontend URL
        methods: ["GET", "POST"],
    },
});
const PORT = 4000;
app.use((0, cors_1.default)());
app.use(express_1.default.json());
// Example API route
app.get('/api/hello', (req, res) => {
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
