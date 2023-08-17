import uvicorn
import uuid
from passlib.context import CryptContext
from fastapi import APIRouter, FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from Models.User import User, UserDB
from Config.Database import Database
from Utils.Utils import search_user

app = FastAPI()
api_router = APIRouter(prefix="/api")
crypt = CryptContext(schemes=["bcrypt"])

# Ruta para obtener un usuario


@api_router.get("/getuser")
def get_user():
    # Lógica para obtener un usuario
    return {"message": "Obtener usuario"}

# Ruta para actualizar la imagen de un usuario


@api_router.patch("/updateuserimage")
def update_user_image():
    # Lógica para actualizar la imagen de un usuario
    return {"message": "Actualizar imagen de usuario"}

# Ruta para subir la imagen de un usuario


@api_router.patch("/uploaduserimage")
def upload_user_image():
    # Lógica para subir la imagen de un usuario
    return {"message": "Subir imagen de usuario"}

# Ruta para crear un usuario


@api_router.post("/createuser", status_code=status.HTTP_201_CREATED,)
async def create_user(user: UserDB):

    conn = None
    try:

        current = search_user(user.user_name, False)
        if current is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User exist")

        conn = Database.get_connection()
        user.user_id = str(uuid.uuid4()) 

        cur = conn.cursor()
        query = 'INSERT INTO "USER" (user_id, user_name, user_score, user_email,user_password) VALUES (%s, %s, %s, %s,%s)'
        values = (user.user_id,user.user_name, user.user_score,
                  user.user_email, crypt.encrypt(user.user_password))
        cur.execute(query, values)

        query = 'INSERT INTO requester (user_id) values(%s)'
        cur.execute(query,(user.user_id,))
    
        conn.commit()
        cur.close()
        return User(**dict(user))
    except psycopg2.Error as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo crear: " + str(e))
    finally:
        if conn is not None:
            conn.close()


# Ruta para actualizar un usuario
@api_router.put("/updateuser")
def update_user(user: User):
    conn = None
    try:
        conn = Database.get_connection()
        cur = conn.cursor()
        query = 'UPDATE "USER" SET user_name = %s, user_email = %s WHERE user_name = %s'
        values = (user.user_name,user.user_email, user.user_name)
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return User(**dict(user))
    except psycopg2.Error as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo actualizar el usuario: " + str(e))
    finally:
        if conn is not None:
            conn.close()


# Ruta para eliminar un usuario

@api_router.delete("/deleteuser/{user_id}")
def delete_user(user_id: str):
    conn = None
    try:
        conn = Database.get_connection()
        cur = conn.cursor()
        query = 'DELETE FROM "USER" WHERE user_id = %s'
        values = (user_id,)
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return {"message": "Usuario eliminado correctamente"}
    except psycopg2.Error as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo eliminar el usuario: " + str(e))
    finally:
        if conn is not None:
            conn.close()



app.include_router(api_router)

"""
Configuración del CORS
Se definen los dominios permitidos para las solicitudes CORS.
"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    """
    Inicia el servidor uvicorn en el archivo "app" con la variable "app".
    Se configura el host en "0.0.0.0" para aceptar conexiones de cualquier dirección IP.
    Se configura el puerto en 800.
    Se habilita el modo de recarga automática para el desarrollo.
    """
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
