from fastapi import APIRouter, Depends, status, HTTPException
from post import schemas, database, models, hashing
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(username=request.username, password=hashing.Hash.bcrypt(request.password))
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail=f"User with that username is already registered")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: str,  db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with the id {id} in not avaliable")
    
    return user