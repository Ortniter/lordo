from tortoise import Tortoise


async def connect_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']},
    )
