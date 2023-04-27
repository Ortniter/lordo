import requests
from tortoise import run_async

from database.connect_db import connect_db
import models
import settings

TOKEN = '30mT5Bg7VwZN-JKt6cfv'
BASE_URL = 'https://the-one-api.dev/v2'


class Palantir:

    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    @property
    def auth_header(self):
        return {'Authorization': f'Bearer {self.token}'}

    def get(self, endpoint, params=None):
        return requests.get(f'{self.base_url}/{endpoint}', headers=self.auth_header, params=params)

    async def gather(self):
        await self.save_books()
        await self.save_characters()
        await self.save_movies()

    async def save_books(self):
        response = self.get('book')
        response.raise_for_status()
        books = response.json()['docs']
        for book in books:
            book, _ = await models.Book.get_or_create(
                external_ref=book['_id'],
                defaults={'name': book['name']}
            )
            await self.save_chapters_for_book(book)

    async def save_chapters_for_book(self, book):
        response = self.get(f'book/{book.external_ref}/chapter')
        response.raise_for_status()
        chapters = response.json()['docs']
        for chapter in chapters:
            await models.Chapter.get_or_create(
                external_ref=chapter['_id'],
                defaults={
                    'name': chapter['chapterName'],
                    'book': book
                }
            )

    async def save_characters(self):
        response = self.get('character')
        response.raise_for_status()
        characters = response.json()['docs']
        for character in characters:
            await models.Character.get_or_create(
                external_ref=character['_id'],
                defaults={
                    'name': character.get('name', ''),
                    'race': character.get('race', ''),
                    'gender': character.get('gender', ''),
                    'birth': character.get('birth', ''),
                    'death': character.get('death', ''),
                    'spouse': character.get('spouse', ''),
                    'wiki_url': character.get('wikiUrl', '')
                }
            )

    async def save_movies(self):
        response = self.get('movie')
        response.raise_for_status()
        movies = response.json()['docs']
        for movie in movies:
            movie, _ = await models.Movie.get_or_create(
                external_ref=movie['_id'],
                defaults={
                    'name': movie['name'],
                    'runtime': movie['runtimeInMinutes'],
                    'budget': movie['budgetInMillions'],
                    'revenue': movie['boxOfficeRevenueInMillions'],
                    'academy_award_nominations': movie['academyAwardNominations'],
                    'academy_award_wins': movie['academyAwardWins'],
                    'rotten_tomatoes_score': movie['rottenTomatoesScore']
                }
            )
            await self.save_quotes(movie)

    async def save_quotes(self, movie):
        response = self.get('quote')
        response.raise_for_status()
        quotes = response.json()['docs']
        for quote in quotes:
            await models.Quote.get_or_create(
                external_ref=quote['_id'],
                defaults={
                    'text': quote['dialog'],
                    'movie': movie,
                    'character': await models.Character.get(external_ref=quote['character'])
                }
            )


async def main():
    await connect_db()
    palantir = Palantir(
        token=settings.ONE_API_TOKEN,
        base_url=settings.ONE_API_URL
    )
    await palantir.gather()


if __name__ == '__main__':
    run_async(main())
