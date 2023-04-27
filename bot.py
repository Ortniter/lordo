import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from tortoise import run_async, Tortoise

import settings
import handlers
from palantir import Palantir
from database.connect_db import connect_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(settings.BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', handlers.start))

    application.add_handler(CommandHandler('help', handlers.help))

    application.add_handler(CommandHandler('books', handlers.books))

    application.add_handler(CommandHandler('movies', handlers.movies))

    application.add_handler(CommandHandler('character', handlers.character))

    application.add_handler(CallbackQueryHandler(handlers.Button()))

    application.run_polling()


async def set_db():
    await connect_db()
    await Tortoise.generate_schemas()
    palantir = Palantir(
        token=settings.ONE_API_TOKEN,
        base_url=settings.ONE_API_URL
    )
    await palantir.gather()


if __name__ == '__main__':
    run_async(set_db())
    main()
