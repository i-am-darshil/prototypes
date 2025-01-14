"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.testDB = testDB;
const PostModel_1 = require("../models/PostModel");
async function testDB(pool, poolId) {
    try {
        console.log(`TEST START pool: ${poolId}----`);
        let deleteResultStart = await (0, PostModel_1.deleteAll)(pool);
        console.log(`deleteResultStart: ${JSON.stringify(deleteResultStart)}`);
        let getBeforeInsert = await (0, PostModel_1.getAll)(pool);
        console.log(`getBeforeInsert: ${JSON.stringify(getBeforeInsert)}`);
        let insertResult = await (0, PostModel_1.insert)(pool, 'My First Post', 'This is the description');
        console.log(`insertResult: ${JSON.stringify(insertResult)}`);
        let getAfterInsert = await (0, PostModel_1.getAll)(pool);
        console.log(`getAfterInsert: ${JSON.stringify(getAfterInsert)}`);
        let deleteResultEnd = await (0, PostModel_1.deleteAll)(pool);
        console.log(`deleteResultEnd: ${JSON.stringify(deleteResultEnd)}`);
        console.log(`TEST END pool: ${poolId}----`);
    }
    catch (err) {
        console.error('Error querying the database:', err);
    }
}
