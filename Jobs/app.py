from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from datetime import datetime
import uuid
import uvicorn

app = FastAPI()
api_router = APIRouter(prefix="/api")

# PostgreSQL database configuration
DB_HOST = "pgdb"
DB_NAME = "employme"
DB_USER = "root"
DB_PASSWORD = "toor"
DB_PORT = 5432

connection_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"


def create_connection():
    return psycopg2.connect(connection_string)


@api_router.get('/jobs/{user_id}')
def get_jobs(user_id: str):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            querry = "SELECT j.job_id, j.job_tittle, j.job_description, p.publish_date, STRING_AGG(s.skill_name, ', ') AS skill_names FROM job j JOIN post p ON j.job_id = p.job_id JOIN requester r ON p.user_id = r.user_id LEFT JOIN jobskills js ON j.job_id = js.job_id LEFT JOIN skill s ON js.skill_id = s.skill_id WHERE r.user_id <> %s GROUP BY j.job_id, j.job_tittle, j.job_description, p.publish_date;"

            cur.execute(
                querry, (user_id,))

            rows = cur.fetchall()

            columns = [desc[0] for desc in cur.description]
            jobs = [dict(zip(columns, row)) for row in rows]
            return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


class JobUser(BaseModel):
    job_tittle: str
    user_id: str

class JobApply(BaseModel):
    job_id: str
    user_id: str

@api_router.post('/jobs/search')
def get_job_by_title(job:JobUser):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            querry = "SELECT j.job_id, j.job_tittle, j.job_description, p.publish_date, STRING_AGG(s.skill_name, ', ') AS skill_names FROM job j JOIN post p ON j.job_id = p.job_id JOIN requester r ON p.user_id = r.user_id LEFT JOIN jobskills js ON j.job_id = js.job_id LEFT JOIN skill s ON js.skill_id = s.skill_id WHERE r.user_id <> %s  AND LOWER(j.job_tittle) LIKE lower(%s) GROUP BY j.job_id, j.job_tittle, j.job_description, p.publish_date;"

            cur.execute(
                querry, (job.user_id,'%' + job.job_tittle + '%'))

            rows = cur.fetchall()

            columns = [desc[0] for desc in cur.description]
            jobs = [dict(zip(columns, row)) for row in rows]
            return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
 

@api_router.post('jobs/apply')
def apply_job(jobUser:JobApply):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            querry = "INSERT INTO apply (job_id,user_id,apply_date,favorite) values (%s,%s,%s,false)"

            cur.execute(
                querry, (jobUser.job_tittle,jobUser.user_id,datetime.now()))

           
        conn.commit()
        return {"message": "Apply created successfully", "job_id": str(jobUser.job_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@api_router.get('jobs/apply')
def apply_job(jobUser:JobUser):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            querry = ""

            cur.execute(
                querry, (jobUser.job_tittle,jobUser.user_id,datetime.now()))

            rows = cur.fetchall()

            columns = [desc[0] for desc in cur.description]
            jobs = [dict(zip(columns, row)) for row in rows]
            return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    """
    Inicia el servidor uvicorn en el archivo "app" con la variable "app".
    Se configura el host en "0.0.0.0" para aceptar conexiones de cualquier dirección IP.
    Se configura el puerto en 8081.
    Se habilita el modo de recarga automática para el desarrollo.
    """
    uvicorn.run("app:app", host="0.0.0.0", port=8082, reload=True)
