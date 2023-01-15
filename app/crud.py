from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def auth(db: Session, login: str, password: str):
    return db.query(models.User).filter(models.User.login == login).filter(models.User.password == password).first()