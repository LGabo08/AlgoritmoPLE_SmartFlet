from .models import Operador, Unidad, Viaje

def cumple_licencia(operador: Operador, unidad: Unidad) -> bool:
    return operador.licencia_tipo == unidad.requiere_licencia

def cumple_base(operador: Operador, unidad: Unidad) -> bool:
    return operador.base == unidad.base

def cumple_disponible(operador: Operador) -> bool:
    return operador.disponible

def cumple_horas(operador: Operador, viaje: Viaje) -> bool:
    return viaje.duracion_horas <= operador.max_horas_dia
