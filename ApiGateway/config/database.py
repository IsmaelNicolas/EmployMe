import psycopg2


class Database:

    database = {
        "dbname": "employme",
        "user": "root",
        "password": "toor",
        "host": "pgdb",
        "port": "5432"
    }

    @classmethod
    def get_connection(cls):
        conn = psycopg2.connect(
            dbname=cls.database["dbname"],
            user=cls.database["user"],
            password=cls.database["password"],
            host=cls.database["host"],
            port=cls.database["port"]
        )
        return conn
