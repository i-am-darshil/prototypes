import Docker, { Container, ContainerInfo } from "dockerode";
import * as stream from "stream";

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export default class Project {
  name: string;
  status: "pending" | "done" | "failed" = "pending";
  type: string = "python";
  host: string;
  dockerConn: Docker | undefined = undefined;
  container: Docker.Container | undefined;

  constructor(name: string, type: string, host: string) {
    this.name = name;
    this.type = type;
    this.host = host;
  }

  async create() {
    try {
      const docker = new Docker({
        //'ip172-18-0-93-cubhcdaim2rg00cmbqj0-2375.direct.labs.play-with-docker.com' - Replace with the IP address from the session
        host: this.host,
        port: 2375, // Default exposed port for Docker API
        protocol: "http", // PWD uses HTTP, not HTTPS
      });

      this.dockerConn = docker;

      console.log(`Created docker conntection: ${JSON.stringify(docker)}`);

      const streamPull = await docker.pull("python:3.11-slim")
      let outputPull = "";
      streamPull.on("data", (chunk) => {
        outputPull += chunk.toString();
      });
      await new Promise((resolve, reject) => {
        streamPull.on("end", resolve);
        streamPull.on("error", reject);
      });
      console.log(`outputPull: ${outputPull}`)

      try {
        const existingContainers = await docker.listContainers()
        console.log(`existingContainers: ${JSON.stringify(existingContainers)}`)
        const existingContainerList = existingContainers.filter((existingContainer) => existingContainer.Names.includes("/" + this.name))
        if (existingContainerList.length > 0) {
          const existingContainer = docker.getContainer(this.name);
          console.log(`existingContainer: ${JSON.stringify(existingContainer)}`)
          if (existingContainer) {
            this.container = existingContainer;
            this.status = "done";
            return;
          }
        }
        
      } catch (err) {
        console.error(`err while getting container: ${err}`)
      }
      

      // Define container options
      const containerOptions = {
        Image: "python:3.11-slim",
        Cmd: ["sleep", "infinity"],
        Tty: true,
        name: this.name,
      };

      const container: Docker.Container =
        await docker.createContainer(containerOptions);
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
      console.log(`outputBashMkdir: ${outputBashMkdir}`)

      this.status = "done";
    } catch (err) {
      console.error(`Container ${this.name}:${this.type} start failed`);
      console.error(err);
      this.status = "failed";
    }
  }

  async runCommand(command: string): Promise<stream.Duplex | undefined> {
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

  // async saveFileContent(filePath: string, fileContent: string) {
  //   if (!this.container) {
  //     return undefined;
  //   }

  //   fileContent = fileContent.trim()
  //   const execBashSaveFileContent = await this.container.exec({
  //     AttachStdout: true,
  //     AttachStderr: true,
  //     Cmd: ["/bin/bash", "-c", `printf %s "${fileContent.replace(/"/g, '\\"')}" > ${filePath}`],
  //   });

  //   const streamBashSaveFileContent = await execBashSaveFileContent.start({ Detach: false, stdin: true });
  //   let outputBashSaveFileContent = "";
    // streamBashSaveFileContent.on("data", (chunk) => {
    //   let chunkStr = chunk.toString().trim();
  
    //   // Remove leading control characters except newlines (\n)
    //   chunkStr = chunkStr.replace(/^[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/, ""); 
      
    //   outputBashSaveFileContent += chunkStr;
    // });
    // await new Promise((resolve, reject) => {
    //   streamBashSaveFileContent.on("end", resolve);
    //   streamBashSaveFileContent.on("error", reject);
    // });
    // console.log(`saveFileContent outputBashSaveFileContent: ${outputBashSaveFileContent}`)
  // }

  async saveFileContent(filePath: string, fileContent: string) {
    if (!this.container) {
        return undefined;
    }

    // ✅ Step 1: Truncate the file (clear all previous content)
    const execBashTruncateFileContent = await this.container.exec({
        AttachStdout: true,
        AttachStderr: true,
        Cmd: ["/bin/bash", "-c", `> "${filePath}"`],  // Truncate file
    })
    const streamBashTruncateFileContent = await execBashTruncateFileContent.start({ Detach: false })
    let outputBashTruncateFileContent = "";
    streamBashTruncateFileContent.on("data", (chunk) => {
      let chunkStr = chunk.toString().trim();
  
      // Remove leading control characters except newlines (\n)
      chunkStr = chunkStr.replace(/^[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/, ""); 
      
      outputBashTruncateFileContent += chunkStr;
    });

    await new Promise((resolve, reject) => {
      streamBashTruncateFileContent.on("end", resolve);
      streamBashTruncateFileContent.on("error", reject);
    });
    console.log(`saveFileContent outputBashTruncateFileContent: ${outputBashTruncateFileContent}`)

    // ✅ Step 2: Write the new content
    const execBashSaveFileContent = await this.container.exec({
        AttachStdout: true,
        AttachStderr: true,
        AttachStdin: true,
        Cmd: ["/bin/bash", "-c", `cat > "${filePath}"`],  // Use `cat` safely
    });

    // Start the process
    const streamBashSaveFileContent = await execBashSaveFileContent.start({ Detach: false, stdin: true });
    let outputBashSaveFileContent = "";
    streamBashSaveFileContent.on("data", (chunk) => {
      let chunkStr = chunk.toString().trim();
  
      // Remove leading control characters except newlines (\n)
      chunkStr = chunkStr.replace(/^[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/, ""); 
      
      outputBashSaveFileContent += chunkStr;
    });

    // Write new content and close stream properly
    let fileContentLines = fileContent.split("\n")
    console.log(`fileContentLines: ${fileContentLines}`)
    for (let fileContentLine of fileContentLines) {
      console.log(`fileContentLine: ${fileContentLine}`)
      streamBashSaveFileContent.write(fileContentLine + "\n");
    }
    // streamBashSaveFileContent.write(fileContent + "\n");
    streamBashSaveFileContent.end();

    await new Promise((resolve, reject) => {
      streamBashSaveFileContent.on("end", resolve);
      streamBashSaveFileContent.on("error", reject);
    });
    console.log(`saveFileContent outputBashSaveFileContent: ${outputBashSaveFileContent}`)
}


  async getFileContent(filePath: string): Promise<string | undefined> {

    if (!this.container) {
      return undefined;
    }

    // check if filePath is a file or a directory
    const execBashTestFileDir = await this.container.exec({
      AttachStdout: true,
      AttachStderr: true,
      Cmd: ["/bin/bash", "-c", `if test -f ${filePath}; then echo 'file exists'; else echo 'file not exists'; fi`],
    });

    const streamBash = await execBashTestFileDir.start({ Detach: false, stdin: true });
    let outputBashTestFileDir = "";
    streamBash.on("data", (chunk) => {
      outputBashTestFileDir += chunk.toString().trim();
    });
    await new Promise((resolve, reject) => {
        streamBash.on("end", resolve);
        streamBash.on("error", reject);
    });
    console.log(`getFileContent outputBashTestFileDir: ${outputBashTestFileDir}`)

    if (!outputBashTestFileDir.includes('file exists')) {
      return undefined
    }

    const execBashCatFile = await this.container.exec({
      AttachStdout: true,
      AttachStderr: true,
      Cmd: ["/bin/bash", "-c", `cat ${filePath}`],
    });

    const streamBashCatFile = await execBashCatFile.start({ Detach: false, stdin: true });
    let outputBashCatFile = "";
    streamBashCatFile.on("data", (chunk) => {
      let chunkStr = chunk.toString().trim();
  
      // Remove leading control characters except newlines (\n)
      chunkStr = chunkStr.replace(/^[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/, ""); 
      
      outputBashCatFile += chunkStr;
    });
    await new Promise((resolve, reject) => {
      streamBashCatFile.on("end", resolve);
      streamBashCatFile.on("error", reject);
    });
    console.log(`getFileContent outputBashCatFile: ${outputBashCatFile}`)

    return outputBashCatFile
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
    console.log(`outputBash: ${outputBash}`)

    let startIndex = outputBash.indexOf(basePath)
    outputBash = outputBash.substring(startIndex)

    /*
    new outputBash: /tmp
                    /tmp/sub1
                    /tmp/sub1/sub2
                    /tmp/sub1/sub2/abc2.txt
                    /tmp/sub1/abc1.txt
                    /tmp/sub2
                    /tmp/sub2/abc.txt
    */
    console.log(`new outputBash: ${outputBash}`)
    

    // Parse the `find` output into a dictionary
    const lines = outputBash.split("\n").filter((line) => line.trim() !== "");
    const folderStructure: any = {};

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

    return folderStructure
  }
}
