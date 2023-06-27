import os

ALGORITHM =  os.getenv('ALGORITHM')
"""
Algoritmo utilizado para codificar y decodificar el token JWT.

Valor:
    str: Valor de la variable de entorno 'ALGORITHM'.
"""

ACCESS_TOKEN_DURATION = int(os.getenv('ACCESS_TOKEN_DURATION'))
"""
Duración en minutos del token de acceso.

Valor:
    int: Valor entero de la variable de entorno 'ACCESS_TOKEN_DURATION'.
"""

SECRET = os.getenv('SECRET')
"""
Clave secreta utilizada para firmar el token JWT.

Valor:
    str: Valor de la variable de entorno 'SECRET'.
"""
