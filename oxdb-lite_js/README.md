# ox-db_lite.js

> not developed yet this js binding to oxdb-lite is not stable

## ox-db :


## Installation:

always build from source for latest and bug free version

> note : install [ox-doc](https://github.com/ox-ai/ox-doc.git) and [ox-db](https://github.com/ox-ai/ox-db.git) before installing ox-db

### pre requisite
+ refere **[ox-db](https://github.com/ox-ai/ox-db.git)** the core server for more imformation on installing server **[ox-db](https://github.com/ox-ai/ox-db.git)** and **[ox-doc](https://github.com/ox-ai/ox-doc.git)**  and documentation

#### build from source

```
pip install git+https://github.com/ox-ai/ox-doc.git
pip install git+[ox-db](https://github.com/ox-ai/ox-db.git)
```
### ox-db.js buinding lib

```
npm install git+https://github.com/ox-ai/ox-db.js.git
```

## usage :

### server :

to srart server run below cmd 
```
uvicorn ox_db.api.log:app
```

### code-snipet :

```js
import {Oxdb ,pushData} from "ox-db"

const db = new Oxdb("http://127.0.0.1:8000");

const result = await db.push(pushData);

console.log(result)
```
