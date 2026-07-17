from .. import models, schemas, utils, database
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter    
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
router = APIRouter(
    tags=  ['Posts']
)


@router.get("/post")
def root():
    return {'message':'welcome to my first FastAPI project'}

@router.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {'data': posts}



@router.get("/posts", status_code= status.HTTP_201_CREATED, response_model = List[schemas.PostResponse])
def getpost(db: Session =Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
    return post

@router.post('/createposts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createpost(newpost: schemas.Post, db: Session = Depends(get_db)):
    post = models.Post(**newpost.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post



@router.get("/post/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_postID(id: int, db: Session = Depends(get_db)):
    # 1. Dùng .first() để lấy ra dữ liệu thực tế của bài viết
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} was not found"
        )
        
    # 2. Trả về đối tượng post (dữ liệu thật) chứ không phải Query
    return  post

@router.delete("/post/{id}")
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

@router.put("/post/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
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
    return post_query.first()