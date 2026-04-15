from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, todo, users

from .schemas import Message

app = FastAPI(title='Minha primeira API')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
