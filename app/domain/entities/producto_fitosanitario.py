from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProductoFitosanitario:
    id: Optional[int]
    nombre: str
    tipo: str
    fabricante: Optional[str]
    principio_activo: Optional[str]
    dosis_recomendada: Optional[str]
    periodo_carencia: Optional[int]
    usuario_id: int
    fecha_registro: datetime
    activo: bool = True