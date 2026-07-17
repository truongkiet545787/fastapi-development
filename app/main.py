from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from fastapi import Depends, HTTPException, status, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import Base, engine, SessionLocal, get_db
from . import models
from sqlalchemy.orm import Session
from .config import settings
from . import schemas
from .utils import hash_password, pwd_context
from .routers import posts,users,authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# Sử dụng vòng lặp để đảm bảo kết nối ổn định khi khởi động ứng dụng
while True:
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname, 
            database=settings.database_name, 
            user=settings.database_username, 
            password=settings.database_password, 
            port=settings.database_port,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)




