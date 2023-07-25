import logging

import psycopg2
import psycopg2.extras
from config.database import Database
from config.environment import *
from fastapi import Depends, HTTPException, WebSocket, status
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
    conn = None
    try:
        conn = Database.get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM "USER" WHERE USER_NAME = %s', (user_name,))
        user = cur.fetchone()
        logger.warn(user)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_dict = dict(user)
        print(user_dict)
        return UserDB(**user_dict) if db else User(**user_dict)
    except psycopg2.Error:
        logger.warn("Error base de datos:"+ str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Server error")
    except HTTPException:
        # Re-raise HTTPException to propagate the error with the correct status code
        raise
    except Exception as e:
        logger.warn("Error:"+ str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
    finally:
        if conn is not None:
            conn.close()


async def   auth_user(token: str = Depends(oauth2)):
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

def validate_route(route: str):
    if route.endswith('/') or '//' in route:
        return False,False  # No puede terminar en '/' ni tener dos barras consecutivas '//'
    
    special = {'{', '}', '/'}
    open_bracket = 0
    previous_char = None
    for char in route:
        if previous_char == char and char in special:
            return False,False  # Dos caracteres especiales seguidos
        
        if char == '{':
            open_bracket += 1
        
        if char == '}':
            if open_bracket == 0:
                return False ,False # Paréntesis cerrado sin paréntesis abierto previo
            open_bracket -= 1
        
        previous_char = char
    
    return open_bracket == 0 and route.count('{') == route.count('}') ,  '{' in route # Paréntesis abierto sin paréntesis cerrado posterior




def authenticate_websocket(token):
    # Obtener el token JWT del encabezado de la solicitud de WebSocket
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="UNAUTHORIZED", headers={"WWW-Authenticate": "Bearer"})

    try:
        user_name = jwt.decode(token, SECRET, ALGORITHM)
        print('token: '+ user_name)
        if user_name is None:
            raise exception

    except JWTError as e:
        print("JWT error" + str(e))
        raise exception

    return search_user(user_name=user_name, db=False)

