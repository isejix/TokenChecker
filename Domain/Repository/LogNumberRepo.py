from sqlalchemy.future import select
from sqlalchemy import update, delete
from Domain.DB import Database
from Domain.Models.LogNumber import LogNUmber
from sqlalchemy.future import select
from Domain.DB import Database
from Domain.Models.LogNumber import LogNUmber

# Create
async def create_log_number(number: str ,code: int, name: str, email: str = "-"):
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
async def update_log_number(id: int, number: str = None, email: str = None, code: int = None, name: str = None):
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber).filter_by(id=id))
        log_entry = result.scalars().first()
        if not log_entry:
            return None

        if number is not None:
            log_entry.number = number
        if email is not None:
            log_entry.email = email
        if code is not None:
            log_entry.code = code
        if name is not None:
            log_entry.name = name

        await session.commit()
        await session.refresh(log_entry)
        return log_entry

# Delete
async def delete_log_number(id: int):
    async with Database.async_session() as session:
        result = await session.execute(select(LogNUmber).filter_by(id=id))
        log_entry = result.scalars().first()
        if not log_entry:
            return False

        await session.delete(log_entry)
        await session.commit()
        return True
