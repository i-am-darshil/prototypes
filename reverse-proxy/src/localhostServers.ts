import * as http from "http";
import { getLogger } from "./jsonLogger.js";

async function main() {
  let port = 3001;
  if (process.env.port) {
    port = parseInt(process.env.port);
  }

  const logger = getLogger(`localHostServer:${port}`);

  const server = http.createServer(
    (req: http.IncomingMessage, res: http.ServerResponse) => {
      logger.info(req.method ? req.method : "", req.url);

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          data: `You have reached port ${port} for ${req.method} ${req.url}`,
        })
      );
    }
  );

  server.listen(port, () => {
    logger.info(`Local Host server listening on port ${port}`);
  });
}

main();
