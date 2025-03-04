from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Recordatorio:
    id: Optional[int]
    aplicacion_id: int
    fecha_recordatorio: date
    tipo: str
    mensaje: str
    completado: bool
    fecha_registro: datetime