import { RANGE, } from "./constants";
import * as crypto from 'crypto';

const startTime = Date.now()

/*
We set ID to be int in DB -> 32 bits
22 MSB bits for time - We can run this for at max 2^22 milliseconds to ensure unique IDa
10 bits for threadId - We can have at max 2^10 threads to ensure unique IDa
*/
const MAX_TIME_BITS = 2 ** 22; // 22-bit limit (2**22 milliseconds or ~1.17 hours)
const MAX_THREAD_ID = 2 ** 10;  // 10-bit limit (1024 threads)

function generateId(threadId: number = Math.floor(Math.random() * MAX_THREAD_ID)): number {
  const currentTime = ((Date.now() - startTime) % MAX_TIME_BITS); // Wrap time to 22 bits

  if (!threadId) {
    threadId = Math.floor(Math.random() * MAX_THREAD_ID)
  }

  // Validate threadId to ensure it's within 10-bit range
  if (threadId >= MAX_THREAD_ID || threadId < 0) {
    throw new Error(`Thread ID must be between 0 and ${MAX_THREAD_ID - 1}`);
  }

  // Pack time (24 MSB) and threadId (10 LSB) into a 32-bit integer
  const id = ((currentTime << 10) | threadId) >>> 0; // Convert to unsigned 32-bit integer;

  return id;
}


function getNumericHash(input: string, range: number): number {
  // Generate MD5 hash
  const hash = crypto.createHash("md5").update(input).digest("hex");

  // Convert the hash (hexadecimal) into a numeric value
  const numericHash = parseInt(hash.slice(0, 8), 16); // Use first 8 characters to avoid overflow

  // Restrict the value within the range [0, range)
  return numericHash % range;
}


export {
  generateId,
  getNumericHash
}