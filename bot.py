import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from tortoise import run_async

import settings
import handlers
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

    # application.run_polling()

    # application.start_webhook(
    #     listen="0.0.0.0",
    #     port=settings.PORT,
    #     url_path=settings.BOT_TOKEN
    # )

    application.start_webhook(
        listen="0.0.0.0",
        port=settings.PORT,
        url_path=settings.BOT_TOKEN,
        webhook_url=f"https://{settings.HEROKU_APP_NAME}.herokuapp.com/{settings.BOT_TOKEN}"
    )


if __name__ == '__main__':
    run_async(connect_db())
    main()
