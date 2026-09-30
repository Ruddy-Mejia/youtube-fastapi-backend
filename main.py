from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import pymysql

from database import engine, Base, get_db
import models   # registrar clases
from routers import user, video, category, comment, like
from routers import auth as auth_router
from fastapi.middleware.cors import CORSMiddleware


def ensure_database_exists():
    """
    Se conecta al servidor MySQL SIN especificar la base de datos
    y ejecuta CREATE DATABASE IF NOT EXISTS.
    """
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = int(os.getenv("DB_PORT", 3306))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "youtube_api")

    try:
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        conn.close()
        print(f"✅ Base de datos '{db_name}' verificada/creada.")
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación...")
    ensure_database_exists()

    Base.metadata.create_all(bind=engine) 
    print("Tablas verificadas/creadas.")

    yield

    print("Apagando aplicación...")

app = FastAPI(
    title="YouTube API Simple",
    version="1.0.0",
    lifespan=lifespan,
)


# Montaje de routers
app.include_router(auth_router.router)
app.include_router(user.router)
app.include_router(video.router)
app.include_router(category.router)
app.include_router(comment.router)
app.include_router(like.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def root():
    return {"mensaje": "API funcionando", "docs": "/docs"}