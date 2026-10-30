# =============================================================================
# ARCHIVO: __init__.py
# PAQUETE: liga
# DESCRIPCIÓN: Inicializador del paquete 'liga'.
#              Exporta las funciones principales de lógica de negocio.
# FUNDAMENTO: Sección 1.2 - Modularización: "Un paquete es una carpeta que contiene
#             módulos y un archivo especial llamado __init__.py" (Guía Prof. Piñate)
# =============================================================================

from liga.tabla import (
    crear_tabla,
    registrar_equipo,
    obtener_equipo,
    actualizar_estadisticas,
    ordenar_tabla,
    buscar_equipo
)

from liga.partidos import (
    procesar_resultado,
    procesar_lote
)

from liga.torneo import (
    crear_torneo,
    registrar_equipo_torneo,
    generar_calendario,
    registrar_partido_jugado,
    consultar_historial_equipo
)

__all__ = [
    "crear_tabla",
    "registrar_equipo",
    "obtener_equipo",
    "actualizar_estadisticas",
    "ordenar_tabla",
    "buscar_equipo",
    "procesar_resultado",
    "procesar_lote",
    "crear_torneo",
    "registrar_equipo_torneo",
    "generar_calendario",
    "registrar_partido_jugado",
    "consultar_historial_equipo"
]
