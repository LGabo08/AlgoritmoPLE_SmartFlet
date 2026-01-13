from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Operador:
    id_operador: str
    nombre: str
    licencia_tipo: str          # "B", "FEDERAL", etc.
    base: str                   # "Veracruz", etc.
    disponible: bool = True
    max_horas_dia: float = 8.0
    costo_hora: float = 0.0
    ultima_salida: Optional[datetime] = None  # opcional para siguientes versiones


@dataclass(frozen=True)
class Unidad:
    id_unidad: str
    tipo: str
    requiere_licencia: str      # "B", "FEDERAL", etc.
    base: str
    activa: bool = True


@dataclass(frozen=True)
class Viaje:
    id_viaje: str
    origen: str
    destino: str
    salida: datetime
    duracion_horas: float
    unidad_id: str
    prioridad: int = 3          # 1 alta, 5 baja
