import psycopg2
import psycopg2.extras

class Database:
    """
    Clase para administrar la conexión a la base de datos PostgreSQL.

    Atributos:
        database (dict): Configuración de la base de datos.

    Métodos:
        get_connection(): Establece una conexión a la base de datos y devuelve el objeto de conexión.

    """
    database = {
        "dbname": "employme",
        "user": "root",
        "password": "toor",
        "host": "pgdb",
        "port": "5432"
    }

    @classmethod
    def get_connection(cls):
        """
        Establece una conexión a la base de datos PostgreSQL.

        Returns:
            psycopg2.extensions.connection: Objeto de conexión a la base de datos.

        """
        conn = psycopg2.connect(
            dbname=cls.database["dbname"],
            user=cls.database["user"],
            password=cls.database["password"],
            host=cls.database["host"],
            port=cls.database["port"]
        )
        return conn
