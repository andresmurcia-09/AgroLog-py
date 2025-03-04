from datetime import datetime
from typing import List, Optional

from app.domain.entities.producto_fitosanitario import ProductoFitosanitario
from app.domain.repositories.producto_fitosanitario_repository import ProductoFitosanitarioRepository
from app.domain.repositories.usuario_repository import UsuarioRepository


class ProductoFitosanitarioService:
    def __init__(self, producto_repository: ProductoFitosanitarioRepository, usuario_repository: UsuarioRepository):
        self.producto_repository = producto_repository
        self.usuario_repository = usuario_repository
    
    def crear_producto(self, nombre: str, tipo: str, fabricante: str, principio_activo: str,
                      dosis_recomendada: str, periodo_carencia: int, usuario_id: int) -> ProductoFitosanitario:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        nuevo_producto = ProductoFitosanitario(
            id=None,
            nombre=nombre,
            tipo=tipo,
            fabricante=fabricante,
            principio_activo=principio_activo,
            dosis_recomendada=dosis_recomendada,
            periodo_carencia=periodo_carencia,
            usuario_id=usuario_id,
            fecha_registro=datetime.now(),
            activo=True
        )
        
        return self.producto_repository.crear(nuevo_producto)
    
    def obtener_producto(self, producto_id: int) -> Optional[ProductoFitosanitario]:
        return self.producto_repository.obtener_por_id(producto_id)
    
    def listar_productos_por_usuario(self, usuario_id: int) -> List[ProductoFitosanitario]:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self.producto_repository.listar_por_usuario(usuario_id)
    
    def listar_productos_por_tipo(self, tipo: str, usuario_id: int) -> List[ProductoFitosanitario]:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self.producto_repository.listar_por_tipo(tipo, usuario_id)
    
    def actualizar_producto(self, producto_id: int, nombre: str = None, tipo: str = None,
                           fabricante: str = None, principio_activo: str = None,
                           dosis_recomendada: str = None, periodo_carencia: int = None) -> ProductoFitosanitario:
        producto = self.producto_repository.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        if nombre:
            producto.nombre = nombre
        if tipo:
            producto.tipo = tipo
        if fabricante:
            producto.fabricante = fabricante
        if principio_activo:
            producto.principio_activo = principio_activo
        if dosis_recomendada:
            producto.dosis_recomendada = dosis_recomendada
        if periodo_carencia is not None:
            producto.periodo_carencia = periodo_carencia
        
        return self.producto_repository.actualizar(producto)
    
    def eliminar_producto(self, producto_id: int) -> bool:
        producto = self.producto_repository.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        return self.producto_repository.eliminar(producto_id)