import random
import logging

from telegram import Update
from telegram.ext import ContextTypes

import models
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm a bot that can tell you about the Lord of the Rings universe.\n"
             "You can use the following commands:\n"
             "/books - get a list of books\n"
             "/movies - get a list of movies\n"
             "/character - get a random character\n"
             "/character <name> - get a character by name\n"
             "/help - get help"
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You can use the following commands:\n"
             "/books - get a list of books\n"
             "/movies - get a list of movies\n"
             "/character - get a random character\n"
             "/character <name> - get a character by name\n"
             "/help - get help"
    )


async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Select a book',
        reply_markup=await utils.get_inline_keyboard_markup(models.Book, 'book')
    )


async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Select a Movie',
        reply_markup=await utils.get_inline_keyboard_markup(models.Movie, 'movie')
    )


async def character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = ' '.join(context.args)

    if not name:
        character = random.choice(await models.Character.all())
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=character.detail_info,
            reply_markup=utils.get_quote_markup(character, 'character')
        )
        return

    character = await models.Character.filter(name__icontains=name).first()

    if not character:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Character not found')
        await context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            sticker='CAACAgQAAxkBAAEIvFpkSOxFZA0hXL4Z5ysrGrJageUsowAC4AcAAlnewgF8fmybOPnZpy8E'
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=character.detail_info,
        reply_markup=utils.get_quote_markup(character, 'character')
    )


class Button:

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        logger.info(query.data)

        self.data = utils.Mapper(query.data)
        self.chat_id = query.message.chat_id
        self.bot = context.bot

        await self.process()

    async def process(self):
        kwargs = dict()
        obj = await self.data.obj

        if self.data.is_quote:
            await self._reply_quote(obj)

        if self.data.is_book or self.data.is_movie:
            text = await obj.get_detail_info() if self.data.is_book else obj.detail_info
            if self.data.is_movie:
                kwargs['reply_markup'] = utils.get_quote_markup(obj, 'movie')
            await self._reply(obj, text, **kwargs)

    async def _reply(self, obj, text, **kwargs):
        if obj.image:
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=obj.image,
                caption=text,
                **kwargs
            )
        else:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                **kwargs
            )

    async def _reply_quote(self, obj):
        quotes = await obj.quotes.all()
        if quotes:
            quote = random.choice(quotes)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=quote.text,
                reply_markup=utils.get_quote_markup(obj, self.data.model_name)
            )
        else:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text='No quotes found',
            )
