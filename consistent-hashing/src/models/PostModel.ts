import {type Pool, type ResultSetHeader} from "mysql2/promise"
import { generateId } from "../utils"
import { type ConsistentHasher } from "../consistentHashing";
import { type consistentHasherShardResponse, type Post } from "../interfaces";

/* Lets say we want roughly increasing IDs.
Let's assume we are building instagram, and we are storing posts for it. 
We will be doing a lot of batch processing jobs on posts to find trending posts,
This will require fetching posts via pagination, i.e 0-100 posts, 100-200, etc

Since pur database is sharded, each database will start IDs from 1 if auto-increment.
Hence we need an ID generator that can generate roughly increasing IDs across all shards.
*/
async function insert(consistentHasher: ConsistentHasher, title: string, description: string): Promise<ResultSetHeader | undefined>{
  const id = generateId()
  console.log(`${id} ${title} ${description}`)
  const response: consistentHasherShardResponse = consistentHasher.getConnectionPoolForKey(`${id}`)
  let [result, _] = await response.connectionPool.query<ResultSetHeader>("INSERT INTO posts VALUES (?, ?, ?)", [id, title, description])
  return result
}

async function get(consistentHasher: ConsistentHasher, id: number, limit?:number): Promise<Post[] | undefined> {
  const response: consistentHasherShardResponse = consistentHasher.getConnectionPoolForKey(`${id}`)
  let query = "SELECT * FROM posts where id = ?" + (limit ? `limit ${limit}` : "")
  let [result, _] = await response.connectionPool.query<Post[]>(query, [id])

  if (result && result.length == 0) {
    let backupConnectionResponse = consistentHasher.getBackupConnectionPoolForShardNum(response.shardNum)
    if (backupConnectionResponse) {
      console.log(`Backing up get for ${id}, shardNum: ${response.shardNum}, backupShardNum: ${backupConnectionResponse.shardNum}`)
      let [result, _] = await backupConnectionResponse.connectionPool.query<Post[]>(query, [id])
      return result
    }
  }
  return result
}


async function flushAllShards(consistentHasher: ConsistentHasher): Promise<ResultSetHeader[] | undefined> {
  const results: ResultSetHeader[] = []
  for (let pool of consistentHasher.getAllConnectionPools()) {
    let [result, _] = await pool.query<ResultSetHeader>("DELETE FROM posts")
    results.push(result)
  }
  return results
}

export {
  insert, get, flushAllShards
}