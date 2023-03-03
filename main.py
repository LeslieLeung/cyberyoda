import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from cyberyoda.route import route

app = FastAPI()

# load config
load_dotenv()

route.register_route(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000)
