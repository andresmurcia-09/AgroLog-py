from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.application.dtos.recordatorio_dto import RecordatorioCreate, RecordatorioResponse, RecordatorioUpdate, RecordatorioDetalleResponse
from app.domain.services.recordatorio_service import RecordatorioService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.recordatorio_repository_impl import RecordatorioRepositoryImpl
from app.infrastructure.repositories.aplicacion_repository_impl import AplicacionRepositoryImpl
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=RecordatorioResponse, status_code=status.HTTP_201_CREATED)
async def crear_recordatorio(
    recordatorio_data: RecordatorioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    # Verificar que la aplicación pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(recordatorio_data.aplicacion_id)
    if not aplicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )
    
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear recordatorios para esta aplicación"
        )
    
    try:
        recordatorio = recordatorio_service.crear_recordatorio(
            aplicacion_id=recordatorio_data.aplicacion_id,
            fecha_recordatorio=recordatorio_data.fecha_recordatorio,
            tipo=recordatorio_data.tipo,
            mensaje=recordatorio_data.mensaje
        )
        return recordatorio
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/pendientes", response_model=List[RecordatorioResponse])
async def listar_recordatorios_pendientes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    try:
        recordatorios = recordatorio_service.listar_recordatorios_pendientes_por_usuario(current_user.id)
        return recordatorios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/fecha/{fecha}", response_model=List[RecordatorioResponse])
async def listar_recordatorios_por_fecha(
    fecha: date,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    try:
        recordatorios = recordatorio_service.listar_recordatorios_por_fecha(fecha, current_user.id)
        return recordatorios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/aplicacion/{aplicacion_id}", response_model=List[RecordatorioResponse])
async def listar_recordatorios_por_aplicacion(
    aplicacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    # Verificar que la aplicación pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(aplicacion_id)
    if not aplicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aplicación no encontrada"
        )
    
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver los recordatorios de esta aplicación"
        )
    
    try:
        recordatorios = recordatorio_service.listar_recordatorios_por_aplicacion(aplicacion_id)
        return recordatorios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{recordatorio_id}", response_model=RecordatorioResponse)
async def obtener_recordatorio(
    recordatorio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    recordatorio = recordatorio_service.obtener_recordatorio(recordatorio_id)
    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado"
        )
    
    # Verificar que el recordatorio pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(recordatorio.aplicacion_id)
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver este recordatorio"
        )
    
    return recordatorio


@router.put("/{recordatorio_id}/completar", response_model=RecordatorioResponse)
async def marcar_recordatorio_completado(
    recordatorio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    # Verificar que el recordatorio exista
    recordatorio = recordatorio_service.obtener_recordatorio(recordatorio_id)
    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado"
        )
    
    # Verificar que el recordatorio pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(recordatorio.aplicacion_id)
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar este recordatorio"
        )
    
    try:
        recordatorio_actualizado = recordatorio_service.marcar_recordatorio_completado(recordatorio_id)
        return recordatorio_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{recordatorio_id}", response_model=RecordatorioResponse)
async def actualizar_recordatorio(
    recordatorio_id: int,
    recordatorio_data: RecordatorioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    # Verificar que el recordatorio exista
    recordatorio = recordatorio_service.obtener_recordatorio(recordatorio_id)
    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado"
        )
    
    # Verificar que el recordatorio pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(recordatorio.aplicacion_id)
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar este recordatorio"
        )
    
    # Actualizar el recordatorio
    recordatorio.fecha_recordatorio = recordatorio_data.fecha_recordatorio or recordatorio.fecha_recordatorio
    recordatorio.tipo = recordatorio_data.tipo or recordatorio.tipo
    recordatorio.mensaje = recordatorio_data.mensaje or recordatorio.mensaje
    
    try:
        recordatorio_actualizado = recordatorio_repository.actualizar(recordatorio)
        return recordatorio_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{recordatorio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_recordatorio(
    recordatorio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    recordatorio_repository = RecordatorioRepositoryImpl(db)
    aplicacion_repository = AplicacionRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    
    recordatorio_service = RecordatorioService(
        recordatorio_repository,
        aplicacion_repository,
        usuario_repository
    )
    
    # Verificar que el recordatorio exista
    recordatorio = recordatorio_service.obtener_recordatorio(recordatorio_id)
    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado"
        )
    
    # Verificar que el recordatorio pertenezca al usuario actual
    aplicacion = aplicacion_repository.obtener_por_id(recordatorio.aplicacion_id)
    if aplicacion.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este recordatorio"
        )
    
    resultado = recordatorio_service.eliminar_recordatorio(recordatorio_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado"
        )