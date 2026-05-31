from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth_schema import (
    RegisterRequest, LoginRequest, TokenResponse,
    TokenRefreshRequest, UserResponse
)
from app.utils.jwt import create_access_token, decode_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(user_data)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.authenticate(login_data.email, login_data.password)
    
    access_token, refresh_token = service.create_tokens(user)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRefreshRequest):
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new access token (issue new refresh token for rotation)
    access_token = create_access_token(data={"sub": payload["sub"]})
    refresh_token = request.refresh_token  # or create new one for better security
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }