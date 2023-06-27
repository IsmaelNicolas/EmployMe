from datetime import datetime, timedelta, timezone

from config.database import Database
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from Models.User import User, UserDB
from passlib.context import CryptContext
from Utils.Services import *

crypt = CryptContext(schemes=["bcrypt"])
api_router = APIRouter(prefix="/api")

@api_router.post("/login")
async def login(response: Response, form: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticar al usuario y generar un token de acceso.

    Args:
        response (Response): Objeto de respuesta HTTP.
        form (OAuth2PasswordRequestForm): Datos del formulario de inicio de sesión.

    Returns:
        Response: Objeto de respuesta HTTP con el token de acceso y tipo de token.

    Raises:
        HTTPException: Si la contraseña es incorrecta.
    """
    user: UserDB = search_user(form.username)

    if not crypt.verify(form.password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    expire = (datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    access_token = {
        "sub": user.user_name,
        "exp": expire
    }

    encoded_token = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)

    response = JSONResponse(
        content={"access_token": encoded_token, "token_type": "bearer"},
        status_code=status.HTTP_202_ACCEPTED
    )

    response.set_cookie(
        key="access_token",
        value=encoded_token,
        expires=expire,
        httponly=True,
    )

    return response


@api_router.post("/logout")
async def logout(response: Response, user: User = Depends(current_user)):
    """
    Endpoint para cerrar sesión y eliminar el token de acceso almacenado en las cookies.

    Args:
        response (Response): Objeto de respuesta HTTP.
        user (User): Usuario autenticado.

    Returns:
        dict: Mensaje de éxito.

    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@api_router.get("/user/me")
async def mee(user: User = Depends(current_user)):
    """
    Endpoint para obtener la información del usuario autenticado.

    Args:
        user (User): Usuario autenticado.

    Returns:
        User: Información del usuario autenticado.

    """
    return user
