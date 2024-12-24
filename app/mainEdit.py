from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg,time
from psycopg.rows import dict_row
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import insert
models.Base.metadata.create_all(bind= engine)


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
# Connecting to the database
# while True:
#     try:
#         conn = psycopg.connect(
#             host='localhost',
#             dbname='fastapi',
#             user='postgres',
#             password='12112012',
#             row_factory=dict_row # type: ignore
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)

@app.get('/')
async def root():
    return {'message': "Welcome to my api yayy booo suiii"}

@app.get("/sqlalchemy")
async def test_posts(db:Session = Depends(get_db)):
    posts =db.query(models.Post).all()
    return {"data": posts}
    

@app.get('/posts')
async def get_posts(db:Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    posts = db.execute(select(models.Post)).scalars().all()
    return {'posts':posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db:Session = Depends(get_db)):
    # new_post = cursor.execute("""INSERT INTO posts ("title", "content", "published") VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)).fetchone()
    
    # conn.commit()
    
     new_post = models.Post(title=post.title, content=post.content, published=post.published)
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     
     return {"message": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db:Session = Depends(get_db)):
    try:
        # get_post = cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,)).fetchone()
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        post = result.scalars().first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return {"Post detail": post}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session = Depends(get_db)):
   try:
        # deleted_post = cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,)).fetchone()
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        post = result.scalars().first()
        
        if post is None:
            # Raise a 404 error if the post is not found
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post with id {id} not found.")
        # conn.commit()
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
   except Exception as error:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error {error}")

@app.put("/posts/{id}")
async def update_post(id:int, post: Post, db:Session = Depends(get_db)):
    try:
        # get_post = cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,)).fetchone()
        stmt = select(models.Post).filter(models.Post.id == id)
        result = db.execute(stmt)
        existing_post = result.scalars().first()
        print(existing_post)
        
        if existing_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found.")
        
        existing_post.title = post.title # type: ignore
        existing_post.content = post.content # type: ignore
        existing_post.published = post.published # type: ignore

        db.commit()
        db.refresh(existing_post)
        # updated_post = cursor.execute("""
        # UPDATE posts
        # SET title=%s, content=%s, published= %s
        # WHERE id = %s RETURNING *
        # """, (post.title, post.content, post.published, id)).fetchone()
        # conn.commit()
        
        return {"data": existing_post}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {error}")

