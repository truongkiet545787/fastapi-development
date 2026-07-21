from .. import models, schemas, utils, database
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter    
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import oauth2
from typing import Optional
from sqlalchemy import func
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



@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def getpost(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.current_user), limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    print(search)
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

@router.post('/createposts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createpost(newpost: schemas.Post, db: Session = Depends(get_db), current_user: schemas.tokendata = Depends(oauth2.current_user)):
    post = models.Post(user_id=current_user.id, **newpost.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post




@router.get("/post/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_postID(id: int, db: Session = Depends(get_db), current_user_id: schemas.tokendata = Depends(oauth2.current_user)):
    # 1. Lấy bài viết từ database
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} was not found"
        )
        
    # 2. Kiểm tra quyền sở hữu
    if post.user_id != current_user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
        
    return  post

@router.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user_id: schemas.tokendata = Depends(oauth2.current_user)):
    # 1. Tạo đối tượng truy vấn (Query) trước
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # 2. Dùng .first() để kiểm tra xem bài viết có tồn tại không
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    if post.user_id !=current_user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    # 3. Thực thi xóa trực tiếp bằng câu lệnh SQL và commit
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Post deleted successfully"}

@router.put("/post/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user_id: schemas.tokendata = Depends(oauth2.current_user)):
    # 1. Tạo đối tượng truy vấn (Query)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # 2. Kiểm tra sự tồn tại của bài viết
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
        
    # 3. Kiểm tra quyền sở hữu
    if post.user_id != current_user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    # 4. Thực hiện cập nhật dữ liệu từ Pydantic Model (PostUpdate)
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    
    # 5. Lưu thay đổi xuống Database (Rất quan trọng!)
    db.commit()
    
    return post_query.first()

@router.delete('/deleteALLPosts')
def deleteALL(db: Session = Depends(get_db)):
    posts_query = db.query(models.Post)
    
    # Check if there are any posts in the database
    if not posts_query.all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No posts found to delete"
        )
    
    # Execute delete on the query to delete all rows and commit
    posts_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "All posts deleted successfully"}

