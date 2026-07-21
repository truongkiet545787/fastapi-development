from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['votes'],
    prefix='/vote'
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_votes(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: schemas.tokendata = Depends(oauth2.current_user)):
    
    # 1. Kiểm tra xem bài viết (post) có tồn tại trong database không
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {vote.post_id} does not exist"
        )
        
    # 2. Tìm kiếm lượt vote hiện tại của user cho post này
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    
    # 3. Xử lý logic vote
    if (vote.dir == 1):
        # Nếu đã vote rồi thì báo lỗi 409
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"user with id {current_user.id} has already voted on post {vote.post_id}"
            )
        # Nếu chưa vote thì tiến hành tạo mới lượt vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        # Nếu muốn hủy vote mà lượt vote không tồn tại thì báo lỗi 404
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="vote does not exist"
            ) 
        # Nếu tồn tại thì tiến hành xóa lượt vote đó
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}