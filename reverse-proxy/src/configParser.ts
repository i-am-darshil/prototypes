import * as yaml from "js-yaml";
import { promises as fs } from "fs";
import { z } from "zod";

const serverSchema = z.object({
  name: z.string(),
  host: z.string(),
  port: z.number(),
  protocol: z.string(),
  prepath: z.string().optional(),
});

const configSchema = z.object({
  port: z.number().default(3000),
  servers: z.array(serverSchema),
  paths: z.array(
    z.object({
      path: z.string(),
      server: z.array(z.string()),
    })
  ),
  rate_limit: z.object({
    strategy: z.string().default("TokenBucketStrategy"),
    capacity: z.number().default(10),
    refillRate: z.number().default(1),
    refillIntervalInSec: z.number().default(10),
    maxSize: z.number().default(2),
  }),
});

type Config = z.infer<typeof configSchema>;
type ServerInfo = z.infer<typeof serverSchema>;

async function loadConfig(filePath: string): Promise<Config> {
  try {
    const file = await fs.readFile(filePath, "utf8");
    const data = yaml.load(file);
    return configSchema.parse(data);
  } catch (error) {
    throw new Error(`Failed to load config file: ${error}`);
  }
}

export { loadConfig, type Config, type ServerInfo };
