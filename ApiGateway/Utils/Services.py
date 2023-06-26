import logging

import psycopg2
import psycopg2.extras
from config.database import Database
from config.environment import *
from fastapi import Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from Models.User import User, UserDB

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")

# Busca el usuario en la base de datos
def search_user(user_name: str, db=True) -> User:
    print("search user")
    conn = None
    try:
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM "USER" WHERE USER_NAME = %s', (user_name,))
        user = cur.fetchone()
        logger.info(user)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_dict = dict(user)
        return UserDB(**user_dict) if db else User(**user_dict)

    except Exception as e:
        print("Error base de datos:", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Server error")
    finally:
        if conn is not None:
            conn.close()


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="UNAUTHORIZED", headers={"WWW-Authenticate": "Bearer"})
    try:
        user_name = jwt.decode(token, SECRET, ALGORITHM).get("sub")
        if user_name is None:
            raise exception

    except JWTError as e:
        print("JWT error" + str(e))
        raise exception

    return search_user(user_name=user_name, db=False)

# obtiene el usuario actual
async def current_user(user: User = Depends(auth_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="UNAUTHORIZED", headers={"WWW-Authenticate": "Bearer"})
    return user
