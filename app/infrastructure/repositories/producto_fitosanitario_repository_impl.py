from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.producto_fitosanitario import ProductoFitosanitario
from app.domain.repositories.producto_fitosanitario_repository import ProductoFitosanitarioRepository
from app.infrastructure.persistence import models


class ProductoFitosanitarioRepositoryImpl(ProductoFitosanitarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, producto: ProductoFitosanitario) -> ProductoFitosanitario:
        db_producto = models.ProductoFitosanitario(
            nombre=producto.nombre,
            tipo=producto.tipo,
            fabricante=producto.fabricante,
            principio_activo=producto.principio_activo,
            dosis_recomendada=producto.dosis_recomendada,
            periodo_carencia=producto.periodo_carencia,
            usuario_id=producto.usuario_id,
            fecha_registro=producto.fecha_registro,
            activo=producto.activo
        )
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)

        return self._map_to_entity(db_producto)

    def obtener_por_id(self, producto_id: int) -> Optional[ProductoFitosanitario]:
        db_producto = self.db.query(models.ProductoFitosanitario).filter(
            models.ProductoFitosanitario.id == producto_id
        ).first()

        if db_producto is None:
            return None

        return self._map_to_entity(db_producto)

    def listar_por_usuario(self, usuario_id: int) -> List[ProductoFitosanitario]:
        db_productos = self.db.query(models.ProductoFitosanitario).filter(
            models.ProductoFitosanitario.usuario_id == usuario_id,
            models.ProductoFitosanitario.activo == True
        ).all()

        return [self._map_to_entity(db_producto) for db_producto in db_productos]

    def listar_por_tipo(self, tipo: str, usuario_id: int) -> List[ProductoFitosanitario]:
        db_productos = self.db.query(models.ProductoFitosanitario).filter(
            models.ProductoFitosanitario.tipo == tipo,
            models.ProductoFitosanitario.usuario_id == usuario_id,
            models.ProductoFitosanitario.activo == True
        ).all()

        return [self._map_to_entity(db_producto) for db_producto in db_productos]

    def actualizar(self, producto: ProductoFitosanitario) -> ProductoFitosanitario:
        db_producto = self.db.query(models.ProductoFitosanitario).filter(
            models.ProductoFitosanitario.id == producto.id
        ).first()

        if db_producto is None:
            return None

        db_producto.nombre = producto.nombre
        db_producto.tipo = producto.tipo
        db_producto.fabricante = producto.fabricante
        db_producto.principio_activo = producto.principio_activo
        db_producto.dosis_recomendada = producto.dosis_recomendada
        db_producto.periodo_carencia = producto.periodo_carencia
        db_producto.activo = producto.activo

        self.db.commit()
        self.db.refresh(db_producto)

        return self._map_to_entity(db_producto)

    def eliminar(self, producto_id: int) -> bool:
        db_producto = self.db.query(models.ProductoFitosanitario).filter(
            models.ProductoFitosanitario.id == producto_id
        ).first()

        if db_producto is None:
            return False

        db_producto.activo = False
        self.db.commit()

        return True

    def _map_to_entity(self, db_producto: models.ProductoFitosanitario) -> ProductoFitosanitario:
        return ProductoFitosanitario(
            id=db_producto.id,
            nombre=db_producto.nombre,
            tipo=db_producto.tipo,
            fabricante=db_producto.fabricante,
            principio_activo=db_producto.principio_activo,
            dosis_recomendada=db_producto.dosis_recomendada,
            periodo_carencia=db_producto.periodo_carencia,
            usuario_id=db_producto.usuario_id,
            fecha_registro=db_producto.fecha_registro,
            activo=db_producto.activo
        )