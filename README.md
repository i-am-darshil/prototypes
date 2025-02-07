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

### Cloud IDE like Repl.it
- [ ] Basic UI - Home Page, Folder structure, code editor, terminal. ✅
- [ ] On Home Page, show past projects and create project. ✅
- [ ] On create project, start a docker container for the type of project like python, node, etc. ✅
- [ ] For a past active project, start that particular docker container. Ideally, would need to handle initialising the container with the file system, packages. Currently out of scope. ✅
- [ ] Commands in terminal should be relayed to the terminal in docker container. ✅
- [ ] Real time code updates should be persisted in local file system (ideally to s3 periodically as well) and is mounted to docker container to keep things simple. ✅
