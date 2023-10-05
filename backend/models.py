import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True)
    card_id = Column(String(255), unique=True)
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(255))
    image_url = Column(String(255))
    gender = Column(String(255))
    dob = Column(String(255))
    # created = Column(DateTime, default=datetime.datetime.now())

    user_logs = relationship("UserLog", back_populates="user")

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class UserLog(Base):
    __tablename__ = 'user_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id"))
    checkin_date = Column(String(255))
    time_in = Column(String(255), nullable=True)
    time_out = Column(String(255), nullable=True)

    user = relationship("User", back_populates="user_logs")

    def as_dict(self):
        result = {column.name: getattr(self, column.name)
                  for column in self.__table__.columns}
        for relationship in self.__mapper__.relationships:
            related_obj = getattr(self, relationship.key)
            if isinstance(related_obj, Base):
                result[relationship.key] = related_obj.as_dict()
        return result


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
