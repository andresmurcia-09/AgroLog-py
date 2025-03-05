from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.application.dtos.usuario_dto import Token, UsuarioLogin, UsuarioCreate, UsuarioResponse
from app.application.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.services.usuario_service import UsuarioService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        usuario_repository = UsuarioRepositoryImpl(db)
        usuario_service = UsuarioService(usuario_repository)

        usuario = usuario_service.autenticar_usuario(form_data.username, form_data.password)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(usuario.id)}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login/mobile", response_model=Token)
async def login_mobile(usuario_data: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        usuario_repository = UsuarioRepositoryImpl(db)
        usuario_service = UsuarioService(usuario_repository)

        usuario = usuario_service.autenticar_usuario(usuario_data.email, usuario_data.password)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(usuario.id)}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/registro", response_model=UsuarioResponse)
async def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario_repository = UsuarioRepositoryImpl(db)
        usuario_service = UsuarioService(usuario_repository)

        usuario = usuario_service.crear_usuario(
            nombre=usuario_data.nombre,
            apellido=usuario_data.apellido,
            email=usuario_data.email,
            password=usuario_data.password
        )
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/me", response_model=UsuarioResponse)
async def obtener_usuario_actual(current_user: UsuarioResponse = Depends(get_current_user)):
    return current_user
