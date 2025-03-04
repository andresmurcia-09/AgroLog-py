from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.dtos.parcela_dto import ParcelaCreate, ParcelaResponse, ParcelaUpdate
from app.domain.services.parcela_service import ParcelaService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.parcela_repository_impl import ParcelaRepositoryImpl
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=ParcelaResponse, status_code=status.HTTP_201_CREATED)
async def crear_parcela(
    parcela_data: ParcelaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    parcela_repository = ParcelaRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    parcela_service = ParcelaService(parcela_repository, usuario_repository)
    
    try:
        parcela = parcela_service.crear_parcela(
            nombre=parcela_data.nombre,
            ubicacion=parcela_data.ubicacion,
            superficie=parcela_data.superficie,
            usuario_id=current_user.id
        )
        return parcela
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ParcelaResponse])
async def listar_parcelas(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    parcela_repository = ParcelaRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    parcela_service = ParcelaService(parcela_repository, usuario_repository)
    
    try:
        parcelas = parcela_service.listar_parcelas_por_usuario(current_user.id)
        return parcelas
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{parcela_id}", response_model=ParcelaResponse)
async def obtener_parcela(
    parcela_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    parcela_repository = ParcelaRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    parcela_service = ParcelaService(parcela_repository, usuario_repository)
    
    parcela = parcela_service.obtener_parcela(parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )
    
    # Verificar que la parcela pertenezca al usuario actual
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver esta parcela"
        )
    
    return parcela


@router.put("/{parcela_id}", response_model=ParcelaResponse)
async def actualizar_parcela(
    parcela_id: int,
    parcela_data: ParcelaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    parcela_repository = ParcelaRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    parcela_service = ParcelaService(parcela_repository, usuario_repository)
    
    # Verificar que la parcela exista y pertenezca al usuario actual
    parcela = parcela_service.obtener_parcela(parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )
    
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar esta parcela"
        )
    
    try:
        parcela_actualizada = parcela_service.actualizar_parcela(
            parcela_id=parcela_id,
            nombre=parcela_data.nombre,
            ubicacion=parcela_data.ubicacion,
            superficie=parcela_data.superficie
        )
        return parcela_actualizada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{parcela_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_parcela(
    parcela_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    parcela_repository = ParcelaRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    parcela_service = ParcelaService(parcela_repository, usuario_repository)
    
    # Verificar que la parcela exista y pertenezca al usuario actual
    parcela = parcela_service.obtener_parcela(parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )
    
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar esta parcela"
        )
    
    resultado = parcela_service.eliminar_parcela(parcela_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )