MONGO DB NOTES
==============

# Using the Mongo Shell
--

To start the shell: "mongo"

Useful commands: 

```
use db, 
show dbs, 
show collections
```

Searches:

```
db.collection.find({query})
db.collection.find({query}).count()
db['collection'].find().limit(10)
```

# Creating a MongoDB Replica
--

1. configure replSet = <name> in all replica set members
2. take the expected master (the one which right now hosts the dbs) and create a 
replica set configuration

3. replica set config:

Set a config variable named cfg as follows:

	cfg = {"_id": "rs0", "members": [ {"_id": 0, "host":
	"mongodb_server:27017"}, {"_id": 1, "host": 
	"boson.i.labs.lacnic.net:27017"} ] }

4. initiate replicas
Run rs.initiate(cfg) on the master's mongo shell.

5. check operation
Run rs.status().

Statuses can be PRIMARY, RECOVERING, SECONDARY

6. enable eventually consistent reads
Run rs.slaveOk(true) once per shell session.


# Dump and restore
---

Dumping and restore are the preferred mechanisms for performing MongoDB backups.

