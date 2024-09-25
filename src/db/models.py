from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    func,
)

from .database import Base


class Readme(Base):
    __tablename__ = "readmes"

    id = Column(Integer, primary_key=True)
    github_url = Column(String, index=True)  # URL of the GitHub repository
    original_readme = Column(Text)  # The original README content
    improved_readme = Column(Text)  # The improved README content
    llm_used = Column(String)  # The LLM model used to generate the improved README
    timestamp = Column(
        DateTime, default=func.now()
    )  # Timestamp of when the README was generated
