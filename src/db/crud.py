from sqlalchemy.orm import Session
from . import models, schemas


def get_readme_by_url(db: Session, github_url: str):
    """Get a README by its GitHub URL."""
    return (
        db.query(models.Readme).filter(models.Readme.github_url == github_url).first()
    )


def get_all_readmes(db: Session, skip: int = 0, limit: int = 100):
    """Get all README entries with pagination."""
    return db.query(models.Readme).offset(skip).limit(limit).all()


def create_readme(db: Session, readme: schemas.ReadmeCreate):
    """Create a new README entry."""
    db_readme = models.Readme(
        github_url=readme.github_url,
        original_readme=readme.original_readme,
        improved_readme=readme.improved_readme,
        llm_used=readme.llm_used,
    )
    db.add(db_readme)
    db.commit()
    db.refresh(db_readme)
    return db_readme
