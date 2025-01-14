import {type Pool, type RowDataPacket} from 'mysql2/promise'

type shardInfoType = {
  host: string,
  port: number,
  user: string,
  pwd: string,
  database: string,
  numConnections: number,
}

type consistentHasherShardResponse = {
  shardNum: number,
  connectionPool: Pool
}

interface Post extends RowDataPacket {
  id: number;
  title: string;
  description: string;
}

export {
  shardInfoType,
  consistentHasherShardResponse,
  Post
}