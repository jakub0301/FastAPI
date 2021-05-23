from fastapi import APIRouter, Depends, status, Response, HTTPException
from post import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from post.repository import post


router = APIRouter(
    prefix="/post",
    tags=['Post']
)

#@router.get('/')
#def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)): 
#    posts = db.query(models.Post).all()
#    return posts


@router.get('/{id}')
def show(id: int, response: Response, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with the id {id} is not avaliable")
    
    post.counter += 1
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


#, get_current_user: schemas.User = Depends(oauth2.get_current_user)
@router.post('/new', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedPost)
def new_str(request: schemas.Post, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    request.body = request.body[:160]
    return post.create(request, db) 


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with the id {id} is not avaliable")

    post = db.query(models.Post).filter(models.Post.id ==
     id).delete(synchronize_session=False)
    db.commit()
    return 

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Post, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    request.body = request.body[:160]
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with {id} not found")
    if db.query(models.Post).filter(models.Post.id == id, models.Post.body == request.body).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Post has not been modified")
    
    post.update({"body": request.body, "counter": 0})
    db.commit()
    return f"Messege {id} has been updated"
  