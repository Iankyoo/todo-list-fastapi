from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User

# provisório
SECRET_KEY = 'YOU-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = PasswordHash.recommended()

credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    jwt_encoded = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(OAuth2_scheme),
):
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user
