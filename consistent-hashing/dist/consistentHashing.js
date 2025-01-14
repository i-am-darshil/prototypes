"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConsistentHasher = void 0;
const constants_1 = require("./constants");
const mysqlConnectionPool_1 = require("./mysqlConnectionPool");
const utils_1 = require("./utils");
/*
To simulate adding shard, we initially consider having two shards.
SHARD_INFO has 3 shards, simulating when we added the shard, we added its config as well.
*/
class ConsistentHasher {
    shardNumberToConnectionPoolMap = {};
    originalShardNumberToBackupShardNumber = {};
    shardNameToNumber = {};
    sortedShardNumbers = [];
    connectionPools = [];
    numShards;
    shardNames = [];
    constructor(numShards) {
        this.numShards = numShards;
        if (this.numShards >= Object.keys(constants_1.SHARD_INFO).length) {
            console.error("Not supported");
            return;
        }
        this.shardNames = Object.keys(constants_1.SHARD_INFO).slice(0, this.numShards);
        for (let shardname of this.shardNames) {
            const shardInfo = constants_1.SHARD_INFO[shardname];
            this.connectionPools.push((0, mysqlConnectionPool_1.getConnectionPool)(shardInfo.host, shardInfo.port, shardInfo.user, shardInfo.pwd, shardInfo.database, shardInfo.numConnections));
        }
        for (let i = 0; i < this.shardNames.length; i++) {
            const shardNumber = (0, utils_1.getNumericHash)(this.shardNames[i], constants_1.RANGE);
            this.sortedShardNumbers.push(shardNumber);
            this.shardNumberToConnectionPoolMap[shardNumber] = this.connectionPools[i];
            this.shardNameToNumber[this.shardNames[i]] = shardNumber;
        }
        this.sortedShardNumbers.sort((a, b) => a - b);
        console.log(this.sortedShardNumbers);
        console.log(this.shardNameToNumber);
        console.log(this.shardNames);
        console.log(this.numShards);
    }
    getConnectionPoolForKey(key) {
        const hash = (0, utils_1.getNumericHash)(key, constants_1.RANGE);
        let start = 0;
        let end = this.sortedShardNumbers.length - 1;
        let shardIndex = start;
        while (start <= end) {
            let mid = Math.floor((start + end) / 2);
            if (this.sortedShardNumbers[mid] < hash) {
                start = mid + 1;
            }
            else {
                shardIndex = mid;
                end = mid - 1;
            }
        }
        if (start == this.sortedShardNumbers.length) {
            if (this.sortedShardNumbers[start] < hash) {
                shardIndex = 0;
            }
        }
        console.log(`key: ${key}, hash: ${hash}, shardNumber: ${shardIndex}`);
        let res = {
            "shardNum": this.sortedShardNumbers[shardIndex],
            "connectionPool": this.shardNumberToConnectionPoolMap[this.sortedShardNumbers[shardIndex]]
        };
        return res;
    }
    getBackupConnectionPoolForShardNum(shardNum) {
        if (!(shardNum in this.originalShardNumberToBackupShardNumber)) {
            return undefined;
        }
        let backupShardNum = this.originalShardNumberToBackupShardNumber[shardNum];
        let res = {
            "shardNum": backupShardNum,
            "connectionPool": this.shardNumberToConnectionPoolMap[backupShardNum]
        };
        return res;
    }
    async destroy() {
        for (let i = 0; i < this.sortedShardNumbers.length; i++) {
            await this.connectionPools[i].end();
        }
    }
    async addShard(hotShardIndex) {
        if (this.numShards >= Object.keys(constants_1.SHARD_INFO).length || hotShardIndex >= this.sortedShardNumbers.length) {
            console.error("Not supported");
            return;
        }
        this.numShards += 1;
        this.shardNames = Object.keys(constants_1.SHARD_INFO).slice(0, this.numShards + 1);
        const shardInfo = constants_1.SHARD_INFO[this.shardNames[this.numShards - 1]]; // Since 0 indexed
        this.connectionPools.push((0, mysqlConnectionPool_1.getConnectionPool)(shardInfo.host, shardInfo.port, shardInfo.user, shardInfo.pwd, shardInfo.database, shardInfo.numConnections));
        let shardNumber;
        if (hotShardIndex == 0) {
            shardNumber = Math.floor(this.sortedShardNumbers[hotShardIndex] / 2);
        }
        else {
            const diff = Math.floor((this.sortedShardNumbers[hotShardIndex] - this.sortedShardNumbers[hotShardIndex - 1]) / 2);
            shardNumber = this.sortedShardNumbers[hotShardIndex - 1] + diff;
        }
        const oldShardNumber = this.sortedShardNumbers[hotShardIndex];
        this.originalShardNumberToBackupShardNumber[shardNumber] = oldShardNumber;
        this.sortedShardNumbers.push(shardNumber);
        this.sortedShardNumbers.sort((a, b) => a - b);
        this.shardNumberToConnectionPoolMap[shardNumber] = this.connectionPools[this.numShards - 1];
        this.shardNameToNumber[this.shardNames[this.numShards - 1]] = shardNumber;
        console.log(`sortedShardNumbers: ${this.sortedShardNumbers}`);
        console.log(`shardNameToNumber: ${JSON.stringify(this.shardNameToNumber)}`);
        console.log(`shardNames: ${this.shardNames}`);
        console.log(`numShards: ${this.numShards}`);
        console.log(`ogShardNumberToBackupShardNumber: ${JSON.stringify(this.originalShardNumberToBackupShardNumber)}`);
        await this.migrateData(oldShardNumber, shardNumber);
    }
    /*
    This ensures NO downtime.
    While we migrate the data (insert to new, delete from old),
    the `gets` from DB are also routed to current shard identified.
    If no results and a backup shard exists, query from backup shard
    */
    async migrateData(oldShard, newShard) {
        console.log(`========== Migration started from ${oldShard} to ${newShard}! ==========`);
        const oldShardPool = this.shardNumberToConnectionPoolMap[oldShard];
        const newShardPool = this.shardNumberToConnectionPoolMap[newShard];
        let [results, _] = await oldShardPool.query("SELECT * FROM posts"); // Should paginate if big response
        let numResultsToMove = 0;
        if (results && results.length > 0) {
            for (let result of results) {
                const shardResponse = this.getConnectionPoolForKey(`${result.id}`);
                if (shardResponse.shardNum == newShard) {
                    numResultsToMove++;
                    let [dbInsertResult, _] = await newShardPool.query("INSERT INTO posts VALUES (?, ?, ?)", [result.id, result.title, result.description]);
                    if (dbInsertResult && dbInsertResult.insertId) {
                        let [dbDeleteResult, _] = await oldShardPool.query("DELETE FROM posts where id = ?", [dbInsertResult.insertId]);
                        if (dbDeleteResult && dbDeleteResult.affectedRows > 0) {
                            console.log(`========== Insert to ${newShard} & Delete from ${oldShard} for ${result.id} is successful ==========`);
                        }
                    }
                }
            }
        }
        delete this.originalShardNumberToBackupShardNumber[newShard];
        console.log(`========== Migrated #${numResultsToMove} rows from ${oldShard} to ${newShard}! ==========`);
    }
    getAllConnectionPools() {
        return this.connectionPools;
    }
}
exports.ConsistentHasher = ConsistentHasher;
