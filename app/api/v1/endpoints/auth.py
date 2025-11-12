from fastapi import APIRouter, Form

from app.core.security import *
from app.core.exceptions import *
from app.models.user import User

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedException(message="Invalid username or password")
    if user.role != "dispatcher":
        raise UnauthorizedException(message="User role not authorized")

    access = create_access_token({"sub": user.username, "role": user.role})
    refresh = create_refresh_token({"sub": user.username, "role": user.role})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    username = validate_refresh_token(refresh_token)
    if not username:
        raise UnauthorizedException(message="Invalid refresh token")
    new_access_token = create_access_token({"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(refresh: str):
    blacklisted_tokens.add(refresh)
    return {"message": "Successfully logged out. "}
