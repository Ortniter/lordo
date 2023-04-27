import json
from functools import cached_property

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import models


async def get_inline_keyboard_markup(model, model_name):
    objects = await model.all()
    keyboard = [
        [
            InlineKeyboardButton(
                text=obj.name,
                callback_data=json.dumps({'action': model_name, 'model': model_name, 'id': obj.pk})
            )
        ] for obj in objects
    ]
    return InlineKeyboardMarkup(keyboard)


def get_quote_markup(obj, model_name):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=f'Get {obj.name} quote',
                callback_data=json.dumps({'action': 'quote', 'model': model_name, 'id': obj.pk})
            )
        ]]
    )


class Mapper:
    MODEL_MAP = {
        'book': models.Book,
        'movie': models.Movie,
        'character': models.Character,
        'quote': models.Quote,
    }

    def __init__(self, query_data):
        query_data = json.loads(query_data)
        self.model = self.MODEL_MAP[query_data['model']]
        self.model_name = query_data['model']
        self.obj_id = query_data['id']
        self.action = query_data['action']

    @cached_property
    async def obj(self):
        return await self.model.get(id=self.obj_id)

    @property
    def is_quote(self):
        return self.action == 'quote'

    @property
    def is_movie(self):
        return self.action == 'movie'

    @property
    def is_book(self):
        return self.action == 'book'
