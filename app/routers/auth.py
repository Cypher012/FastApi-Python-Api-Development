from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils, oauth2
from sqlalchemy.future import select

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    try:
        stmt = select(models.User).filter(models.User.email == user_credentials.username)
        result = db.execute(stmt)
        user = result.scalars().first()
        
        if user is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
        
        verify = utils.verify(user_credentials.password, user.password)
        print(verify)
        
        if not verify:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
            
        # create a token
        # return token
        
        access_token = oauth2.create_access_token(data = {"user_id":user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")
        
    