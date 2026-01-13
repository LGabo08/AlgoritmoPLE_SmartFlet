from datetime import datetime
from domain.models import Operador, Unidad, Viaje
from domain.optimizer_v1 import asignar_operadores_v1

def imprimir_tabla(asignaciones):
    headers = ["viaje_id", "unidad_id", "operador_id", "motivo"]
    rows = [[a.viaje_id, a.unidad_id, a.operador_id or "-", a.motivo] for a in asignaciones]

    # calcular anchos
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))

    # helpers
    def line(sep="+", fill="-"):
        return sep + sep.join(fill * (w + 2) for w in widths) + sep

    def fmt_row(r):
        return "| " + " | ".join(str(r[i]).ljust(widths[i]) for i in range(len(headers))) + " |"

    print(line())
    print(fmt_row(headers))
    print(line())
    for r in rows:
        print(fmt_row(r))
    print(line())

def main():
    operadores = [
        Operador(id_operador="OP01", nombre="Juan", licencia_tipo="B", base="Veracruz", costo_hora=120),
        Operador(id_operador="OP02", nombre="Luis", licencia_tipo="FEDERAL", base="Veracruz", costo_hora=150),
        Operador(id_operador="OP03", nombre="Ana", licencia_tipo="B", base="Puebla", costo_hora=110),
    ]

    unidades = {
        "U01": Unidad(id_unidad="U01", tipo="Torton", requiere_licencia="B", base="Veracruz", activa=True),
        "U02": Unidad(id_unidad="U02", tipo="Tracto", requiere_licencia="FEDERAL", base="Veracruz", activa=True),
    }

    viajes = [
        Viaje(id_viaje="V01", origen="Veracruz", destino="Xalapa",
              salida=datetime(2026, 1, 13, 8, 0), duracion_horas=5, unidad_id="U01", prioridad=1),
        Viaje(id_viaje="V02", origen="Veracruz", destino="CDMX",
              salida=datetime(2026, 1, 13, 9, 0), duracion_horas=8, unidad_id="U02", prioridad=2),
        Viaje(id_viaje="V03", origen="Puebla", destino="CDMX",
              salida=datetime(2026, 1, 13, 10, 0), duracion_horas=6, unidad_id="U01", prioridad=3),
    ]

    asignaciones = asignar_operadores_v1(operadores, unidades, viajes)
    imprimir_tabla(asignaciones)

if __name__ == "__main__":
    main()
