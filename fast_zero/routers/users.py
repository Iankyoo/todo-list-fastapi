from http import HTTPStatus
from operator import or_
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def user_create(user: UserSchema, session: SessionDep):
    db_user = await session.scalar(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: SessionDep,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    users = await session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {'users': users}


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    session: SessionDep,
    current_user: CurrentUser,
    user: UserSchema,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.flush()
        await session.commit()
        await session.refresh(current_user)

        return current_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await session.delete(current_user)
    await session.commit()

    return {'message': 'User has been deleted'}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user_id(user_id: int, session: SessionDep):
    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return user_db
