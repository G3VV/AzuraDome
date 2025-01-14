from fastapi import FastAPI
from util.protection import startProtection, stopProtection, protection_task
from util.monitor import startMonitor
import uvicorn
import threading
import asyncio

app = FastAPI()

@app.get("/protection/activate")
async def activate():
    response = await startProtection()
    return {"message": "activated"}

@app.get("/protection/deactivate")
async def activate():
    await stopProtection()
    return {"message": "deactivated"}

@app.get("/protection/status")
async def status():
    return {"status": "active" if protection_task is not None and not protection_task.done() else "inactive"}

@app.get("/")
async def root():
    await startMonitor()
    return "yes"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)