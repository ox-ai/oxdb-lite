
# api.log



## to start ox-db api 

### run directly from lib

```
uvicorn ox_engine.api.log:app  
```

### to run via file:

create file test.py

```py
from ox_engine.api import log

app = log.run()
```
run test.py by below command

```
uvicorn test:app --reload 
```
for testing on other device run

```
uvicorn test:app --reload 
ngrok http 127.0.0.1:8000
```