"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SHARD_INFO = exports.SHARD_NAMES = exports.RANGE = void 0;
const RANGE = 720;
exports.RANGE = RANGE;
const SHARD_NAMES = ["mysql-shard-test-1", "mysql-shard-test-2", "mysql-shard-test-3"];
exports.SHARD_NAMES = SHARD_NAMES;
const SHARD_INFO = {
    "mysql-shard-test-1": {
        host: "localhost",
        port: 4306,
        user: "root",
        pwd: "",
        database: "my_org_dev",
        numConnections: 1
    },
    "mysql-shard-test-2": {
        host: "localhost",
        port: 4307,
        user: "root",
        pwd: "",
        database: "my_org_dev",
        numConnections: 1
    },
    "mysql-shard-test-3": {
        host: "localhost",
        port: 4308,
        user: "root",
        pwd: "",
        database: "my_org_dev",
        numConnections: 1
    }
};
exports.SHARD_INFO = SHARD_INFO;
