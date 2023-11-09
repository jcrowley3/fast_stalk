import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import greenstalk
import json
import threading
import time


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting Survey Consumer...")
#     threading.Thread(target=worker, daemon=True).start()
#     yield
#     print("Consumer stopped!")


# # async def worker():
# def worker():
#     print("Starting Survey Consumer...")
#     conn = greenstalk.Client(('127.0.0.1', 11300), use="response_tube", watch="survey_tube")
#     while True:
#             print("Waiting for job...")
#             job = conn.reserve()
#             print("Got job!")
#             time.sleep(2)
#             job_data = json.loads(job.body)
#             print(job_data)
#             print("Deleting job...")
#             conn.delete(job)
#             print("Job deleted!")

# app = FastAPI(lifespan=lifespan)


# ASYNC VERSION ##
import asyncio
from async_stalk import Client
async def async_lifespan(app: FastAPI):
    print("Starting Survey Consumer...")
    task = asyncio.create_task(async_worker())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

async def async_worker():
    async with Client(('127.0.0.1', 11300), use="response_tube", watch="survey_tube") as conn:
        # print(f"Stats: {await conn.stats()}")
        print(f"Tube States: {await conn.stats_tube(tube='survey_tube')}")
        while True:
            print("Waiting for job...")
            job = await conn.reserve()
            print("Got job!")
            time.sleep(1)
            job_data = json.loads(job.body)
            print(job_data)
            print("Deleting job...")
            await conn.delete(job)
            print("Job deleted!")
            print("-"*20)

app = FastAPI(lifespan=async_lifespan)



@app.get("/")
async def root():
    return {"message": "Hello, world!"}



@app.get("/")
async def root():
    return {"message": "Hello, world!"}


# 'action' endpoint and function
@app.get("/health")
async def health():
    response = await health_action()
    return response


async def health_action():
    return {"Health message": "OK"}


if __name__ == "__main__":


    # should be running at port 8000
    uvicorn.run("main:app", workers=2, reload=True)
