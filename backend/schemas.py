from pydantic import BaseModel
from fastapi import Request
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str
    name: str
    card_id: str
    email: str
    phone_number: str
    image_url: str
    gender: str
    dob: str
    created: Optional[str] = None

    class Config:
        orm_mode = True


class UserLog(BaseModel):
    id: int
    user_id: str
    checkin_date: str
    time_in: Optional[str] = None
    time_out: Optional[str] = None

    user: User

    class Config:
        orm_mode = True


class UserCheckin(BaseModel):
    user_id: str
    checkin_date: str
    time_in: str

    class Config:
        orm_mode = True


class FormCreateUser:
    def __init__(self, request: Request):
        self.request: Request = request
        self.id: str = ""
        self.card_id: str = ""
        self.name: str = ""
        self.email: str = ""
        self.image_url: str = ""
        self.phone_number: str = ""
        self.dob: str = ""
        self.gender: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.id = form.get('id')
        self.name = form.get('name')
        self.card_id = form.get('card_id')
        self.email = form.get('email')
        self.image_url = form.get('image_url')
        self.gender = form.get('gender')
        self.dob = form.get('dob')
        self.phone_number = form.get('phone_number')
