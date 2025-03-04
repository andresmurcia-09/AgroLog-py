from datetime import datetime
from typing import List, Optional

from app.domain.entities.parcela import Parcela
from app.domain.repositories.parcela_repository import ParcelaRepository
from app.domain.repositories.usuario_repository import UsuarioRepository


class ParcelaService:
    def __init__(self, parcela_repository: ParcelaRepository, usuario_repository: UsuarioRepository):
        self.parcela_repository = parcela_repository
        self.usuario_repository = usuario_repository
    
    def crear_parcela(self, nombre: str, ubicacion: str, superficie: float, usuario_id: int) -> Parcela:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        nueva_parcela = Parcela(
            id=None,
            nombre=nombre,
            ubicacion=ubicacion,
            superficie=superficie,
            usuario_id=usuario_id,
            fecha_registro=datetime.now(),
            activo=True
        )
        
        return self.parcela_repository.crear(nueva_parcela)
    
    def obtener_parcela(self, parcela_id: int) -> Optional[Parcela]:
        return self.parcela_repository.obtener_por_id(parcela_id)
    
    def listar_parcelas_por_usuario(self, usuario_id: int) -> List[Parcela]:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self.parcela_repository.listar_por_usuario(usuario_id)
    
    def actualizar_parcela(self, parcela_id: int, nombre: str = None, 
                          ubicacion: str = None, superficie: float = None) -> Parcela:
        parcela = self.parcela_repository.obtener_por_id(parcela_id)
        if not parcela:
            raise ValueError("Parcela no encontrada")
        
        if nombre:
            parcela.nombre = nombre
        if ubicacion:
            parcela.ubicacion = ubicacion
        if superficie is not None:
            parcela.superficie = superficie
        
        return self.parcela_repository.actualizar(parcela)
    
    def eliminar_parcela(self, parcela_id: int) -> bool:
        parcela = self.parcela_repository.obtener_por_id(parcela_id)
        if not parcela:
            raise ValueError("Parcela no encontrada")
        
        return self.parcela_repository.eliminar(parcela_id)