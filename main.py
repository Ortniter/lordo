from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

import models

app = FastAPI()


class Status(BaseModel):
    message: str


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}


@app.post('/books/', status_code=201)
async def create_book(name=Form(...)):
    book = await models.Book.create(name=name)
    return await models.BookReadPydantic.from_tortoise_orm(book)


@app.get('/books/')
async def get_books():
    return await models.BookReadPydantic.from_queryset(models.Book.all())


@app.put('/books/{id}', response_model=models.BookReadPydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_book(book_id: int, book: models.BookWritePydantic):
    await models.Book.filter(id=book_id).update(**book.dict(exclude_unset=True))
    return await models.BookReadPydantic.from_queryset_single(models.Book.get(id=book_id))


@app.get('/books/{id}', response_model=models.BookReadPydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_book(book_id: int):
    return await models.BookReadPydantic.from_queryset_single(models.Book.get(id=book_id))


@app.delete('/books/{id}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_book(book_id: int):
    deleted_count = await models.Book.filter(id=book_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'Book {book_id} not found')
    return Status(message=f'Deleted book {book_id}')


@app.get('/chapters/')
async def get_chapters():
    return await models.ChapterReadPydantic.from_queryset(models.Chapter.all())


@app.get('/movies/')
async def get_movies():
    return await models.MovieReadPydantic.from_queryset(models.Movie.all())


@app.get('/characters/')
async def get_characters():
    return await models.CharacterReadPydantic.from_queryset(models.Character.all())


@app.get('/quotes/')
async def get_quotes():
    return await models.QuoteReadPydantic.from_queryset(models.Quote.all())


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

TORTOISE_ORM = {
    'connections': {
        'default': 'sqlite://db.sqlite3',
    },
    'apps': {
        'models': {'models': ['models'], 'default_connection': 'default'},
    },
}
