from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/fixtures/{fixture_id}")
async def get_fixture(fixture_id: int):
    return {"fixture": fixture_id}

@app.get("/results/{date}")
async def get_results(date: str):
    return {"date": date}