from fastapi import FastAPI
from .users.db import database, metadata, engine
from .users import routes

app = FastAPI()

metadata.create_all(engine)

app.include_router(routes.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI with PostgreSQL!"}

