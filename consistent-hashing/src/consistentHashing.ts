import { RANGE, SHARD_INFO} from "./constants";
import { getConnectionPool } from "./mysqlConnectionPool";
import { getNumericHash } from "./utils";
import { type consistentHasherShardResponse, type Post } from "./interfaces";

import { type Pool, type ResultSetHeader } from 'mysql2/promise'

/*
To simulate adding shard, we initially consider having two shards.
SHARD_INFO has 3 shards, simulating when we added the shard, we added its config as well.
*/
export class ConsistentHasher {
  shardNumberToConnectionPoolMap: {[key: number]: Pool} = {}
  originalShardNumberToBackupShardNumber: {[key: number]: number} = {}
  shardNameToNumber: {[key: string]: number} = {}
  sortedShardNumbers: number[] = []
  connectionPools: Pool[] = []
  numShards:number
  shardNames:string[] = []

  constructor(numShards: number) {
    this.numShards = numShards
    if (this.numShards >= Object.keys(SHARD_INFO).length) {
      console.error("Not supported")
      return
    }
    this.shardNames = Object.keys(SHARD_INFO).slice(0, this.numShards)

    for (let shardname of this.shardNames) {
      const shardInfo = SHARD_INFO[shardname]
      this.connectionPools.push(
        getConnectionPool(shardInfo.host, shardInfo.port, shardInfo.user, shardInfo.pwd, shardInfo.database, shardInfo.numConnections)
      )
    }

    for (let i = 0; i < this.shardNames.length; i++) {
      const shardNumber = getNumericHash(this.shardNames[i], RANGE)
      this.sortedShardNumbers.push(shardNumber)
      this.shardNumberToConnectionPoolMap[shardNumber] = this.connectionPools[i]
      this.shardNameToNumber[this.shardNames[i]] = shardNumber
    }
    
    this.sortedShardNumbers.sort((a:number, b:number):number => a - b)
    console.log(this.sortedShardNumbers)
    console.log(this.shardNameToNumber)
    console.log(this.shardNames)
    console.log(this.numShards)
  }

  getConnectionPoolForKey(key: string): consistentHasherShardResponse {
    const hash = getNumericHash(key, RANGE);
    let start = 0
    let end = this.sortedShardNumbers.length - 1
    let shardIndex = start

    while (start <= end) {
      let mid: number = Math.floor((start + end) / 2)

      if (this.sortedShardNumbers[mid] < hash) {
        start = mid + 1
      } else {
        shardIndex = mid
        end = mid - 1
      }
    }

    if (start == this.sortedShardNumbers.length) {
      if (this.sortedShardNumbers[start] < hash) {
        shardIndex = 0
      }
    }

    console.log(`key: ${key}, hash: ${hash}, shardNumber: ${shardIndex}`)

    let res = {
      "shardNum": this.sortedShardNumbers[shardIndex],
      "connectionPool": this.shardNumberToConnectionPoolMap[this.sortedShardNumbers[shardIndex]]
    }

    return res
  }

  getBackupConnectionPoolForShardNum(shardNum: number): consistentHasherShardResponse | undefined {
    if (!(shardNum in this.originalShardNumberToBackupShardNumber)) {
      return undefined
    }
    let backupShardNum = this.originalShardNumberToBackupShardNumber[shardNum]
    let res = {
      "shardNum": backupShardNum,
      "connectionPool": this.shardNumberToConnectionPoolMap[backupShardNum]
    }
    return res
  }

  async destroy() {
    for (let i = 0; i < this.sortedShardNumbers.length; i++) {
      await this.connectionPools[i].end();
    }
  }

  async addShard(hotShardIndex: number) {
    if (this.numShards >= Object.keys(SHARD_INFO).length || hotShardIndex >= this.sortedShardNumbers.length) {
      console.error("Not supported")
      return
    }

    this.numShards += 1
    this.shardNames = Object.keys(SHARD_INFO).slice(0, this.numShards + 1)
    const shardInfo = SHARD_INFO[this.shardNames[this.numShards - 1]] // Since 0 indexed

    this.connectionPools.push(
      getConnectionPool(shardInfo.host, shardInfo.port, shardInfo.user, shardInfo.pwd, shardInfo.database, shardInfo.numConnections)
    )
    let shardNumber;
    if (hotShardIndex == 0) {
      shardNumber = Math.floor(this.sortedShardNumbers[hotShardIndex] / 2)
    } else {
      const diff = Math.floor((this.sortedShardNumbers[hotShardIndex] - this.sortedShardNumbers[hotShardIndex - 1]) / 2)
      shardNumber = this.sortedShardNumbers[hotShardIndex - 1] + diff
    }

    const oldShardNumber = this.sortedShardNumbers[hotShardIndex]
    this.originalShardNumberToBackupShardNumber[shardNumber] = oldShardNumber
    
    this.sortedShardNumbers.push(shardNumber)
    this.sortedShardNumbers.sort((a:number, b:number):number => a - b)
    this.shardNumberToConnectionPoolMap[shardNumber] = this.connectionPools[this.numShards - 1]

    this.shardNameToNumber[this.shardNames[this.numShards - 1]] = shardNumber

    
    console.log(`sortedShardNumbers: ${this.sortedShardNumbers}`)
    console.log(`shardNameToNumber: ${JSON.stringify(this.shardNameToNumber)}`)
    console.log(`shardNames: ${this.shardNames}`)
    console.log(`numShards: ${this.numShards}`)
    console.log(`ogShardNumberToBackupShardNumber: ${JSON.stringify(this.originalShardNumberToBackupShardNumber)}`)

    await this.migrateData(oldShardNumber, shardNumber)
  }

  /*
  This ensures NO downtime. 
  While we migrate the data (insert to new, delete from old), 
  the `gets` from DB are also routed to current shard identified. 
  If no results and a backup shard exists, query from backup shard
  */
  async migrateData(oldShard: number, newShard: number) {
    console.log(`========== Migration started from ${oldShard} to ${newShard}! ==========`)

    const oldShardPool: Pool = this.shardNumberToConnectionPoolMap[oldShard]
    const newShardPool: Pool = this.shardNumberToConnectionPoolMap[newShard]

    let [results, _] = await oldShardPool.query<Post[]>("SELECT * FROM posts") // Should paginate if big response
    let numResultsToMove: number = 0
    if (results && results.length > 0) {
      for (let result of results) {
        const shardResponse: consistentHasherShardResponse = this.getConnectionPoolForKey(`${result.id}`)
        if (shardResponse.shardNum == newShard) {
          numResultsToMove++;

          let [dbInsertResult, _] = await newShardPool.query<ResultSetHeader>("INSERT INTO posts VALUES (?, ?, ?)", [result.id, result.title, result.description])
          if (dbInsertResult && dbInsertResult.insertId) {
            let [dbDeleteResult, _] = await oldShardPool.query<ResultSetHeader>("DELETE FROM posts where id = ?", [dbInsertResult.insertId])
            if (dbDeleteResult && dbDeleteResult.affectedRows > 0) {
              console.log(`========== Insert to ${newShard} & Delete from ${oldShard} for ${result.id} is successful ==========`)
            }
          }
        }
      }
    }

    delete this.originalShardNumberToBackupShardNumber[newShard]
    console.log(`========== Migrated #${numResultsToMove} rows from ${oldShard} to ${newShard}! ==========`)

  }

  getAllConnectionPools(): Pool[] {
    return this.connectionPools;
  }
}