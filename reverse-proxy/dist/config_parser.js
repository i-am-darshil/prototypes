import * as yaml from "js-yaml";
import { promises as fs } from "fs";
import { z } from "zod";
const configSchema = z.object({
    port: z.number().default(3000),
    servers: z.array(z.object({
        name: z.string(),
        host: z.string(),
        prepath: z.string().optional(),
    })),
    paths: z.array(z.object({
        path: z.string(),
        server: z.string(),
    })),
    rate_limit: z.object({
        max_requests: z.number().default(10),
        time_window: z.number().default(10),
    }),
    cache: z.object({
        enabled: z.boolean().default(false),
        ttl: z.number().default(60),
    }),
    health_check: z.object({
        enabled: z.boolean().default(false),
        interval: z.number().default(10),
        timeout: z.number().default(5),
    }),
    logging: z.object({
        enabled: z.boolean().default(false),
        level: z.string().default("info"),
        format: z.string().default("json"),
    }),
});
async function loadConfig(filePath) {
    try {
        const file = await fs.readFile(filePath, "utf8");
        const data = yaml.load(file);
        return configSchema.parse(data);
    }
    catch (error) {
        throw new Error(`Failed to load config file: ${error}`);
    }
}
export { loadConfig, };
