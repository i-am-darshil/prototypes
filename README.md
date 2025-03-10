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

### Conflict Free Replicated Data Types - Last Write Wins Dictionary
- [ ] Understand Conflict Free Replica Data Types (CRDT) ✅
- [ ] Implement Last Write Wins Dictionary ✅
- [ ] Think of multithreading scenarios ✅
- [ ] Support lookup, add, remove & update operations ✅
- [ ] Implement Routing - GET, POST, PUT, DELETE ✅
- [ ] Add unit tests ✅

### Pessimistic & Optimistic Locking
- [ ] Understand Pessimistic & Optimistic Locking ✅
- [ ] Implement using SQL alchemy ✅
- [ ] Prototype it ✅

### Slack Prototype
#### Flask server
- [ ] Serves UI ✅
- [ ] Use to manage CRUD calls for users, channels, memberships ✅
- [ ] Use as connection manager to guide users to the websocket server ✅
- [ ] Upon receiving message, persist in database (slack prefers durability over latency as it is an enterprise application) ✅
- [ ] Upon persisting, put the message to redis pub/sub for websockets to consume ✅

#### Websocket server
- [ ] Spawn 2 websocket servers to mimic users from same channel connected to different servers ✅
- [ ] Send message to the relevant user subscribed to channel upon receiving message from pub/sub ✅
