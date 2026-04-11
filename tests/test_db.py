from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User('test', 'test@test', 'secret')
        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'test')
        )

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test',
            'password': 'secret',
            'created_at': time,
        }


@pytest.mark.asyncio
async def test_get_session():

    session_gen = get_session()
    session = await anext(session_gen)

    assert isinstance(session, AsyncSession)
    await session.close()
