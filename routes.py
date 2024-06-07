from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from auth import models
from sqlalchemy.orm import Session  # type: ignore
import auth
from database import get_db
from views.home import index
import jwt
from jwt import PyJWTError

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    return index()


# Route to generate access token
@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
  
    student = auth.authenticate_student(form_data.username, form_data.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect student code or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": student.student_code},
                                       expires_delta=access_token_expires)
    return RedirectResponse(
        url="/students/me",
        status_code=302,
        headers={
            "set-cookie":
            f"access_token={access_token}; Max-Age={180}; Path=/students"
        })
   


# Protected route that requires authentication
@router.get("/students/me", response_class=HTMLResponse)
async def read_students_me(request: Request,
                           access_token: Annotated[str | None,
                                                   Cookie()] = None):
    if access_token is None:
        print("No access token")
        return RedirectResponse(url="/", status_code=302)
    try:
        payload = jwt.decode(access_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        student_code: str = payload.get("sub")
        if student_code is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    return {"Request":request,"Codigo":student_code}