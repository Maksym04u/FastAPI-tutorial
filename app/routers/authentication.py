from fastapi import status, HTTPException, Depends, Response, APIRouter, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2, main
from ..forms import LoginForm
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Authentication"])


@router.post("/token")
def login_for_access_token(response: Response, user_credentials: LoginForm = Depends(),
                           db: Session = Depends(get_db)):

    user = db.query(models.User).filter(user_credentials.username == models.User.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong data")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong data")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)
    # return token
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
            login_for_access_token(response=response, user_credentials=form, db=db)

            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect email or password")
            return main.templates.TemplateResponse("login.html", form.__dict__)
    return RedirectResponse("/")
