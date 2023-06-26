import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.login import api_router
from Utils.Services import *

app = FastAPI()

# Configuración del CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
