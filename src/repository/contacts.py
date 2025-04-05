from typing import List, Optional
from datetime import date, timedelta

from sqlalchemy import select, extract, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def get_contacts_by_birthday(self, days: int = 7) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)
        
        if today.month == 12 and end_date.month < 12:
            december_stmt = select(Contact).where(
                extract('month', Contact.birthday) == 12,
                extract('day', Contact.birthday) >= today.day,
                extract('day', Contact.birthday) <= 31
            )
            
            january_stmt = select(Contact).where(
                extract('month', Contact.birthday) == 1,
                extract('day', Contact.birthday) >= 1,
                extract('day', Contact.birthday) <= end_date.day
            )
            
            dec_result = await self.db.execute(december_stmt)
            jan_result = await self.db.execute(january_stmt)
            
            return list(dec_result.scalars().all()) + list(jan_result.scalars().all())
        else:
            stmt = select(Contact).where(
                (
                    (
                        extract('month', Contact.birthday) == today.month,
                        extract('day', Contact.birthday) >= today.day,
                        extract('day', Contact.birthday) <= end_date.day
                    )
                ) if today.month == end_date.month else (
                    (
                        (
                            extract('month', Contact.birthday) == today.month,
                            extract('day', Contact.birthday) >= today.day
                        )
                    ) | (
                        (
                            extract('month', Contact.birthday) == end_date.month,
                            extract('day', Contact.birthday) <= end_date.day
                        )
                    )
                )
            )
            
            result = await self.db.execute(stmt)
            return result.scalars().all()

    async def search_contacts(self, search_term: str) -> List[Contact]:
        search_pattern = f"%{search_term}%"
        stmt = select(Contact).where(
            or_(
                Contact.name.ilike(search_pattern),
                Contact.surname.ilike(search_pattern),
                Contact.email.ilike(search_pattern)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, body: ContactUpdate) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                if value is not None:
                    setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact 