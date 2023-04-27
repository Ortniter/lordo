from tortoise import Tortoise, run_async
from database.connect_db import connect_db


async def main():
    await connect_db()
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(main())
