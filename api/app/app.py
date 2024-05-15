from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def app_index():
    return {"Hello": "World"}