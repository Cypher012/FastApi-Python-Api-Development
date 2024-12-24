from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.Post])
async def get_posts(db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user) ,limit:int =  10):
    stmt = select(models.Post).limit(limit)
    posts = db.execute(stmt).scalars().all()  # Use .all() after scalars()
    print(limit)
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    
    new_post = models.Post(user_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    try:
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        post = result.scalars().first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return post
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
   try:
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        post = result.scalars().first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post with id {id} not found.")
            
        if post.user_id is not current_user.id: # type: ignore
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Not authorized to make requested action")
        # conn.commit()
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
   except Exception as error:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")

@router.put("/{id}", response_model=schemas.Post)
async def update_post(id:int, post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    try:
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        existing_post = result.scalars().first()
        
        if existing_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found.")
        
        if existing_post.user_id is not current_user.id: # type: ignore
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Not authorized to make requested action")
        
        existing_post.title = post.title # type: ignore
        existing_post.content = post.content # type: ignore
        existing_post.published = post.published # type: ignore
        existing_post.user_id = current_user.id  # type: ignore
        db.commit()
        db.refresh(existing_post)
        
        return existing_post
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {error}")
