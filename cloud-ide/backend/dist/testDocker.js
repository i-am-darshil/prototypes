"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dockerode_1 = __importDefault(require("dockerode"));
async function main() {
    const docker = new dockerode_1.default({
        host: 'ip172-18-0-20-cu49migl2o9000doc7h0-2375.direct.labs.play-with-docker.com/_ping', // Replace with the IP address from the session
        port: 2375, // Default exposed port for Docker API
        protocol: 'http', // PWD uses HTTP, not HTTPS
    });
    console.log(`Created docker conntection: ${JSON.stringify(docker)}`);
    // Define container options
    const containerOptions = {
        Image: 'python:3.9-slim',
        Cmd: ['sleep', 'infinity'],
        Tty: true,
    };
    const container = await docker.createContainer(containerOptions);
    console.log(`container: ${JSON.stringify(container)}`);
    container.attach({ stream: true, stdout: true, stderr: true }, function (err, stream) {
        stream?.pipe(process.stdout);
    });
    await container.start();
    console.log(`Container started successfully`);
    const containerStatus1 = await container.inspect();
    console.log(`ContainerStatus: ${containerStatus1.State.Status}`);
    // Now you can execute Python commands or interact with the container
    const exec = await container.exec({
        AttachStdout: true,
        AttachStderr: true,
        Cmd: ['python3', '-c', 'print("Hello, world!")'],
    });
    const stream = await exec.start({ Detach: false, stdin: true });
    // Get the output of the Python command
    let output = '';
    stream.on('data', (data) => {
        output += data.toString();
    });
    stream.on('end', () => {
        console.log('Python command output:', output);
    });
    // Example: List all containers
    const allContainers = await docker.listContainers()
        .catch(err => {
        console.error('Error connecting to Docker:', err);
        return undefined;
    });
    console.log(allContainers);
    console.log("DONE");
}
main();
