from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List  # Import List from typing
from . import models, schemas, crud, deps, auth, cache
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/addpost", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@app.get("/getposts", response_model=List[schemas.Post])
def read_posts(db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    user_cache = cache.get_cache(current_user.id)
    if "posts" in user_cache:
        return user_cache["posts"]
    posts = crud.get_posts_by_user(db=db, user_id=current_user.id)
    user_cache["posts"] = posts
    return posts

@app.delete("/deletepost/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    post = crud.get_posts_by_user(db=db, user_id=current_user.id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db=db, post_id=post_id)
