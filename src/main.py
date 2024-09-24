from fastapi import FastAPI

from src.utils.utils import get_first_line_of_readme, is_open_source

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# post endpoint that takes a github url as a param and return true if it is open source
@app.get("/is_open_source")
async def github(url: str = None):
    if url is None:
        return {"message": "No URL provided"}
    else:
        if is_open_source(url):
            return {"message": "Open Source"}
        else:
            return {"message": "Not Open Source"}


@app.get("/first_line_of_readme")
async def first_line_of_readme(url: str = None):
    if url is None:
        return {"message": "No URL provided"}
    else:
        first_line = get_first_line_of_readme(url)
        return {"message": first_line}
