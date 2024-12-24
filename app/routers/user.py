from fastapi import status, HTTPException, Depends,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
import jwt


router = APIRouter(
    prefix= "/users",
    tags=['Users']
)
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.execute(select(models.User).filter(models.User.email == user.email)).scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash the password
    user.password = utils.hash(user.password)
    
    # Create and save the new user
    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
async def getUser(id: int, db:Session = Depends(get_db)):
    try:
        stmt = select(models.User).filter(models.User.id == id)
        result = db.execute(stmt)
        user = result.scalars().first()
        
        if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
        
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")
    




