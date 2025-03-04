from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.dtos.producto_fitosanitario_dto import ProductoFitosanitarioCreate, ProductoFitosanitarioResponse, ProductoFitosanitarioUpdate
from app.domain.services.producto_fitosanitario_service import ProductoFitosanitarioService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.producto_fitosanitario_repository_impl import ProductoFitosanitarioRepositoryImpl
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from app.infrastructure.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=ProductoFitosanitarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(
        producto_data: ProductoFitosanitarioCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    try:
        producto = producto_service.crear_producto(
            nombre=producto_data.nombre,
            tipo=producto_data.tipo,
            fabricante=producto_data.fabricante,
            principio_activo=producto_data.principio_activo,
            dosis_recomendada=producto_data.dosis_recomendada,
            periodo_carencia=producto_data.periodo_carencia,
            usuario_id=current_user.id
        )
        return producto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ProductoFitosanitarioResponse])
async def listar_productos(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    try:
        productos = producto_service.listar_productos_por_usuario(current_user.id)
        return productos
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tipo/{tipo}", response_model=List[ProductoFitosanitarioResponse])
async def listar_productos_por_tipo(
        tipo: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    try:
        productos = producto_service.listar_productos_por_tipo(tipo, current_user.id)
        return productos
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{producto_id}", response_model=ProductoFitosanitarioResponse)
async def obtener_producto(
        producto_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    producto = producto_service.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Verificar que el producto pertenezca al usuario actual
    if producto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver este producto"
        )

    return producto


@router.put("/{producto_id}", response_model=ProductoFitosanitarioResponse)
async def actualizar_producto(
        producto_id: int,
        producto_data: ProductoFitosanitarioUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    # Verificar que el producto exista
    producto = producto_service.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Verificar que el producto pertenezca al usuario actual
    if producto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para actualizar este producto"
        )

    try:
        producto_actualizado = producto_service.actualizar_producto(
            producto_id=producto_id,
            nombre=producto_data.nombre,
            tipo=producto_data.tipo,
            fabricante=producto_data.fabricante,
            principio_activo=producto_data.principio_activo,
            dosis_recomendada=producto_data.dosis_recomendada,
            periodo_carencia=producto_data.periodo_carencia
        )
        return producto_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
        producto_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    producto_repository = ProductoFitosanitarioRepositoryImpl(db)
    usuario_repository = UsuarioRepositoryImpl(db)
    producto_service = ProductoFitosanitarioService(producto_repository, usuario_repository)

    # Verificar que el producto exista
    producto = producto_service.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Verificar que el producto pertenezca al usuario actual
    if producto.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para eliminar este producto"
        )

    resultado = producto_service.eliminar_producto(producto_id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )