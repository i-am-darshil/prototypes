"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.testDB = testDB;
async function testDB(pool) {
    try {
        const rowsBefore = await pool.execute('SELECT * FROM posts');
        console.log('rowsBefore Posts:', rowsBefore);
        const insertResult = await pool.execute('INSERT INTO posts (title, description) VALUES (?, ?)', ['My First Post', 'This is the description']);
        console.log("insertResult: ", insertResult);
        const rowsAfter = await pool.execute('SELECT * FROM posts');
        console.log('rowsAfter Posts:', rowsAfter);
        const deleteResult = await pool.execute('DELETE from posts');
        console.log("deleteResult: ", deleteResult);
    }
    catch (err) {
        console.error('Error querying the database:', err);
    }
}
