from fastapi import FastAPI

app = FastAPI()

@app.get("/protection/activate")
async def activate():
    return {"message": "Activated"}

@app.get("/protection/deactivate")
async def activate():
    return {"message": "Activated"}from fastapi import FastAPI

app = FastAPI()

@app.get("/protection/activate")
async def activate():
    return {"message": "Activated"}

@app.get("/protection/deactivate")
async def activate():
    return {"message": "Activated"}