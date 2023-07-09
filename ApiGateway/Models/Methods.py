from enum import Enum

class Methods(Enum):
    """
    Enumeración para representar los métodos HTTP.
    """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'