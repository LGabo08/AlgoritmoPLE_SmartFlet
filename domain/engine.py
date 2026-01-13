from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from .models import Operador, Unidad, Viaje
from .rules import cumple_licencia, cumple_base, cumple_disponibilidad, cumple_horas

@dataclass
class Asignacion:
    viaje_id: str
    operador_id: Optional[str]
    unidad_id: str
    motivo: str

def score(operador: Operador, viaje: Viaje, unidad: Unidad) -> float:
    # Menor score = mejor
    # 1) prioridad del viaje pesa mucho
    # 2) costo
    # 3) penalizar si base no coincide (aunque hoy lo bloqueamos)
    return (viaje.prioridad * 1000) + (operador.costo_hora * viaje.duracion_horas)

def asignar_greedy(
    operadores: List[Operador],
    unidades: Dict[str, Unidad],
    viajes: List[Viaje],
) -> List[Asignacion]:

    # ordenar viajes: primero los más prioritarios y más cercanos
    viajes_ordenados = sorted(viajes, key=lambda v: (v.prioridad, v.salida))

    disponibles = {o.id_operador: o for o in operadores}
    asignaciones: List[Asignacion] = []

    usados = set()  # operador ya asignado (MVP: 1 viaje por corrida)

    for v in viajes_ordenados:
        unidad = unidades.get(v.unidad_id)
        if not unidad or not unidad.activa:
            asignaciones.append(Asignacion(v.id_viaje, None, v.unidad_id, "Unidad inexistente o inactiva"))
            continue

        candidatos: List[Tuple[float, Operador]] = []
        for o in disponibles.values():
            if o.id_operador in usados:
                continue
            if not cumple_licencia(o, unidad):
                continue
            if not cumple_base(o, unidad):
                continue
            if not cumple_disponibilidad(o, v):
                continue
            if not cumple_horas(o, v):
                continue

            candidatos.append((score(o, v, unidad), o))

        if not candidatos:
            asignaciones.append(Asignacion(v.id_viaje, None, v.unidad_id, "Sin operador elegible"))
            continue

        candidatos.sort(key=lambda x: x[0])
        mejor = candidatos[0][1]
        usados.add(mejor.id_operador)

        asignaciones.append(Asignacion(v.id_viaje, mejor.id_operador, v.unidad_id, "OK"))

    return asignaciones
