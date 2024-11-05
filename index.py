from fastapi import FastAPI
from util.protection import startProtection, stopProtection
import uvicorn

app = FastAPI()

@app.get("/protection/activate")
async def activate():
    response = await startProtection()
    return {"message": "activated"}

@app.get("/protection/deactivate")
async def activate():
    await stopProtection()
    return {"message": "deactivated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)