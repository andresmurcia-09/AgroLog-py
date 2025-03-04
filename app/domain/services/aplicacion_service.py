from datetime import datetime, date, timedelta
from typing import List, Optional

from app.domain.entities.aplicacion import Aplicacion
from app.domain.entities.recordatorio import Recordatorio
from app.domain.repositories.aplicacion_repository import AplicacionRepository
from app.domain.repositories.producto_fitosanitario_repository import ProductoFitosanitarioRepository
from app.domain.repositories.cultivo_repository import CultivoRepository
from app.domain.repositories.recordatorio_repository import RecordatorioRepository


class AplicacionService:
    def __init__(self, aplicacion_repository: AplicacionRepository, 
                producto_repository: ProductoFitosanitarioRepository,
                cultivo_repository: CultivoRepository,
                recordatorio_repository: RecordatorioRepository):
        self.aplicacion_repository = aplicacion_repository
        self.producto_repository = producto_repository
        self.cultivo_repository = cultivo_repository
        self.recordatorio_repository = recordatorio_repository
    
    def crear_aplicacion(self, fecha_aplicacion: date, producto_id: int, cultivo_id: int,
                        dosis_aplicada: float, unidad_medida: str, area_tratada: float,
                        motivo: str, observaciones: str, usuario_id: int) -> Aplicacion:
        producto = self.producto_repository.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        cultivo = self.cultivo_repository.obtener_por_id(cultivo_id)
        if not cultivo:
            raise ValueError("Cultivo no encontrado")
        
        fecha_segura_reingreso = None
        if producto.periodo_carencia:
            fecha_segura_reingreso = fecha_aplicacion + timedelta(days=producto.periodo_carencia)
        
        nueva_aplicacion = Aplicacion(
            id=None,
            fecha_aplicacion=fecha_aplicacion,
            producto_id=producto_id,
            cultivo_id=cultivo_id,
            dosis_aplicada=dosis_aplicada,
            unidad_medida=unidad_medida,
            area_tratada=area_tratada,
            motivo=motivo,
            observaciones=observaciones,
            fecha_segura_reingreso=fecha_segura_reingreso,
            usuario_id=usuario_id,
            fecha_registro=datetime.now()
        )
        
        aplicacion_creada = self.aplicacion_repository.crear(nueva_aplicacion)
        
        if fecha_segura_reingreso:
            recordatorio = Recordatorio(
                id=None,
                aplicacion_id=aplicacion_creada.id,
                fecha_recordatorio=fecha_segura_reingreso,
                tipo="reingreso",
                mensaje=f"Fecha segura para reingresar al cultivo tratado con {producto.nombre}",
                completado=False,
                fecha_registro=datetime.now()
            )
            self.recordatorio_repository.crear(recordatorio)
        
        return aplicacion_creada
    
    def obtener_aplicacion(self, aplicacion_id: int) -> Optional[Aplicacion]:
        return self.aplicacion_repository.obtener_por_id(aplicacion_id)
    
    def listar_aplicaciones_por_cultivo(self, cultivo_id: int) -> List[Aplicacion]:
        cultivo = self.cultivo_repository.obtener_por_id(cultivo_id)
        if not cultivo:
            raise ValueError("Cultivo no encontrado")
        
        return self.aplicacion_repository.listar_por_cultivo(cultivo_id)
    
    def listar_aplicaciones_por_usuario(self, usuario_id: int) -> List[Aplicacion]:
        return self.aplicacion_repository.listar_por_usuario(usuario_id)
    
    def listar_aplicaciones_por_fecha(self, fecha_inicio: date, fecha_fin: date, usuario_id: int) -> List[Aplicacion]:
        return self.aplicacion_repository.listar_por_fecha(fecha_inicio, fecha_fin, usuario_id)
    
    def actualizar_aplicacion(self, aplicacion_id: int, fecha_aplicacion: date = None,
                             dosis_aplicada: float = None, unidad_medida: str = None,
                             area_tratada: float = None, motivo: str = None,
                             observaciones: str = None) -> Aplicacion:
        aplicacion = self.aplicacion_repository.obtener_por_id(aplicacion_id)
        if not aplicacion:
            raise ValueError("Aplicación no encontrada")
        
        if fecha_aplicacion:
            aplicacion.fecha_aplicacion = fecha_aplicacion
            producto = self.producto_repository.obtener_por_id(aplicacion.producto_id)
            if producto and producto.periodo_carencia:
                aplicacion.fecha_segura_reingreso = fecha_aplicacion + timedelta(days=producto.periodo_carencia)
                
                recordatorios = self.recordatorio_repository.listar_por_aplicacion(aplicacion_id)
                recordatorio_reingreso = next((r for r in recordatorios if r.tipo == "reingreso"), None)
                
                if recordatorio_reingreso:
                    recordatorio_reingreso.fecha_recordatorio = aplicacion.fecha_segura_reingreso
                    self.recordatorio_repository.actualizar(recordatorio_reingreso)
                else:
                    nuevo_recordatorio = Recordatorio(
                        id=None,
                        aplicacion_id=aplicacion_id,
                        fecha_recordatorio=aplicacion.fecha_segura_reingreso,
                        tipo="reingreso",
                        mensaje=f"Fecha segura para reingresar al cultivo tratado con {producto.nombre}",
                        completado=False,
                        fecha_registro=datetime.now()
                    )
                    self.recordatorio_repository.crear(nuevo_recordatorio)
        
        if dosis_aplicada is not None:
            aplicacion.dosis_aplicada = dosis_aplicada
        if unidad_medida:
            aplicacion.unidad_medida = unidad_medida
        if area_tratada is not None:
            aplicacion.area_tratada = area_tratada
        if motivo:
            aplicacion.motivo = motivo
        if observaciones:
            aplicacion.observaciones = observaciones
        
        return self.aplicacion_repository.actualizar(aplicacion)
    
    def eliminar_aplicacion(self, aplicacion_id: int) -> bool:
        aplicacion = self.aplicacion_repository.obtener_por_id(aplicacion_id)
        if not aplicacion:
            raise ValueError("Aplicación no encontrada")
        
        recordatorios = self.recordatorio_repository.listar_por_aplicacion(aplicacion_id)
        for recordatorio in recordatorios:
            self.recordatorio_repository.eliminar(recordatorio.id)
        
        return self.aplicacion_repository.eliminar(aplicacion_id)