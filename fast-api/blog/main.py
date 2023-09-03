from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs

@app.get('/blog/{id}', status_code=200)
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not available')
    return blog