from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.dtos.cultivo_dto import CultivoCreate, CultivoResponse, CultivoUpdate
from app.domain.services.cultivo_service import CultivoService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.cultivo_repository_impl import CultivoRepositoryImpl
from app.infrastructure.repositories.parcela_repository_impl import ParcelaRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=CultivoResponse, status_code=status.HTTP_201_CREATED)
async def crear_cultivo(
    cultivo_data: CultivoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    # Verificar que la parcela pertenezca al usuario actual
    parcela = parcela_repository.obtener_por_id(cultivo_data.parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )
    
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear cultivos en esta parcela"
        )
    
    try:
        cultivo = cultivo_service.crear_cultivo(
            nombre=cultivo_data.nombre,
            variedad=cultivo_data.variedad,
            fecha_siembra=cultivo_data.fecha_siembra,
            fecha_cosecha_estimada=cultivo_data.fecha_cosecha_estimada,
            parcela_id=cultivo_data.parcela_id
        )
        return cultivo
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CultivoResponse])
async def listar_cultivos_por_usuario(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    cultivos = cultivo_service.listar_cultivos_por_usuario(current_user.id)
    return cultivos


@router.get("/parcela/{parcela_id}", response_model=List[CultivoResponse])
async def listar_cultivos_por_parcela(
    parcela_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    # Verificar que la parcela pertenezca al usuario actual
    parcela = parcela_repository.obtener_por_id(parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada"
        )
    
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver los cultivos de esta parcela"
        )
    
    try:
        cultivos = cultivo_service.listar_cultivos_por_parcela(parcela_id)
        return cultivos
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{cultivo_id}", response_model=CultivoResponse)
async def obtener_cultivo(
    cultivo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    cultivo = cultivo_service.obtener_cultivo(cultivo_id)
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )
    
    # Verificar que el cultivo pertenezca al usuario actual
    parcela = parcela_repository.obtener_por_id(cultivo.parcela_id)
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver este cultivo"
        )
    
    return cultivo


@router.put("/{cultivo_id}", response_model=CultivoResponse)
async def actualizar_cultivo(
    cultivo_id: int,
    cultivo_data: CultivoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    # Verificar que el cultivo exista
    cultivo = cultivo_service.obtener_cultivo(cultivo_id)
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )
    
    # Verificar que el cultivo pertenezca al usuario actual
    parcela = parcela_repository.obtener_por_id(cultivo.parcela_id)
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar este cultivo"
        )
    
    try:
        cultivo_actualizado = cultivo_service.actualizar_cultivo(
            cultivo_id=cultivo_id,
            nombre=cultivo_data.nombre,
            variedad=cultivo_data.variedad,
            fecha_siembra=cultivo_data.fecha_siembra,
            fecha_cosecha_estimada=cultivo_data.fecha_cosecha_estimada
        )
        return cultivo_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{cultivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cultivo(
    cultivo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cultivo_repository = CultivoRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    cultivo_service = CultivoService(cultivo_repository, parcela_repository)
    
    # Verificar que el cultivo exista
    cultivo = cultivo_service.obtener_cultivo(cultivo_id)
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )
    
    # Verificar que el cultivo pertenezca al usuario actual
    parcela = parcela_repository.obtener_por_id(cultivo.parcela_id)
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este cultivo"
        )
    
    resultado = cultivo_service.eliminar_cultivo(cultivo_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )