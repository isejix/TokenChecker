from sqlalchemy.future import select
from sqlalchemy import delete
from Domain.DB import Database
from Domain.Models.ReceivedNumbers import ReciveNumber, SessionStatus

# Create
async def create_number(number: str, link: str, path: str, status: SessionStatus = SessionStatus.Accepted):
    async with Database.async_session() as session:
        new_number = ReciveNumber(
            number=number,
            link=link,
            path=path,
            status=status
        )
        session.add(new_number)
        await session.commit()
        await session.refresh(new_number)
        return new_number

# Get by ID
async def get_number_by_id(id: int):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(id=id)
        )
        return result.scalars().first()

# Get all
async def get_all_numbers():
    async with Database.async_session() as session:
        result = await session.execute(select(ReciveNumber))
        return result.scalars().all()

# Get last number
async def get_last_number():
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).order_by(ReciveNumber.id.desc()).limit(1)
        )
        return result.scalars().first()

# Update
async def update_number(id: int, new_number: str = None, new_link: str = None, new_path: str = None, new_status: SessionStatus = None):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(id=id)
        )
        data = result.scalars().first()

        if not data:
            return None

        if new_number:
            data.number = new_number
        if new_link:
            data.link = new_link
        if new_path:
            data.path = new_path
        if new_status:
            data.status = new_status

        await session.commit()
        await session.refresh(data)
        return data

# Delete
async def delete_number(id: int):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(id=id)
        )
        data = result.scalars().first()

        if not data:
            return False

        await session.delete(data)
        await session.commit()
        return True

# Get by phone
async def get_number_by_phone(phone):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(number=phone)
        )
        return result.scalars().first()

# Get all numbers by path
async def get_all_numbers_by_path(path: str):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(path=path)
        )
        return result.scalars().all()

async def update_status_by_number(phone: str, new_status: SessionStatus):
    async with Database.async_session() as session:
        result = await session.execute(
            select(ReciveNumber).filter_by(number=phone)
        )
        number_entry = result.scalars().first()

        if not number_entry:
            return None  # phone not found

        number_entry.status = new_status
        await session.commit()
        await session.refresh(number_entry)
        return number_entry
    

async def delete_all_numbers_by_path(path: str):

    
    async with Database.async_session() as session:
        result = await session.execute(
            delete(ReciveNumber).where(ReciveNumber.path == path)
        )
        await session.commit()
        return result.rowcount