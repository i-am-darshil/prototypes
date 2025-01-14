"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const consistentHashing_1 = require("./consistentHashing");
const PostModel_1 = require("./models/PostModel");
async function testInserts(consistentHasher, numInserts) {
    const insertResultPromises = [];
    const insertResults = [];
    for (let i = 0; i < numInserts; i++) {
        let insertResultPromise = (0, PostModel_1.insert)(consistentHasher, `My ${i} Post`, `This is the description: ${i}`)
            .then((value) => {
            insertResults.push(value);
        })
            .catch((msg) => {
            console.error(msg);
        });
        insertResultPromises.push(insertResultPromise);
    }
    await Promise.all(insertResultPromises);
    return insertResults;
}
async function testReads(insertResults, consistentHasher) {
    for (let insertResult of insertResults) {
        let getResults = await (0, PostModel_1.get)(consistentHasher, insertResult.insertId);
        if (getResults) {
            if (getResults.length == 0) {
                console.log(`========== ERROR No results found for ${insertResult.insertId} ========== `);
            }
            else {
                for (let getResult of getResults) {
                    console.log(`${getResult.id} ${getResult.title} ${getResult.description}`);
                }
            }
        }
    }
}
async function main() {
    const consistentHasher = new consistentHashing_1.ConsistentHasher(2);
    await (0, PostModel_1.flushAllShards)(consistentHasher);
    const numInserts = 50;
    const insertResults = await testInserts(consistentHasher, numInserts);
    console.log(`========== Number of inserts done: ${insertResults.length}. Reading them now ==========`);
    console.log(`========== Simulating addition of shard ==========`);
    consistentHasher.addShard(1);
    await testReads(insertResults, consistentHasher);
    await (0, PostModel_1.flushAllShards)(consistentHasher);
    await consistentHasher.destroy();
}
main();
