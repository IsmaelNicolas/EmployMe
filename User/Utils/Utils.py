import psycopg2
import psycopg2.extras
from fastapi import status,HTTPException
from Models.User import User,UserDB
from Config.logger import logger
from Config.Database import Database

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
        logger.info(user)
        if user is None:
            return None

        user_dict = dict(user)
        print(user_dict)
        return UserDB(**user_dict) if db else User(**user_dict)

    except Exception as e:
        print("Error base de datos:", str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Server error")
    finally:
        if conn is not None:
            conn.close()
