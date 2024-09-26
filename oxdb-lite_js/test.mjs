import {Oxdb ,pushData} from "./db/log.js"
const db = new Oxdb("http://127.0.0.1:8000");
const result = await db.push(pushData);
console.log(result)