import mysql from 'mysql2/promise';

export function getConnectionPool(host: string, port: number, user: string, password: string, database: string, connectionLimit: number): mysql.Pool {
  // Create a connection pool
  const pool = mysql.createPool({
    host: host,
    port: port,
    user: user,
    password: password,
    database: database,
    waitForConnections: true,
    connectionLimit: connectionLimit,      // Maximum number of connections in the pool
    // queueLimit: 0,
    connectTimeout: 10000,   // 10 seconds
    enableKeepAlive: true
  });

  return pool
}


