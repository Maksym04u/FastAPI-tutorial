from fastapi import FastAPI, Request, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from starlette.staticfiles import StaticFiles

from .routers import post, user, authentication, vote
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware
from . import models, oauth2
from .database import get_db
from pydantic.types import Optional

#      CRUD         WE should use PLURAL(-s) in the ways of methods. ( /posts ...)
# C - create -> post -> /posts -> @app.post('/posts')
# R - read -> get -> /posts   or  /posts/:id -> @app.get('/posts')  or @app.get('/posts/{id}')
# U - update -> put/patch -> /posts/:id -> @app.put('/posts/{id}')
# put - can update all post, patch update specific information of the post.
# D - delete -> delete -> /posts/:id -> @app.delete('/posts/{id}')


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

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

# Добавити короткий опис посту                          DONE
# Добавити можливість фото як фото посту                DONE
# Добавити дізлайк                                      DONE
# Добавити різницю лайків і дізлайків                   DONE
# Добавити коменти
# Апргрейнути шаблони
# Добавити фільтри ( добавити можливість сортування за датою та за темою (можливо і то і інше))        DONE
# Добавити можливість Search                            DONE
# Пагінація
# Добавити можливість редагування тексту і зображення в тексті і відтворення його з бази даних          DONE


@app.get('/')  # RETURN OUR POSTS   response-model - needs LIST of DICTIONARIES
def get_posts(request: Request, db: Session = Depends(get_db),
              limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    # cursor.execute("SELECT * FROM posts")       # Take ALL information about EVERY POST
    # posts = cursor.fetchall()       # RETURN ALL objects from database.

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    themes = request.query_params.getlist("themes")
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                        models.Post.id == models.Vote.post_id,
                                                                        isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search), models.Post.themes.contains(list(themes))).limit(limit).offset(skip).all()

    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})


@app.get("/login")
def signin(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup")
def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
