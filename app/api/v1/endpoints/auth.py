from fastapi import APIRouter, Form

from app.core.security import *
from app.core.exceptions import *
from app.models.user import User
from app.schemas.auth import *

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login with credentials",
    description="Authenticate user and get access & refresh tokens"
)
def login(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UnauthorizedException(message="Invalid username or password")

    if not verify_password(password, str(user.hashed_password)):
        raise UnauthorizedException(message="Invalid username or password")

    token_data = {
        "sub": user.username,
        "user_id": str(user.id),
        "role": user.role
    }

    access = create_access_token(token_data)
    refresh = create_refresh_token(token_data)

    return LoginResponse(
        access_token=access,
        refresh_token=refresh,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token"
)
def refresh_access_token(
        refresh_token: str = Form(..., description="Refresh token"),
        db: Session = Depends(get_db)
):
    if refresh_token in blacklisted_tokens:
        raise UnauthorizedException(message="Token has been revoked")

    payload = validate_refresh_token(refresh_token)
    if not payload:
        raise UnauthorizedException(message="Invalid or expired refresh token")

    username = payload.get("sub")
    if not username:
        raise UnauthorizedException(message="Invalid token payload")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise NotFoundException(entity='User')

    if user.role != "dispatcher":
        raise UnauthorizedException(message="Access denied")

    new_access_token = create_access_token({
        "sub": username,
        "user_id": str(user.id),
        "role": user.role
    })

    return RefreshResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="Logout user",
    description="Revoke refresh token (logout)"
)
def logout(
        refresh_token: str = Form(..., description="Refresh token to revoke"),
        current_user: User = Depends(get_current_user)
):
    blacklisted_tokens.add(refresh_token)
    return LogoutResponse(
        success=True,
        message="Successfully logged out"
    )

