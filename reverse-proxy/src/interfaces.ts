import { type ServerInfo } from "./configParser";
import { ServerResponse } from "http";

export interface WorkerMessageType {
  method: string;
  reqPath: string;
  body?: string;
  id: string;
  serverInfo: ServerInfo;
}

export interface WorkerResponseType {
  statusCode: number;
  data: string;
  reqId: string;
}
