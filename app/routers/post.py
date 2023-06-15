
from fastapi import status, HTTPException, Depends, Response, APIRouter, Request, File, UploadFile
from fastapi.responses import RedirectResponse, StreamingResponse
import io
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from app import main


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/myposts')
def get_my_posts(request: Request, current_user: models.User = Depends(oauth2.get_current_user),
                 db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return main.templates.TemplateResponse("profile.html", {"request": request, "posts": posts})


@router.get('/', response_model=List[schemas.PostOut])  # RETURN OUR POSTS   response-model - needs LIST of DICTIONARIES
def get_posts(request: Request):
    return main.templates.TemplateResponse("create_post.html", {"request": request})


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# WE use @router.post - to send data to API.     response_model - SCHEMA of RETURNING DATA.
                                                            # and API do everything what he needs to do with it.
                                                 # WE used status code to raise HTTP Response 201 - Created.
                                                 # This what is needed by documentation.
async def create_post(request: Request, db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user), file: UploadFile = File(...)):

    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                  # (post.title, post.content, post.published))      # CREATION of our post

    # new_post = cursor.fetchone()    # RETURNING post's data

    # conn.commit()   # SAVE the changes to DATABASE (ADD NEW POST TO DATABASE)
    form = await request.form()
    title = form.get("title")
    content = form.get("quill-html")
    description = form.get("description")
    image = await file.read()
    themes = form.getlist("themes")

    post = {"title": title, "content": content, "description": description, "image": image, "themes": themes}

    new_post = models.Post(owner_id=current_user.id, **post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return RedirectResponse(f"/posts/{new_post.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{id}")    # response_model - SCHEMA of RETURNING DATA
def get_post(request: Request, id: int, db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):

    # WE can get SINGLE post by id.
    # cursor.execute("SELECT * FROM posts WHERE %s = id", (id,))      # CHOOSE post by id
    # post = cursor.fetchone()    # RETURN POST or NONE

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == id).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).first()
    if not post:    # CHECK if our post exists.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

    comments = db.query(models.Comment).filter(id == models.Comment.post_id).all()
    return main.templates.TemplateResponse("post_detail.html", {"request": request, "post": post, "comments": comments,
                                                                "user": current_user})


@router.get("/{id}/image")
def get_post_image(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return StreamingResponse(io.BytesIO(post.image), media_type="image/png")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))    # DELETE post by id AND RETURN it
    # deleted_post = cursor.fetchone()   # RETURN IT or NONE
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    if post.owner_id == current_user.id:
        post_query.delete(synchronize_session=False)    # default value
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot perform requested action.")
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s, created_at = now() WHERE id=%s RETURNING *",
                   # (post.title, post.content, post.published, id))      # UPDATE our post

    # updated_post = cursor.fetchone()    # RETURN post
    # conn.commit()       # SAVE changes to our DATABASE (UPDATE post with certain id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()

    if post1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    if post1.owner_id == current_user.id:
        post_query.update(post.dict(), synchronize_session=False)   # default value
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot perform requested action.")

    db.commit()
    return post_query.first()


@router.get("/{id}/comments")
async def get_comments_of_post(id: int, db: Session = Depends(get_db)):
    post_comments = db.query(models.Comment).filter(id == models.Comment.post_id)

    return post_comments


@router.post("/{id}/comments")
async def create_comment(id: int, payload: dict, db: Session = Depends(get_db),
                         user: models.User = Depends(oauth2.get_current_user)):

    comment = models.Comment(post_id=id, user_id=user.id, comment=payload['text'])
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
