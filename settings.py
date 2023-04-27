from environs import Env

env = Env()
env.read_env()

POSTGRES_HOST = env.str('POSTGRES_HOST')
POSTGRES_PORT = env.int('POSTGRES_PORT')
POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')

DATABASES = {
    "connections": {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            "credentials": {
                "database": POSTGRES_DB,
                "host": POSTGRES_HOST,
                "password": POSTGRES_PASSWORD,
                "port": POSTGRES_PORT,
                "user": POSTGRES_USER,
                "ssl": None
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}

BOT_TOKEN = env.str('BOT_TOKEN')
ONE_API_TOKEN = env.str('ONE_API_TOKEN')
ONE_API_URL = env.str('ONE_API_URL')
