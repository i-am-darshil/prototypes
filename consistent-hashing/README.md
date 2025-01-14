- [ ] Let's assume the database is sharded into N shards. Start N MySQL docker containers ✅
- [ ] Have table like posts in all MySQL docker containers ✅
- [ ] Initialize TS project ✅
- [ ] Maintain connection pooling ✅
- [ ] Reads and Updates for database item should go to the right shard ✅
- [ ] Add a shard. Insert/Update/Delete for new shard should go to new shard. Reads go to new shard, if not found, fetch from old shard ✅
- [ ] Carry out data migration with NO DOWNTIME ✅

----

### Initialize TS project
1. `npm init -y`
2. `npm install --save-dev typescript`
3. `npx tsc --init`
4. `mkdir src`
5. `mkdir dist`
6. Modify tsconfig.json - rootDir, outDir, target, module, moduleResolution
7. Add a linter - `npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
8. Add a formatter - `npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier`
9. Add TS watcher `npm i -D tsc-watch`
10. `npm i -D ts-node-dev`
10. Add scripts to package.json

### Docker setup
To start a MySQL Docker container bound to a specific port, you can use the `docker run` command and specify the desired port mapping using the `-p` option. Here's how you can do it:


**Run the MySQL Container**:
Use the `docker run` command with the `-p` option to bind the container's MySQL port (default is `3306`) to a specific port on your host.

Example:
```bash
docker run -d --name=mysql-shard-test-1 -p 4306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=yes mysql:8.0.29-oracle mysqld --default-time-zone=$(sed -e "s/\(...\)\(..\)/\1:\2/" <<< `date "+%z"`)
```


### Step 1: Access the MySQL CLI
If you’ve started the MySQL Docker container (as described earlier), you can access the MySQL CLI using the following command:

```bash
docker exec -it mysql-shard-test-1 mysql -u root -p
```

Enter the root password when prompted (e.g., `my-secret-pw`).

---

### Step 2: Create a Database
Once inside the MySQL CLI, you can create the `my_org_dev` database:

```sql
CREATE DATABASE my_org_dev;
```

Verify the database was created:

```sql
SHOW DATABASES;
```

---

### Step 3: Switch to the `my_org_dev` Database
Use the database you just created:

```sql
USE my_org_dev;
```

---

### Step 4: Create the `posts` Table
Define the `posts` table with the desired schema:

```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT
);
```

---

### Step 5: Verify the Table Creation
Check the structure of the `posts` table to confirm it was created correctly:

```sql
DESCRIBE posts;
```

You should see output like this:

| Field       | Type         | Null | Key | Default | Extra          |
|-------------|--------------|------|-----|---------|----------------|
| id          | int          | NO   | PRI | NULL    | auto_increment |
| title       | varchar(255) | NO   |     | NULL    |                |
| description | text         | YES  |     | NULL    |                |

---

### Step 6: Exit the MySQL CLI
When you're done, you can exit the MySQL CLI:

```sql
EXIT;
```

---

