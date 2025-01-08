import { loadConfig } from "./configParser.js";
import { LoadBalancer, RoundRobinStrategy, } from "./loadBalancer.js";
import { RateLimiter, TokenBucketStrategy, } from "./rateLimiter.js";
import { getLogger } from "./jsonLogger.js";
import { fork } from "child_process";
import * as http from "http";
import { v4 as uuidv4 } from "uuid";
const logger = getLogger("master");
async function main() {
    const config = await loadConfig("./config/config.yaml");
    logger.info(JSON.stringify(config));
    const workers = [];
    const localHostServers = [];
    const numWorkers = 4;
    const idToResponseObjectMap = {};
    const pathToHostMapping = {};
    const pathToLoadBalancerMapping = {};
    const tokenToRateLimiterMapping = {};
    for (let pathInfo of config.paths) {
        const path = pathInfo.path;
        const serverList = pathInfo.server;
        const serverInfos = config.servers.filter((s) => serverList.includes(s.name));
        // Load balancing strategy goes here
        if (serverInfos.length > 0) {
            pathToHostMapping[path] = serverInfos;
            const roundRobin = new RoundRobinStrategy(serverInfos);
            pathToLoadBalancerMapping[path] = new LoadBalancer(roundRobin);
        }
    }
    logger.info(`pathToHostMapping: ${JSON.stringify(pathToHostMapping)}`);
    logger.info(`pathToLoadBalancerMapping: ${JSON.stringify(pathToLoadBalancerMapping)}`);
    function sendResonse(statusCode, message, reqId) {
        const res = idToResponseObjectMap[reqId];
        const response = JSON.stringify({
            data: message,
        });
        res.writeHead(statusCode, {
            "Content-Type": "application/json",
        });
        res.end(response);
        logger.info(`${reqId} - ${statusCode} ${response}`);
        delete idToResponseObjectMap[reqId];
    }
    // Spawn Localhost Servers
    for (const server of config.servers) {
        if (server.host === "localhost") {
            const localHostServer = fork("./src/localHostServers.ts", {
                env: { port: `${server.port}` },
            });
            localHostServers.concat(localHostServer);
        }
    }
    // Spawn Workers
    for (let i = 0; i < numWorkers; i++) {
        const worker = fork("./src/worker.ts");
        workers.push(worker);
        worker.on("message", (message) => {
            const workerResponse = JSON.parse(message);
            sendResonse(workerResponse.statusCode, workerResponse.data, workerResponse.reqId);
        });
        worker.on("error", (err) => {
            logger.error(`Error in Worker ${i}:`, err);
        });
        worker.on("exit", (code) => {
            logger.info(`Worker ${i} exited with code ${code}`);
        });
    }
    const METHODS_WITH_REQUESTS = ["POST", "PATCH", "DELETE", "GET"];
    // Create the HTTP server
    const server = http.createServer((req, res) => {
        const url = req.url || "/";
        const matchedPathInfo = config.paths.filter((p) => url.startsWith(p.path));
        const reqId = uuidv4();
        idToResponseObjectMap[reqId] = res;
        let workerMessage;
        logger.info(`${reqId} - ${req.method} ${req.url} ${JSON.stringify(req.headers)}`);
        if (matchedPathInfo.length > 0) {
            const matchedPath = matchedPathInfo[0].path;
            const reqPath = url.replace(matchedPath, "");
            const serverInfos = pathToHostMapping[matchedPath];
            if (serverInfos.length > 0) {
                const loadBalancer = pathToLoadBalancerMapping[matchedPath];
                const serverInfo = loadBalancer.getHost();
                workerMessage = {
                    method: req.method || "GET",
                    reqPath: reqPath,
                    id: reqId,
                    serverInfo: serverInfo,
                };
            }
            else {
                sendResonse(404, `${url} not found`, reqId);
                return;
            }
        }
        else {
            sendResonse(404, `${url} not found`, reqId);
            return;
        }
        const workerIndex = Math.floor(Math.random() * numWorkers);
        const worker = workers[workerIndex];
        if (METHODS_WITH_REQUESTS.includes(`${req.method}`)) {
            let body = "";
            req.on("data", (chunk) => {
                body += chunk.toString();
            });
            req.on("end", () => {
                try {
                    const parsedBody = JSON.parse(body);
                    const token = parsedBody["x-token"];
                    logger.info(`${reqId} - ${body} ${token}`);
                    if (token) {
                        // ratelimiting goes in here
                        if (!(token in tokenToRateLimiterMapping)) {
                            tokenToRateLimiterMapping[token] = new RateLimiter(new TokenBucketStrategy(token, config.rate_limit.capacity, config.rate_limit.refillRate, config.rate_limit.refillIntervalInSec, config.rate_limit.maxSize));
                        }
                        if (tokenToRateLimiterMapping[token].isRateLimited()) {
                            sendResonse(400, JSON.stringify({ error: `Rate Limited for token ${token}` }), reqId);
                            return;
                        }
                        delete parsedBody.token;
                        workerMessage["body"] = JSON.stringify(parsedBody);
                        worker.send(JSON.stringify(workerMessage));
                    }
                    else {
                        sendResonse(429, JSON.stringify({ error: `No token passed` }), reqId);
                        return;
                    }
                }
                catch (err) {
                    sendResonse(400, JSON.stringify({ error: `Invalid JSON: ${body}` }), reqId);
                    return;
                }
            });
        }
        else {
            worker.send(JSON.stringify(workerMessage));
        }
    });
    server.listen(config.port, () => {
        console.log(`Master server listening on port ${config.port}`);
    });
}
main();
