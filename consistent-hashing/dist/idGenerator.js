"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateId = generateId;
const startTime = Date.now();
function generateId(threadId) {
    let id = `${Date.now() - startTime}`;
    if (threadId)
        id += threadId;
    return id;
}
