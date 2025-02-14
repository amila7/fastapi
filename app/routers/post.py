from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import List,Optional
from passlib.context import CryptContext # type: ignore
import psycopg2
from sqlalchemy import func
from psycopg2.extras import RealDictCursor
from .. import models, schemas, models,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get("/", response_model=List[schemas.Post])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),Limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # print(current_user.id)


    #who is the author of the post and get only posts of that auther
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    #all posts
    # posts = db.query(models.Post).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id== models.Post.id,
    isouter=True).group_by(models.Post.id).all()
    
    results = [result for result, _ in results]
    return results



@router.post("/", response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post =db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exit")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this ")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}

@router.put("/{id}")
def update_post(id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exit")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this ")
    post_query.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post_query.first()