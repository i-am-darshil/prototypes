# prototypes

### Reverse Proxy
- [ ] Event-driven architecture ✅
- [ ] Use Master-Worker Process Pattern (like nginx uses) ✅
- [ ] Take YAML config ✅
- [ ] Implement Routing - GET, POST, PUT, DELETE ✅
- [ ] Implement Load Balancing ✅
- [ ] Implement Rate Limiting ✅
- [ ] Implement Logging ✅

### Consistent Hashing
- [ ] Let's assume the database is sharded into N shards. Start N MySQL docker containers ✅
- [ ] Have table like posts in all MySQL docker containers ✅
- [ ] Initialize TS project ✅
- [ ] Maintain connection pooling ✅
- [ ] Reads and Updates for database item should go to the right shard ✅
- [ ] Add a shard. Insert/Update/Delete for new shard should go to new shard. Reads go to new shard, if not found, fetch from old shard ✅
- [ ] Carry out data migration with NO DOWNTIME ✅
