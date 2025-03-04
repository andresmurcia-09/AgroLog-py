from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.application.dtos.aplicacion_dto import AplicacionCreate, AplicacionResponse, AplicacionUpdate, AplicacionDetalleResponse
from app.domain.services.aplicacion_service import AplicacionService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.aplicacion_repository_impl import AplicacionRepositoryImpl
from app.infrastructure.repositories.producto_fitosanitario_repository_impl import ProductoFitosanitarioRepositoryImpl
from app.infrastructure.repositories.cultivo_repository_impl import CultivoRepositoryImpl
from app.infrastructure.repositories.recordatorio_repository_impl import RecordatorioRepositoryImpl
from app.infrastructure.repositories.parcela_repository_impl import ParcelaRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=AplicacionResponse, status_code=status.HTTP_201_CREATED)
async def crear_aplicacion(
    aplicacion_data: AplicacionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    # Verificar que el producto pertenezca al usuario actual
    producto = producto_repository.obtener_por_id(aplicacion_data.producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    if producto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para usar este producto"
        )
    
    # Verificar que el cultivo pertenezca al usuario actual
    cultivo = cultivo_repository.obtener_por_id(aplicacion_data.cultivo_id)
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )
    
    parcela = parcela_repository.obtener_por_id(cultivo.parcela_id)
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para aplicar productos a este cultivo"
        )
    
    try:
        aplicacion = aplicacion_service.crear_aplicacion(
            fecha_aplicacion=aplicacion_data.fecha_aplicacion,
            producto_id=aplicacion_data.producto_id,
            cultivo_id=aplicacion_data.cultivo_id,
            dosis_aplicada=aplicacion_data.dosis_aplicada,
            unidad_medida=aplicacion_data.unidad_medida,
            area_tratada=aplicacion_data.area_tratada,
            motivo=aplicacion_data.motivo,
            observaciones=aplicacion_data.observaciones,
            usuario_id=current_user.id
        )
        return aplicacion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[AplicacionResponse])
async def listar_aplicaciones(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    aplicaciones = aplicacion_service.listar_aplicaciones_por_usuario(current_user.id)
    return aplicaciones


@router.get("/cultivo/{cultivo_id}", response_model=List[AplicacionResponse])
async def listar_aplicaciones_por_cultivo(
    cultivo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    parcela_repository = ParcelaRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    # Verificar que el cultivo pertenezca al usuario actual
    cultivo = cultivo_repository.obtener_por_id(cultivo_id)
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cultivo no encontrado"
        )
    
    parcela = parcela_repository.obtener_por_id(cultivo.parcela_id)
    if parcela.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver las aplicaciones de este cultivo"
        )
    
    try:
        aplicaciones = aplicacion_service.listar_aplicaciones_por_cultivo(cultivo_id)
        return aplicaciones
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/fecha", response_model=List[AplicacionResponse])
async def listar_aplicaciones_por_fecha(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    aplicaciones = aplicacion_service.listar_aplicaciones_por_fecha(fecha_inicio, fecha_fin, current_user.id)
    return aplicaciones


@router.get("/{aplicacion_id}", response_model=AplicacionResponse)
async def obtener_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    aplicacion = aplicacion_service.obtener_aplicacion(aplicacion_id)
    if not aplicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )
    
    # Verificar que la aplicación pertenezca al usuario actual
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver esta aplicación"
        )
    
    return aplicacion


@router.put("/{aplicacion_id}", response_model=AplicacionResponse)
async def actualizar_aplicacion(
    aplicacion_id: int,
    aplicacion_data: AplicacionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    # Verificar que la aplicación exista
    aplicacion = aplicacion_service.obtener_aplicacion(aplicacion_id)
    if not aplicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )
    
    # Verificar que la aplicación pertenezca al usuario actual
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar esta aplicación"
        )
    
    try:
        aplicacion_actualizada = aplicacion_service.actualizar_aplicacion(
            aplicacion_id=aplicacion_id,
            fecha_aplicacion=aplicacion_data.fecha_aplicacion,
            dosis_aplicada=aplicacion_data.dosis_aplicada,
            unidad_medida=aplicacion_data.unidad_medida,
            area_tratada=aplicacion_data.area_tratada,
            motivo=aplicacion_data.motivo,
            observaciones=aplicacion_data.observaciones
        )
        return aplicacion_actualizada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{aplicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    aplicacion_repository = AplicacionRepositoryImpl(db)
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    cultivo_repository = CultivoRepositoryImpl(db)
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    
    aplicacion_service = AplicacionService(
        aplicacion_repository, 
        producto_repository, 
        cultivo_repository, 
        recordatorio_repository
    )
    
    # Verificar que la aplicación exista
    aplicacion = aplicacion_service.obtener_aplicacion(aplicacion_id)
    if not aplicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )
    
    # Verificar que la aplicación pertenezca al usuario actual
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar esta aplicación"
        )
    
    resultado = aplicacion_service.eliminar_aplicacion(aplicacion_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )