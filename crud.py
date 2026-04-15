import uuid
from typing import Optional
from sqlalchemy.orm import Session

from models import Software, Review


def cuid() -> str:
    return str(uuid.uuid4().hex[:24])


def get_all_software(db: Session):
    return db.query(Software).order_by(Software.createdAt.desc()).all()


def get_software_by_id(db: Session, id: str):
    return db.query(Software).filter(Software.id == id).first()


def get_software_by_name(db: Session, name: str):
    return db.query(Software).filter(Software.name == name).first()


def create_software(db: Session, name: str, description: str, website: Optional[str] = None):
    s = Software(
        id=cuid(),
        name=name.strip(),
        description=description.strip(),
        website=website.strip() if website else None,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def create_review(db: Session, software_id: str, name: str, rating: int, comment: str):
    r = Review(
        id=cuid(),
        softwareId=software_id,
        name=name.strip(),
        rating=rating,
        comment=comment.strip(),
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def get_average_rating(db: Session, software_id: str) -> Optional[float]:
    rows = db.query(Review).filter(Review.softwareId == software_id).all()
    if not rows:
        return None
    return sum(r.rating for r in rows) / len(rows)
