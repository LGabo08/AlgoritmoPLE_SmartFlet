import flet as ft
from datetime import datetime

from domain.models import Operador, Unidad, Viaje
from domain.optimizer_v1 import asignar_operadores_v1


def main(page: ft.Page):
    page.title = "SmartFlet - Asignación de Operadores (v1)"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # ---------------- DATOS DE PRUEBA ----------------
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
        Viaje("V01", "Veracruz", "Xalapa", datetime(2026, 1, 13, 8, 0), 5, "U01", 1),
        Viaje("V02", "Veracruz", "CDMX", datetime(2026, 1, 13, 9, 0), 8, "U02", 2),
        Viaje("V03", "Puebla", "CDMX", datetime(2026, 1, 13, 10, 0), 6, "U01", 3),
    ]

    # ---------------- TABLAS ----------------
    tabla_asignados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Viaje")),
            ft.DataColumn(ft.Text("Unidad")),
            ft.DataColumn(ft.Text("Operador")),
        ],
        rows=[]
    )

    tabla_no_asignados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Viaje")),
            ft.DataColumn(ft.Text("Unidad")),
            ft.DataColumn(ft.Text("Motivo")),
        ],
        rows=[]
    )

    resumen = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    # Contenedores "tipo tab"
    panel_asignados = ft.Column([tabla_asignados], visible=True)
    panel_no_asignados = ft.Column([tabla_no_asignados], visible=False)

    # ---------------- FUNCIONES ----------------
    def mostrar_asignados(e):
        panel_asignados.visible = True
        panel_no_asignados.visible = False
        page.update()

    def mostrar_no_asignados(e):
        panel_asignados.visible = False
        panel_no_asignados.visible = True
        page.update()

    def generar_asignacion(e):
        tabla_asignados.rows.clear()
        tabla_no_asignados.rows.clear()

        asignaciones = asignar_operadores_v1(operadores, unidades, viajes)

        total_ok = 0
        total_no = 0

        for a in asignaciones:
            if a.operador_id:
                total_ok += 1
                tabla_asignados.rows.append(
                    ft.DataRow(
                        # verde suave (compatible con todas)
                        color="#E8F5E9",
                        cells=[
                            ft.DataCell(ft.Text(a.viaje_id)),
                            ft.DataCell(ft.Text(a.unidad_id)),
                            ft.DataCell(ft.Text(a.operador_id)),
                        ],
                    )
                )
            else:
                total_no += 1
                tabla_no_asignados.rows.append(
                    ft.DataRow(
                        # rojo suave (compatible con todas)
                        color="#FFEBEE",
                        cells=[
                            ft.DataCell(ft.Text(a.viaje_id)),
                            ft.DataCell(ft.Text(a.unidad_id)),
                            ft.DataCell(ft.Text(a.motivo)),
                        ],
                    )
                )

        resumen.value = f"Asignados: {total_ok}  |  Sin asignar: {total_no}"

        # Al generar, muestro por defecto Asignados
        panel_asignados.visible = True
        panel_no_asignados.visible = False

        page.update()

    # ---------------- UI ----------------
    page.add(
        ft.Text("SmartFlet – Asignación de Operadores", size=22, weight=ft.FontWeight.BOLD),

        ft.Row(
            [
                ft.Button("Generar asignación", on_click=generar_asignacion),
                ft.Button("Asignados", on_click=mostrar_asignados),
                ft.Button("No asignados", on_click=mostrar_no_asignados),
            ],
            wrap=True,
            spacing=10,
        ),

        resumen,
        ft.Divider(),

        panel_asignados,
        panel_no_asignados,
    )


# EJECUCIÓN EN WEB (evita bloqueos de Windows)
ft.run(main, view=ft.AppView.WEB_BROWSER)
