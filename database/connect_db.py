from tortoise import Tortoise

import settings


async def connect_db():
    await Tortoise.init(settings.DATABASES)
