from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=20)
    birthday: date
    additional_data: Optional[str] = Field(default=None, max_length=500)

class ContactModel(ContactBase):
    pass

class ContactUpdate(ContactBase):
    name: Optional[str] = Field(default=None, max_length=50)
    surname: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    birthday: Optional[date] = None
    additional_data: Optional[str] = Field(default=None, max_length=500)

class ContactResponse(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True) 