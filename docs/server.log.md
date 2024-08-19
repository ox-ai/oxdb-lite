# ox-db server

### access with client-server mode :

- in clien server mode need to start the server with command

```bash
oxdb.server --apikey "your-api-key" --host
```

- can use python client binding high level interfase code which is same as core db access refere [client.log](./docs/client.log.md)
- java script api coming soon u can directly acces using spi

- to start ox-db server run below commend refer [server.log.md](./docs/server.log.md)

### Linux , macos and Windows

- set path in terminal

```bash
#default apikey = "ox-db-prime"
export OXDB_API_KEY="test-apikey"
echo $OXDB_API_KEY

```

```bash
oxdb.server --apikey "hi0x" --host --port 8008
```

- if path not correctly assigned due too sudo or admin access use below cmd

```bash
python -m ox_db.server.log --apikey "hi0x" --host --port 8008
```
