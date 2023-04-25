from fastapi import status, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from .. import models, oauth2, database

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def votes(request: Request, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    form_data = await request.form()
    post_id = form_data.get("post_id")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if current_user.id == post.owner_id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You cannot like your own post")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} doesn't exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if found_vote:
        vote_query.delete()
        db.commit()

        return {"message": "successfully deleted vote."}

    new_vote = models.Vote(post_id=post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "successfully added vote."}
