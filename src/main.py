from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from sqlalchemy.orm import Session


from src.utils.utils import (
    get_first_line_of_readme,
    is_open_source,
    query_llm_to_improve_readme,
)

from src.db import models, crud, schemas
from src.db.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/is_open_source")
async def github(url: str = None):
    if url is None:
        return {"message": "No URL provided"}
    if is_open_source(url):
        return {"message": "Open Source"}
    return {"message": "Not Open Source"}


@app.get("/first_line_of_readme")
async def first_line_of_readme(url: str = None):
    if url is None:
        return {"message": "No URL provided"}
    first_line = get_first_line_of_readme(url)
    return {"message": first_line}


@app.post("/improve_readme")
def improve_readme_endpoint(url: str = None, db: Session = Depends(get_db)):
    query_response = query_llm_to_improve_readme(url)
    id = db.query(models.Readme).count() + 1
    original_readme = query_response.original_readme
    improved_readme = query_response.improved_readme
    llm_used = query_response.llm_used
    github_url = url
    timestamp = datetime.now()
    db_readme = crud.create_readme(
        db=db,
        readme=models.Readme(
            id=id,
            github_url=github_url,
            original_readme=original_readme,
            improved_readme=improved_readme,
            llm_used=llm_used,
            timestamp=timestamp,
        ),
    )
    return db_readme


@app.get("/stored_readmes", response_model=list[schemas.ReadmeCreate])
def get_stored_readmes(db: Session = Depends(get_db)):
    """Retrieve all stored READMEs."""
    readmes = crud.get_all_readmes(db)
    return readmes


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
