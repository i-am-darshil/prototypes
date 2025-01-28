"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dockerode_1 = __importDefault(require("dockerode"));
async function main() {
    const docker = new dockerode_1.default({
        host: 'ip172-18-0-74-cuc5cf291nsg00f04le0-2375.direct.labs.play-with-docker.com/_ping', // Replace with the IP address from the session
        port: 2375, // Default exposed port for Docker API
        protocol: 'http', // PWD uses HTTP, not HTTPS
    });
    console.log(`Created docker conntection: ${JSON.stringify(docker)}`);
    // Define container options
    const containerOptions = {
        Image: 'python:3.11-slim',
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
    await new Promise((resolve, reject) => {
        stream.on("end", resolve);
        stream.on("error", reject);
    });
    console.log(`Python output: ${output}`);


    const execBashMkdir = await container.exec({
      AttachStdout: true,
      AttachStderr: true,
      Cmd: [
        '/bin/bash',
        '-c',
        '/bin/mkdir -p /tmp/sub1 /tmp/sub1/sub2 /tmp/sub2 && /bin/touch /tmp/sub1/abc1.txt /tmp/sub1/sub2/abc2.txt /tmp/sub2/abc.txt',
      ],
    });

    const streamBashMkdir = await execBashMkdir.start({ Detach: false, stdin: true });
    let outputBashMkdir = "";
    streamBashMkdir.on("data", (chunk) => {
      outputBashMkdir += chunk.toString();
    });
    await new Promise((resolve, reject) => {
      streamBashMkdir.on("end", resolve);
      streamBashMkdir.on("error", reject);
    });
    console.log(`outputBashMkdir: ${outputBashMkdir}`)



    const basePath = "/tmp";
    // Execute the `find` command inside the container
    const execBash = await container.exec({
        AttachStdout: true,
        AttachStderr: true,
        Cmd: ["/bin/bash", "-c", `find ${basePath} -type d -o -type f`],
    });
    // Start the exec instance and capture the output
    const streamBash = await execBash.start({ Detach: false, stdin: true });
    let outputBash = "";
    streamBash.on("data", (chunk) => {
        outputBash += chunk.toString().trim();
    });
    await new Promise((resolve, reject) => {
        streamBash.on("end", resolve);
        streamBash.on("error", reject);
    });
    console.log(`outputBash: ${outputBash}`)

    let startIndex = outputBash.indexOf(basePath)
    outputBash = outputBash.substring(startIndex)

    console.log(`new outputBash: ${outputBash}`)

    // Parse the `find` output into a dictionary
    const lines = outputBash.split("\n").filter((line) => line.trim() !== "");
    const folderStructure = {};


    lines.forEach((line) => {
        const parts = line.replace(basePath, "").split("/").filter(Boolean);
        let currentLevel = folderStructure;
        parts.forEach((part, index) => {
            if (index === parts.length - 1) {
                // If it's the last part, mark it as a file or folder
                currentLevel[part] = currentLevel[part] || (line.endsWith("/") ? {} : null);
            }
            else {
                // Create intermediate folders if they don't exist
                currentLevel[part] = currentLevel[part] || {};
                currentLevel = currentLevel[part];
            }
        });
    });
    console.log(JSON.stringify(folderStructure, null, 2));
    // Example: List all containers
    // const allContainers = await docker.listContainers()
    //     .catch(err => {
    //     console.error('Error connecting to Docker:', err);
    //     return undefined;
    // });
    // console.log(allContainers);
    // console.log("DONE");
}
main();
