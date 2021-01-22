from fastapi import FastAPI

from app import method

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": f"World - {method.just_some_method()}"}
