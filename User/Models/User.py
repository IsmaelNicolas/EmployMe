from pydantic import BaseModel


class User(BaseModel):
    """
    Clase que representa un usuario.

    Atributos:
        user_id (str): ID del usuario.
        user_name (str): Nombre del usuario.
        user_score (float): Puntuación del usuario.
        user_email (str): Correo electrónico del usuario.
    """
    user_id: str
    user_name: str
    user_score: float
    user_email: str

class UserDB(User):
    """
    Clase que representa un usuario en la base de datos, hereda de la clase User.

    Atributos:
        user_password (str): Contraseña del usuario en la base de datos.
    """
    user_password: str
