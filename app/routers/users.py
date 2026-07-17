from .. import models, schemas, utils, database
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter    
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..utils import hash_password
router = APIRouter(
    tags= ['Users']
)


@router.post('/createuser', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_pass = hash_password(new_user.password)
    new_user.password = hashed_pass
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/getuser/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session =Depends(get_db)):
    user =   db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"user with id: {id} was not found"
        )
    return user

@router.get('/allUser', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def alluser(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
