from sqlalchemy import select, update, delete
from Domain.Models.Cach import Cach
from Domain.DB import Database


async def create_Cach(chatid: int, key: str, value):
    async with Database.async_session() as session:

        new_entry = Cach(chatid=chatid, key=key, value=value)
        session.add(new_entry)
        await session.commit()
        return new_entry

async def get_user_cache_value(chatid: int, key: str):
    async with Database.async_session() as session:

        result = await session.execute(
            select(Cach.value).where(Cach.chatid == chatid, Cach.key == key)
        )
        return result.scalar_one_or_none()

async def get_all_Cach_by_chatid(chatid: int):
    async with Database.async_session() as session:

        result = await session.execute(
            select(Cach).where(Cach.chatid == chatid)
        )
        return result.scalars().all()

async def delete_all_Cach_by_chatid(chatid: int):
    async with Database.async_session() as session:

        result = await session.execute(
            delete(Cach).where(Cach.chatid == chatid)
        )
        await session.commit()
        return result.rowcount

async def has_any_cache(chatid: int):
    async with Database.async_session() as session:

        result = await session.execute(
            select(Cach.id).where(Cach.chatid == chatid).limit(1)
        )

        return result.scalar() is not None

    
async def delete_user_cache_value(chatid: int, key: str):
    async with Database.async_session() as session:
        await session.execute(
            delete(Cach).where(Cach.chatid == chatid, Cach.key == key)
        )
        await session.commit()
        return True

async def update_user_cache_value(chatid: int, key: str, value: str):
    async with Database.async_session() as session:
        await session.execute(
            update(Cach).where(Cach.chatid == chatid, Cach.key == key).values(value=value)
        )
        await session.commit()
        return True
