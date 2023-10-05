from sqlalchemy import update, and_, text
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from . import models, schemas


def get_users(db: Session) -> List[schemas.User]:
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.User):
    db.add(models.User(**user.dict()))
    db.commit()
    return user


def get_user_logs(db: Session) -> List[schemas.UserLog]:
    return db.query(models.UserLog).order_by(
        models.UserLog.checkin_date.desc(),
        models.UserLog.time_in.desc(),
        models.UserLog.time_out.asc(),
    ).all()


def get_user_by_card_id(db: Session, card_id: str) -> Optional[schemas.User]:
    return db.query(models.User).where(models.User.card_id == card_id).scalar()


def check_card_in_user_logs(db: Session, user_id: str) -> Optional[schemas.UserLog]:
    return db.query(models.UserLog).where(and_(models.UserLog.user_id == user_id, models.UserLog.time_out == None)).scalar()


def get_user_log_by_id(db: Session, id: int):
    return db.query(models.UserLog).where(models.UserLog.id == id).scalar()


def checkin_user(db: Session, user_checkin: schemas.UserCheckin):
    db_user_checkin = models.UserLog(**user_checkin.dict(exclude_none=True))
    db.add(db_user_checkin)
    db.commit()
    db.refresh(db_user_checkin)
    return get_user_log_by_id(db=db, id=db_user_checkin.id)


def checkout_user(db: Session, id: int):
    statement = update(models.UserLog).where(and_(models.UserLog.id == id, models.UserLog.time_out == None)).values(
        {'time_out': datetime.now().strftime('%H:%M:%S')}).execution_options(synchronize_session='fetch')
    db.execute(statement)
    db.commit()
    return get_user_log_by_id(db=db, id=id)


def truncate_user_logs(db: Session):
    db.execute(text("delete from user_logs"))
    db.commit()
    return "chac oke"
