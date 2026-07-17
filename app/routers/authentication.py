from fastapi import HTTPException,APIRouter, status, Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from .. import utils
router = APIRouter(
    tags= ['Authentication']
)
@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credential: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()
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
    return {'data':'pass'}