from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .models import Operador, Unidad, Viaje
from .rules import (
    cumple_licencia,
    cumple_base,
    cumple_disponible,
    cumple_horas,
)

@dataclass
class Asignacion:
    viaje_id: str
    unidad_id: str
    operador_id: Optional[str]
    motivo: str

def _score(operador: Operador, viaje: Viaje) -> float:
    # menor score = mejor
    return (viaje.prioridad * 1000.0) + (operador.costo_hora * viaje.duracion_horas)

def asignar_operadores_v1(
    operadores: List[Operador],
    unidades: Dict[str, Unidad],
    viajes: List[Viaje],
) -> List[Asignacion]:
    """
    MVP v1:
    - Ordena viajes por prioridad y salida
    - Para cada viaje: elige el operador elegible con mejor score
    - Restricción simple: 1 operador = 1 viaje por corrida (para empezar)
    """

    viajes_ordenados = sorted(viajes, key=lambda v: (v.prioridad, v.salida))
    operadores_por_id = {o.id_operador: o for o in operadores}

    usados = set()  # operador ya asignado (MVP)
    asignaciones: List[Asignacion] = []

    for v in viajes_ordenados:
        unidad = unidades.get(v.unidad_id)

        if unidad is None:
            asignaciones.append(Asignacion(v.id_viaje, v.unidad_id, None, "Unidad no existe"))
            continue
        if not unidad.activa:
            asignaciones.append(Asignacion(v.id_viaje, v.unidad_id, None, "Unidad inactiva"))
            continue

        candidatos: List[Tuple[float, Operador]] = []

        for o in operadores_por_id.values():
            if o.id_operador in usados:
                continue
            if not cumple_disponible(o):
                continue
            if not cumple_licencia(o, unidad):
                continue
            if not cumple_base(o, unidad):
                continue
            if not cumple_horas(o, v):
                continue

            candidatos.append((_score(o, v), o))

        if not candidatos:
            asignaciones.append(Asignacion(v.id_viaje, v.unidad_id, None, "Sin operador elegible"))
            continue

        candidatos.sort(key=lambda x: x[0])
        mejor = candidatos[0][1]
        usados.add(mejor.id_operador)

        asignaciones.append(Asignacion(v.id_viaje, v.unidad_id, mejor.id_operador, "OK"))

    return asignaciones
