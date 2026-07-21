from jose import JWTError, jwt
from fastapi import HTTPException,status, Depends
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
SECRET_KEY = 'Kiet0398545787@'
ALGORITHM= 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES= 60
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
def create_access_token(data: dict):
    encoded = data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded.update({
        "exp" : expire
        
    })
    print(encoded)
    encoded_jwt=jwt.encode(encoded,SECRET_KEY,ALGORITHM)
    return encoded_jwt
    
def verify_token(token: str, credential_exception):
    try:
        
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data = schemas.tokendata(id = id)
    except JWTError as e:
        print(e)
        raise credential_exception   
    return token_data
def current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credential', headers={"WWW-Authenticate":"Bearer"}
    )
    return verify_token(token,credential_exception)