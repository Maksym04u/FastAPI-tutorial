from .. import models, utils, schemas
from fastapi import status, HTTPException, Depends, APIRouter, Request
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    # hash password - user.password

    hashed_password = utils.hashes(form_data.get("password"))
    email = form_data.get("email")
    user = {"email": email, "password": hashed_password}
    new_user = models.User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found.")

    return user
