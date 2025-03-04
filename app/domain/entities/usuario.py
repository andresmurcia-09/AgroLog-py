from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    apellido: str
    email: str
    hashed_password: str
    fecha_registro: datetime
    activo: bool = True
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"