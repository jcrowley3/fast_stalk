import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
# import greenstalk
import json
import threading
import time
import asyncio
import aiostalk


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Survey Consumer...")
    task = asyncio.create_task(worker())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


async def worker():
    print("Starting Survey Consumer...")
    # conn = greenstalk.Client(('127.0.0.1', 11300), use="response_tube", watch="survey_tube")
    async with aiostalk.Client(('127.0.0.1', 11300), use="response_tube", watch="survey_tube") as conn:
        while True:
            print(f"Stats: {await conn.stats()}")
            print("Waiting for job...")
            job = await conn.reserve()
            print("Got job!")
            time.sleep(2)
            job_data = json.loads(job.body)
            print(job_data)
            print("Deleting job...")
            await conn.delete(job)
            print("Job deleted!")
    print("Consumer stopped!")


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


# 'action' endpoint and function
@app.get("/health")
async def health():
    response = health_action()
    return response


async def health_action():
    return {"Health message": "OK"}


if __name__ == "__main__":
    # should be running at port 8000
    uvicorn.run("main:app", workers=1, reload=True)
