import { ConsistentHasher } from "./consistentHashing";
import { Post } from "./interfaces";
import { insert, flushAllShards, get } from "./models/PostModel";
import { ResultSetHeader, QueryResult } from "mysql2/promise";

async function testInserts(
  consistentHasher: ConsistentHasher,
  numInserts: number
): Promise<ResultSetHeader[]> {
  const insertResultPromises: Promise<any>[] = [];
  const insertResults: ResultSetHeader[] = [];
  for (let i = 0; i < numInserts; i++) {
    let insertResultPromise: Promise<any> = insert(
      consistentHasher,
      `My ${i} Post`,
      `This is the description: ${i}`
    )
      .then((value: any) => {
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

async function testReads(
  insertResults: ResultSetHeader[],
  consistentHasher: ConsistentHasher
) {
  for (let insertResult of insertResults) {
    let getResults: Post[] | undefined = await get(
      consistentHasher,
      insertResult.insertId
    );
    if (getResults) {
      if (getResults.length == 0) {
        console.log(
          `========== ERROR No results found for ${insertResult.insertId} ========== `
        );
      } else {
        for (let getResult of getResults) {
          console.log(
            `${getResult.id} ${getResult.title} ${getResult.description}`
          );
        }
      }
    }
  }
}

async function main() {
  const consistentHasher: ConsistentHasher = new ConsistentHasher(2);

  await flushAllShards(consistentHasher);

  const numInserts = 50;
  const insertResults: ResultSetHeader[] = await testInserts(
    consistentHasher,
    numInserts
  );

  console.log(
    `========== Number of inserts done: ${insertResults.length}. Reading them now ==========`
  );

  console.log(`========== Simulating addition of shard ==========`);
  consistentHasher.addShard(1);

  await testReads(insertResults, consistentHasher);

  await flushAllShards(consistentHasher);

  await consistentHasher.destroy();
}

main();
