from sqlalchemy.future import select
from sqlalchemy import update, delete
from Domain.DB import Database
from Domain.Models.LogNumber import LogNUmber
from sqlalchemy.future import select
from Domain.DB import Database
from Domain.Models.LogNumber import LogNUmber

# Create
async def create_log_number(number: str ,code: int, name: str, link: str ,email: str = "-"):
    async with Database.async_session() as session:
        new_log = LogNUmber(
            number=number,
            email=email,
            code=code,
            name=name
        )
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)
        return new_log

# Get by ID
async def get_log_number_by_id(id: int):
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber).filter_by(id=id))
        return result.scalars().first()

async def get_name_by_number(number: str):
    async with Database.async_session() as session:
        result = await session.execute(
            select(LogNUmber.name).filter_by(number=number)
        )
        return result.scalar_one_or_none()

# Get all
async def get_all_log_numbers():
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber))
        return result.scalars().all()

# Get by number
async def get_log_number_by_number(number: str):
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber).filter_by(number=number))
        return result.scalars().first()

# Update
async def update_log_number(number: str, code: int, name: str, email: str = None):
    async with Database.async_session() as session:

        # پیدا کردن رکورد بر اساس number
        result = await session.execute(
            select(LogNUmber).filter_by(number=number)
        )
        log = result.scalars().first()

        if log is None:
            return None
        
        # مقداردهی
        if code is not None:
            log.code = code
        if name is not None:
            log.name = name
        if email is not None:
            log.email = email

        await session.commit()
        await session.refresh(log)
        return log

# Delete
async def delete_log_number(number):
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber).filter_by(number=number))
        log_entry = result.scalars().first()
        if not log_entry:
            return False

        await session.delete(log_entry)
        await session.commit()
        return True
