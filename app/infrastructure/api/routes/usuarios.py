from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.dtos.usuario_dto import UsuarioResponse, UsuarioUpdate
from app.domain.services.usuario_service import UsuarioService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    # Solo administradores podrían acceder a esta ruta en un sistema real
    usuario_repository = UsuarioRepositoryImpl(db)
    usuario_service = UsuarioService(usuario_repository)
    
    return usuario_service.listar_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    # Verificar que el usuario actual solo pueda ver su propia información
    if usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver la información de este usuario"
        )
    
    usuario_repository = UsuarioRepositoryImpl(db)
    usuario_service = UsuarioService(usuario_repository)
    
    usuario = usuario_service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    # Verificar que el usuario actual solo pueda actualizar su propia información
    if usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar la información de este usuario"
        )
    
    usuario_repository = UsuarioRepositoryImpl(db)
    usuario_service = UsuarioService(usuario_repository)
    
    try:
        usuario = usuario_service.actualizar_usuario(
            usuario_id=usuario_id,
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


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioResponse = Depends(get_current_user)
):
    # Verificar que el usuario actual solo pueda eliminar su propia cuenta
    if usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este usuario"
        )
    
    usuario_repository = UsuarioRepositoryImpl(db)
    usuario_service = UsuarioService(usuario_repository)
    
    resultado = usuario_service.eliminar_usuario(usuario_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )