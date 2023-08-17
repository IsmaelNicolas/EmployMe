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

# Helper function to create a database connection


def create_connection():
    return psycopg2.connect(connection_string)

# Define the data model for the request


class JobRequest(BaseModel):
    user_id: str
    neighborhood: str
    main_street: str
    secondary_street: str
    job_title: str
    job_description: str
    job_skills: list


class Job(BaseModel):
    job_id: str
    neighborhood: str
    main_street: str
    secondary_street: str
    job_title: str
    job_description: str


class JobSkills(BaseModel):
    job_id: str
    job_skills: list


class JobUser(BaseModel):
    job_tittle: str
    user_id: str

# Function to create a new job and its associated skills


def create_job_with_skills(job_request: JobRequest):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            job_id = str(uuid.uuid4())  # Generate a new UUID for job_id

            # Insert the job data into the 'job' table
            cur.execute(
                "INSERT INTO job (job_id, neighborhood, main_street, secondary_street, job_tittle, job_description) VALUES (%s, %s, %s, %s, %s, %s)",
                (job_id, job_request.neighborhood, job_request.main_street,
                 job_request.secondary_street, job_request.job_title, job_request.job_description)
            )

            # Insert the job skills into the 'jobskills' table
            for skill_id in job_request.job_skills:
                cur.execute(
                    "INSERT INTO jobskills (skill_id, job_id) VALUES (%s, %s)",
                    (skill_id, job_id)
                )

            # Insert the post data (with current date) into the 'post' table
            cur.execute(
                "INSERT INTO post (user_id, job_id, publish_date) VALUES (%s, %s, %s)",
                (job_request.user_id, job_id, datetime.now())
            )

        conn.commit()
        return {"message": "Job created successfully", "job_id": str(job_id)}
    except psycopg2.errors.UniqueViolation:
        return {"error": "Job ID already exists"}
    finally:
        conn.close()


@api_router.post("/createpost", response_model=dict)
def create_job_with_skills_endpoint(job_request: JobRequest):
    return create_job_with_skills(job_request)


@api_router.put('/updatepost')
def update_job(job: Job):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE job SET neighborhood = %s, main_street = %s, secondary_street = %s, job_tittle = %s, job_description = %s WHERE job_id = %s",
                (job.neighborhood, job.main_street, job.secondary_street,
                 job.job_title, job.job_description, job.job_id)
            )

        conn.commit()
    except psycopg2.errors.UniqueViolation:
        return {"error": "Job ID already exists"}
    finally:
        conn.close()


@api_router.get('/skills/{skill_name}')
def get_skills(skill_name: str):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM skill WHERE LOWER(skill_name) LIKE LOWER(%s)", ('%' + skill_name + '%',))
            skills = cur.fetchall()
            # Obtener nombres de columnas
            columns = [desc[0] for desc in cur.description]

        skills_list = []
        for skill in skills:
            skill_dict = dict(zip(columns, skill))
            skills_list.append(skill_dict)

        return skills_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@api_router.get('/posts/{user_id}')
def get_posts_by_user(user_id):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            querry = "SELECT j.job_id, j.neighborhood, j.job_tittle, j.job_description, p.publish_date FROM job j JOIN post p ON j.job_id = p.job_id JOIN requester r ON p.user_id = r.user_id WHERE r.user_id = %s;"
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


@api_router.post('/posts/search')
def search_post_user(job_user: JobUser):
    try:
        conn = create_connection()
        # Usar dictionary=True para obtener resultados como diccionarios
        with conn.cursor() as cur:
            query = "SELECT j.job_id, j.neighborhood, j.job_tittle, j.job_description, p.publish_date FROM job j JOIN post p ON j.job_id = p.job_id JOIN requester r ON p.user_id = r.user_id WHERE r.user_id = %s AND LOWER(j.job_tittle) LIKE LOWER(%s);"
            cur.execute(
                query, (job_user.user_id, '%' + job_user.job_tittle + '%'))

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
    uvicorn.run("app:app", host="0.0.0.0", port=8081, reload=True)
