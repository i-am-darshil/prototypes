class TokenBucketStrategy {
    key;
    capacity;
    refillRate;
    refillIntervalInSec;
    lastUsedTimeStamp;
    bucketSize;
    maxBucketSize;
    lastBucketRefill;
    constructor(key, capacity, refillRate, refillIntervalInSec, maxSize) {
        this.key = key;
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.refillIntervalInSec = refillIntervalInSec;
        this.bucketSize = maxSize;
        this.maxBucketSize = maxSize;
        this.lastUsedTimeStamp = Date.now();
        this.lastBucketRefill = Date.now();
    }
    isRateLimited() {
        const currentTimeStamp = Date.now();
        if (currentTimeStamp - this.lastBucketRefill >
            this.refillIntervalInSec * 1000) {
            this.bucketSize = this.maxBucketSize;
            this.lastBucketRefill = currentTimeStamp;
        }
        else {
            const secondsSinceLastUse = (currentTimeStamp - this.lastUsedTimeStamp) / 1000;
            this.bucketSize = Math.min(this.maxBucketSize, Math.floor(this.bucketSize +
                (secondsSinceLastUse * this.refillRate) / this.refillIntervalInSec));
        }
        this.lastUsedTimeStamp = currentTimeStamp;
        this.bucketSize -= 1;
        return this.bucketSize < 0;
    }
}
class RateLimiter {
    strategy;
    constructor(strategy) {
        this.strategy = strategy;
    }
    isRateLimited() {
        return this.strategy.isRateLimited();
    }
}
export { RateLimiter, TokenBucketStrategy };
