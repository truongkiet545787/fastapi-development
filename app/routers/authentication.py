from fastapi import HTTPException,APIRouter, status, Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from .. import utils
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags= ['Authentication']
)
@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    check_hassed = utils.verify(user_credential.password, user.password)
    if not check_hassed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    access_token = oauth2.create_access_token(data={
        "user_id": user.id
    })
    return {"access_token": access_token, "token_type": "bearer"}