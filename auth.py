import os
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session  # type: ignore
import models
from database import get_db

# Some secret key to sign and decode JWT tokens
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Functions to verify password and create access token
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_student(student_code: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Student)
        .filter(models.Student.student_code == student_code)
        .first()
    )


def authenticate_student(student_code: str, password: str, db: Session = Depends(get_db)):
    student = get_student(db, student_code)
    if not student:
        return False
    if not verify_password(password, student.password):
        return False
    return student


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_student(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        student_code: str = payload.get("sub")
        print('student code', student_code)
        if student_code is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        student = get_student(db, student_code)
        print('student', student)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError as e:
        print('Error')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    return student
