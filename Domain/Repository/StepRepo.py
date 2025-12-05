from Domain.Models.Step import Step
from sqlalchemy.future import select
from Domain.DB import Database


async def create_step(chatid, step):
    async with Database.async_session() as session:
        new_step = Step(
            chatid=chatid,
            step=step
        )

        session.add(new_step)
        await session.commit()
        await session.refresh(new_step)
        return new_step


async def get_step(chatid):
    async with Database.async_session() as session:
        result = await session.execute(
            select(Step).filter_by(chatid=chatid)
        )
        return result.scalars().first()


async def update_step(chatid, new_step=None):
    async with Database.async_session() as session:
        result = await session.execute(
            select(Step).filter_by(chatid=chatid)
        )
        data = result.scalars().first()

        if not data:
            return None

        if new_step is not None:
            data.step = new_step

        await session.commit()
        await session.refresh(data)
        return data


async def delete_step(chatid):
    async with Database.async_session() as session:
        result = await session.execute(
            select(Step).filter_by(chatid=chatid)
        )
        data = result.scalars().first()

        if not data:
            return None

        await session.delete(data)
        await session.commit()
        return True


async def has_step(chatid):
    async with Database.async_session() as session:
        result = await session.execute(
            select(Step).where(Step.chatid == chatid).limit(1)
        )
        return result.first() is not None
