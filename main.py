from fastapi import FastAPI
from routes import task

server = FastAPI()
server.include_router(task.router)