import httpx
import yaml
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Request, Response, UploadFile,status

from Models.Methods import Methods
from Models.User import User
from Utils.Services import current_user,validate_route
from config.logger import logger


routes = {}

ms_router = APIRouter(prefix="/api")

def redirect_json(json:Dict[str, Any]):
    return (json)

def redirect_params(request: Request,param:str):
    return {"mensaje": f"Redirigiendo al post {param}... \n {request.query_params['param']}"}
# Función "redirect"
async def redirect(request: Request, response: Response,user: User = Depends(current_user)):
    target = routes[request.url.path]["endpoint"]
    method = routes[request.url.path]["method"]
    try:
        async with httpx.AsyncClient() as client:
            logger.warning(f'Redirigiendo a {target}')
            response_target = await client.get(target)
            response_target.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado de error
    except httpx.RequestError as e:
        logger.error(f' Redirection error: {status.HTTP_503_SERVICE_UNAVAILABLE}{str(e)}  Target: {target} , Method: {method}')
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    response.status_code = response_target.status_code

    return response_target.json()

async def image_route(file: UploadFile):
    return {"filename": file.filename}

with open("endpoints.yml", "r") as file:
    data = yaml.safe_load(file)

logger.warning("Creando endpoints")
for servicio, info_servicio in data["microservices"].items():
    puerto = info_servicio["port"]
    endpoints = info_servicio["endpoints"]
    for endpoint in endpoints:
        
        ruta = endpoint["route"]
        metodo = endpoint["method"]

        routes[ruta] = {"endpoint":f'http://localhost:{puerto}{ruta}',"method":metodo}

        valida , param = validate_route(ruta)

        funcion = redirect
        if param:
            funcion = redirect_params
        if metodo == Methods.POST.value or metodo == Methods.PUT.value:
            funcion = redirect_json
        if metodo == Methods.PATCH.value:
            funcion = image_route

        if valida:
            ms_router.add_api_route(
                path=ruta,
                status_code=200,
                endpoint=funcion,
                methods=[metodo],
                tags=[servicio]
            )
        else:
            logger.error(f'Ruta no valida: {ruta}')

logger.warning("Rutas creadas")

