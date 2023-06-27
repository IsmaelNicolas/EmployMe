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

def search_user(user_name: str, db=True) -> User:
    """
    Busca un usuario en la base de datos por su nombre de usuario.

    Args:
        user_name (str): Nombre de usuario a buscar.
        db (bool): Indica si se debe devolver un objeto UserDB (True) o User (False).
    
    Returns:
        UserDB or User: El objeto UserDB o User encontrado en la base de datos.

    Raises:
        HTTPException: Si el usuario no se encuentra en la base de datos.
        HTTPException: Si ocurre un error al conectar con la base de datos.
    """
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
    """
    Autentica al usuario a partir del token JWT.

    Args:
        token (str): Token JWT para autenticar al usuario.
    
    Returns:
        User: El objeto User autenticado.

    Raises:
        HTTPException: Si el token JWT no es válido o no contiene el nombre de usuario.
        HTTPException: Si el usuario no está autenticado.
    """
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


async def current_user(user: User = Depends(auth_user)):
    """
    Obtiene el usuario actual autenticado.

    Args:
        user (User): El usuario autenticado obtenido de auth_user.
    
    Returns:
        User: El usuario autenticado.

    Raises:
        HTTPException: Si el usuario no está autenticado.
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="UNAUTHORIZED", headers={"WWW-Authenticate": "Bearer"})
    return user
