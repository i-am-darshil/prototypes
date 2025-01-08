class Strategy {
    hosts;
    constructor(hosts) {
        this.hosts = hosts;
    }
}
class RoundRobinStrategy extends Strategy {
    lastIndex = -1;
    getHost() {
        this.lastIndex = this.lastIndex + 1;
        return this.hosts[this.lastIndex % this.hosts.length];
    }
}
class LoadBalancer {
    strategy;
    constructor(strategy) {
        this.strategy = strategy;
    }
    getHost() {
        return this.strategy.getHost();
    }
}
export { Strategy, RoundRobinStrategy, LoadBalancer };
