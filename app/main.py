from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from .routers import post, user, authentication, vote
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

#      CRUD         WE should use PLURAL(-s) in the ways of methods. ( /posts ...)
# C - create -> post -> /posts -> @app.post('/posts')
# R - read -> get -> /posts   or  /posts/:id -> @app.get('/posts')  or @app.get('/posts/{id}')
# U - update -> put/patch -> /posts/:id -> @app.put('/posts/{id}')
# put - can update all post, patch update specific information of the post.
# D - delete -> delete -> /posts/:id -> @app.delete('/posts/{id}')


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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


@app.get("/")
def hello(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
