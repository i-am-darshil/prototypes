import { type ServerInfo } from "./configParser.js";

abstract class Strategy {
  hosts: ServerInfo[];

  constructor(hosts: ServerInfo[]) {
    this.hosts = hosts;
  }

  abstract getHost(): ServerInfo;
}

class RoundRobinStrategy extends Strategy {
  lastIndex: number = -1;

  getHost(): ServerInfo {
    this.lastIndex = this.lastIndex + 1;
    return this.hosts[this.lastIndex % this.hosts.length];
  }
}

class LoadBalancer {
  strategy: Strategy;
  constructor(strategy: Strategy) {
    this.strategy = strategy;
  }

  getHost(): ServerInfo {
    return this.strategy.getHost();
  }
}

export { Strategy, RoundRobinStrategy, LoadBalancer };
