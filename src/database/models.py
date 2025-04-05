from datetime import date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    additional_data: Mapped[str] = mapped_column(String(500), nullable=True) 