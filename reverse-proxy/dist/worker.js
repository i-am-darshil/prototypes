import https from "https";
import http from "http";
import { getLogger } from "./jsonLogger.js";
const logger = getLogger(`worker:${process.pid}`);
logger.info(`Worker started with PID:${process.pid}`);
process.on("message", (message) => {
    const workerMessage = JSON.parse(message);
    const serverInfo = workerMessage.serverInfo;
    const options = {
        hostname: serverInfo.host,
        port: serverInfo.port,
        path: serverInfo.prepath
            ? serverInfo.prepath + workerMessage.reqPath
            : workerMessage.reqPath,
        method: workerMessage.method,
        headers: {
            "Content-Type": "application/json",
        },
    };
    if (!options.path.startsWith("/")) {
        options.path = "/" + options.path;
    }
    const protocol = serverInfo.protocol === "https" ? https : http;
    const req = protocol.request(options, (res) => {
        let responseBody = "";
        res.on("data", (chunk) => {
            responseBody += chunk;
        });
        res.on("end", () => {
            logger.info(`${workerMessage.id} - Response for ${options.method} ${options.hostname} ${options.path} using ${serverInfo.protocol}: ${res.statusCode} - ${responseBody}`);
            try {
                responseBody = JSON.parse(responseBody);
            }
            catch { }
            const responseMessage = {
                statusCode: res.statusCode ? res.statusCode : 200,
                data: responseBody,
                reqId: workerMessage.id,
            };
            // Send a message back to the master
            if (process.send) {
                process.send(JSON.stringify(responseMessage));
            }
        });
    });
    req.on("error", (err) => {
        const responseMessage = {
            statusCode: 500,
            data: err.message,
            reqId: workerMessage.id,
        };
        logger.error(`${workerMessage.id} - Error for ${options.method} ${options.path}: ${err.message}`);
        if (process.send) {
            process.send(JSON.stringify(responseMessage));
        }
    });
    if (workerMessage.body) {
        req.write(workerMessage.body); // Send data for POST/PUT requests
    }
    req.end();
});
