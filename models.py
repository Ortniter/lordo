from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Book(Model):
    external_ref = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    async def get_detail_info(self):
        await self.fetch_related('chapters')
        formatted_chapters = '\n'.join(
            [
                f'{i + 1}. {chapter.name}'
                for i, chapter in enumerate(self.chapters)
            ]
        )
        return f'{self.name}\n' \
               f'Chapters: {len(self.chapters)}\n' \
               f'{formatted_chapters}'


BookReadPydantic = pydantic_model_creator(Book, name='BookRead')
BookWritePydantic = pydantic_model_creator(Book, exclude=('id',), name='BookWrite')


class Chapter(Model):
    external_ref = fields.CharField(max_length=255, unique=True)
    book = fields.ForeignKeyField('models.Book', related_name='chapters')
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


ChapterReadPydantic = pydantic_model_creator(Chapter, name='ChapterRead')


class Movie(Model):
    external_ref = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    runtime = fields.IntField()
    budget = fields.IntField()
    revenue = fields.IntField()
    academy_award_nominations = fields.IntField()
    academy_award_wins = fields.IntField()
    rotten_tomatoes_score = fields.IntField()
    image = fields.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def detail_info(self):
        return f'{self.name} ({self.runtime} minutes)\n' \
               f'Budget: ${self.budget} million\n' \
               f'Revenue: ${self.revenue} million\n' \
               f'Academy Award Nominations: {self.academy_award_nominations}\n' \
               f'Academy Award Wins: {self.academy_award_wins}\n' \
               f'Rotten Tomatoes Score: {self.rotten_tomatoes_score}%\n'


MovieReadPydantic = pydantic_model_creator(Movie, name='MovieRead')


class Character(Model):
    external_ref = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    race = fields.CharField(max_length=255)
    gender = fields.CharField(max_length=255)
    birth = fields.CharField(max_length=255)
    death = fields.CharField(max_length=255)
    spouse = fields.CharField(max_length=255)
    wiki_url = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def detail_info(self):
        info = f'{self.name}\n' \
               f'Race: {self.race or "Unknown"}\n' \
               f'Gender: {self.gender or "Unknown"}\n' \
               f'Birth: {self.birth or "Unknown"}\n' \
               f'Death: {self.death or "Unknown"}\n' \
               f'Spouse: {self.spouse or "Unknown"}'
        if self.wiki_url:
            info += f'\nWiki: {self.wiki_url}'
        return info


CharacterReadPydantic = pydantic_model_creator(Character, name='CharacterRead')


class Quote(Model):
    external_ref = fields.CharField(max_length=255, unique=True)
    text = fields.TextField()
    movie = fields.ForeignKeyField('models.Movie', related_name='quotes')
    character = fields.ForeignKeyField('models.Character', related_name='quotes')

    def __str__(self):
        return self.text


QuoteReadPydantic = pydantic_model_creator(Quote, name='QuoteRead')
