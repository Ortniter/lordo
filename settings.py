from environs import Env
from tortoise import Tortoise

env = Env()
env.read_env()

PORT = env.int('PORT', 3978)
BOT_TOKEN = env.str('BOT_TOKEN')
ONE_API_TOKEN = env.str('ONE_API_TOKEN')
ONE_API_URL = env.str('ONE_API_URL')
HEROKU_APP_NAME = env.str('HEROKU_APP_NAME')
DB_URL = env.str('DB_URL')


async def init_db():
    await Tortoise.init(db_url=DB_URL, modules={'models': ['models']})
