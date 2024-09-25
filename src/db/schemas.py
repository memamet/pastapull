from pydantic import BaseModel
from datetime import datetime


class ReadmeBase(BaseModel):
    id: int
    github_url: str

    class Config:
        orm_mode = True  # Allow compatibility with ORM models


class ReadmeCreate(ReadmeBase):
    original_readme: str
    improved_readme: str
    llm_used: str
    timestamp: datetime
