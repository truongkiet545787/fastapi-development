from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import Depends, HTTPException, status, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import Base, engine, SessionLocal, get_db
from . import models
from sqlalchemy.orm import Session
from .config import settings
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
   

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


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

def get_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/post")
def root():
    return {'message':'welcome to my first FastAPI project'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {'data': posts}



@app.get("/posts")
def getpost(db: Session =Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
   
    print(post)
    return {'data': post}

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def createpost(newpost: Post, db: Session = Depends(get_db)):
    post = models.Post(**newpost.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"data": post}

@app.get("/post/lastest")
def get_latest_post():
    post = my_posts[-1]
    return {'latest_post' : post}

@app.get("/post/{id}")
def get_postID(id: int, db: Session = Depends(get_db)):
    # 1. Dùng .first() để lấy ra dữ liệu thực tế của bài viết
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} was not found"
        )
        
    # 2. Trả về đối tượng post (dữ liệu thật) chứ không phải Query
    return {'post_detail' : post}

@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # 1. Tạo đối tượng truy vấn (Query) trước
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # 2. Dùng .first() để kiểm tra xem bài viết có tồn tại không
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    
    # 3. Thực thi xóa trực tiếp bằng câu lệnh SQL và commit
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Post deleted successfully"}

@app.put("/post/{id}")
def update_post(id: int, updated_post: PostUpdate, db: Session = Depends(get_db)):
    # 1. Tạo đối tượng truy vấn (Query)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # 2. Kiểm tra sự tồn tại của bài viết
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    
    # 3. Thực hiện cập nhật dữ liệu từ Pydantic Model (PostUpdate)
    # Thêm exclude_unset=True để chỉ cập nhật những trường thực sự được gửi lên
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    
    # 4. Lưu thay đổi xuống Database (Rất quan trọng!)
    db.commit()
    
    # 5. Trả về dữ liệu bài viết mới nhất đã được cập nhật
    return {"data": post_query.first()}
