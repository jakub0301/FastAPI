from fastapi import FastAPI
from post import models
from post.database import engine
from post.routers import post, user, auth

app = FastAPI()

models.Base.metadata.create_all(engine)
 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
