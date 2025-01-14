"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getConnectionPool = getConnectionPool;
const promise_1 = __importDefault(require("mysql2/promise"));
function getConnectionPool(host, port, user, password, database, connectionLimit) {
    // Create a connection pool
    const pool = promise_1.default.createPool({
        host: host,
        port: port,
        user: user,
        password: password,
        database: database,
        waitForConnections: true,
        connectionLimit: connectionLimit, // Maximum number of connections in the pool
        // queueLimit: 0,
        connectTimeout: 10000, // 10 seconds
        enableKeepAlive: true
    });
    return pool;
}
