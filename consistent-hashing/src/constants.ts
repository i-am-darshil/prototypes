import { type shardInfoType } from "./interfaces"

const RANGE = 720
const SHARD_NAMES = ["mysql-shard-test-1", "mysql-shard-test-2", "mysql-shard-test-3"]
const SHARD_INFO: {[key: string]: shardInfoType} = {
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
}

export {
  RANGE,
  SHARD_NAMES,
  SHARD_INFO
}