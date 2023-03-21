from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import post, user, authentication
from .routers import vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

#      CRUD         WE should use PLURAL(-s) in the ways of methods. ( /posts ...)
# C - create -> post -> /posts -> @app.post('/posts')
# R - read -> get -> /posts   or  /posts/:id -> @app.get('/posts')  or @app.get('/posts/{id}')
# U - update -> put/patch -> /posts/:id -> @app.put('/posts/{id}')
# put - can update all post, patch update specific information of the post.
# D - delete -> delete -> /posts/:id -> @app.delete('/posts/{id}')


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)


