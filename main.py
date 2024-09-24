from fastapi import FastAPI

from utils import is_open_source

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# post endpoint that takes a github url as a path param and return true if it is open source
@app.get("/github/{url}")
async def github(url: str):

    if is_open_source(url):
        return {"message": "Open Source"}
    else:
        return {"message": "Not Open Source"}
