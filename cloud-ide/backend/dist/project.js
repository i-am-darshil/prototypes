"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dockerode_1 = __importDefault(require("dockerode"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
class Project {
    name;
    status = "pending";
    type = "python";
    host;
    dockerConn = undefined;
    container;
    constructor(name, type, host) {
        this.name = name;
        this.type = type;
        this.host = host;
    }
    async create() {
        try {
            const docker = new dockerode_1.default({
                //'ip172-18-0-93-cubhcdaim2rg00cmbqj0-2375.direct.labs.play-with-docker.com' - Replace with the IP address from the session
                host: this.host,
                port: 2375, // Default exposed port for Docker API
                protocol: "http", // PWD uses HTTP, not HTTPS
            });
            this.dockerConn = docker;
            console.log(`Created docker conntection: ${JSON.stringify(docker)}`);
            // Define container options
            const containerOptions = {
                Image: "python:3.11-slim",
                Cmd: ["sleep", "infinity"],
                Tty: true,
                name: this.name,
            };
            const container = await docker.createContainer(containerOptions);
            this.container = container;
            await container.start();
            console.log(`Container ${this.name}:${this.type} started successfully`);
            const execBashMkdir = await container.exec({
                AttachStdout: true,
                AttachStderr: true,
                Cmd: [
                    '/bin/bash',
                    '-c',
                    `/bin/mkdir -p /${this.name}`,
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
            console.log(`outputBashMkdir: ${outputBashMkdir}`);
            this.status = "done";
        }
        catch (err) {
            console.error(`Container ${this.name}:${this.type} start failed`);
            console.error(err);
            this.status = "failed";
        }
    }
    async runCommand(command) {
        if (!this.container) {
            return undefined;
        }
        console.log(`Executing command: ${command}`);
        // Now you can execute Python commands or interact with the container
        const exec = await this.container.exec({
            AttachStdout: true,
            AttachStderr: true,
            Cmd: ["/bin/bash", "-c", `cd /${this.name} && ${command}`],
        });
        const stream = await exec.start({ Detach: false, stdin: true });
        return stream;
    }
    async getFileDirectory() {
        if (!this.container) {
            return {};
        }
        const basePath = "/" + this.name;
        const execBash = await this.container.exec({
            AttachStdout: true,
            AttachStderr: true,
            Cmd: ["/bin/bash", "-c", `find ${basePath} -type d -o -type f`],
        });
        const streamBash = await execBash.start({ Detach: false, stdin: true });
        let outputBash = "";
        streamBash.on("data", (chunk) => {
            outputBash += chunk.toString().trim();
        });
        await new Promise((resolve, reject) => {
            streamBash.on("end", resolve);
            streamBash.on("error", reject);
        });
        console.log(`outputBash: ${outputBash}`);
        let startIndex = outputBash.indexOf(basePath);
        outputBash = outputBash.substring(startIndex);
        /*
        new outputBash: /tmp
                        /tmp/sub1
                        /tmp/sub1/sub2
                        /tmp/sub1/sub2/abc2.txt
                        /tmp/sub1/abc1.txt
                        /tmp/sub2
                        /tmp/sub2/abc.txt
        */
        console.log(`new outputBash: ${outputBash}`);
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
        /*
        {
          "sub1": {
            "sub2": {
              "abc2.txt": null
            },
            "abc1.txt": null
          },
          "sub2": {
            "abc.txt": null
          }
        }
        */
        console.log(JSON.stringify(folderStructure, null, 2));
        return folderStructure;
    }
}
exports.default = Project;
