from environs import Env

env = Env()
env.read_env()

PORT = env.int('BOT_TOKEN', 3978)
BOT_TOKEN = env.str('BOT_TOKEN')
ONE_API_TOKEN = env.str('ONE_API_TOKEN')
ONE_API_URL = env.str('ONE_API_URL')
