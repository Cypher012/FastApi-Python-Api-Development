from fastapi import status, HTTPException, Depends,APIRouter
from .. import schemas, database
from .. import models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.future import select

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.execute(select(models.Post).filter(models.Post.id == vote.post_id)).scalars().first()
    
    if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post with id {id} not found.")
    
    
    stmt = select(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = db.execute(stmt).scalars().first()
    
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vote already exists")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote created"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote deleted"}  
        