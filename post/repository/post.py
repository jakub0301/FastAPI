from post import models, schemas
from sqlalchemy.orm import Session


def create(request: schemas.Post, db: Session):
    new_post = models.Post(body=request.body, counter = 0)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 
