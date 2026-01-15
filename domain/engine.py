from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set

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


def cumple_tipo_unidad(operador: Operador, unidad: Unidad) -> bool:
    """
    Nueva regla:
    El operador SOLO puede manejar unidades cuyo tipo esté permitido para él.
    Ajusta los nombres de campos según tus modelos.
    """
    # Ejemplos posibles:
    # - operador.tipos_unidad_permitidos = ["TORTON", "TRACTO", ...]
    # - unidad.tipo_unidad = "TRACTO"
    permitidos = set(getattr(operador, "tipos_unidad_permitidos", []) or [])
    tipo = getattr(unidad, "tipo_unidad", None)

    if tipo is None:
        return False  # si no sabemos el tipo, mejor no asignar
    return tipo in permitidos


def _score(operador: Operador, viaje: Viaje) -> float:
    # menor score = mejor
    return (viaje.prioridad * 1000.0) + (operador.costo_hora * viaje.duracion_horas)


def asignar_operadores_v2(
    operadores: List[Operador],
    unidades: Dict[str, Unidad],
    viajes: List[Viaje],
) -> List[Asignacion]:
    """
    MVP v2 (nueva lógica):
    - Ordena viajes por prioridad y salida
    - Para cada viaje: elige el operador elegible con mejor score
    - Restricciones:
        * 1 operador = 1 unidad por corrida (y por ende 1 viaje en este MVP)
        * operador debe poder manejar el tipo/categoría de la unidad
    """

    viajes_ordenados = sorted(viajes, key=lambda v: (v.prioridad, v.salida))
    operadores_por_id = {o.id_operador: o for o in operadores}

    usados_operador: Set[str] = set()          # operador ya asignado en esta corrida
    unidad_por_operador: Dict[str, str] = {}   # operador -> unidad asignada
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
            if o.id_operador in usados_operador:
                continue

            # Si en tu nueva lógica ya existe "unidad_asignada_id" (operador fijo a una unidad), respétalo:
            unidad_fija = getattr(o, "unidad_asignada_id", None)
            if unidad_fija is not None and unidad_fija != unidad.id_unidad:
                continue

            if not cumple_disponible(o):
                continue
            if not cumple_tipo_unidad(o, unidad):
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

        usados_operador.add(mejor.id_operador)
        unidad_por_operador[mejor.id_operador] = unidad.id_unidad  # (ajusta si el campo se llama distinto)

        asignaciones.append(Asignacion(v.id_viaje, v.unidad_id, mejor.id_operador, "OK"))

    return asignaciones
