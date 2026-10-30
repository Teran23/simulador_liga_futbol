# =============================================================================
# MÓDULO: torneo.py
# PAQUETE: liga
# DESCRIPCIÓN: Administra el torneo completo: metadatos de la liga, registro
#              de equipos, generación de calendario de jornadas (Round-Robin),
#              historial unificado de enfrentamientos y avance de la temporada.
# FUNDAMENTO: Sección 1.1 - Tipos de datos compuestos (dict, list) (Fundamentos A)
#             Sección 1.2 - Modularización: separación de responsabilidades
#             Fundamentos B - Funciones puras con retorno de datos
# =============================================================================

from typing import Dict, List, Any
from excepciones import EquipoNoRegistradoError
from liga.tabla import registrar_equipo as registrar_en_tabla, actualizar_estadisticas


def crear_torneo(nombre: str = "Liga Oficial") -> Dict[str, Any]:
    """
    Crea y retorna la estructura integral de datos del torneo.
    Almacena el nombre, la tabla maestra de equipos, el calendario por jornadas,
    el historial completo de partidos jugados y el índice de progreso.
    """
    nombre_limpio = nombre.strip() if nombre and nombre.strip() else "Liga Oficial"
    return {
        "nombre": nombre_limpio,
        "equipos": {},              # Diccionario maestro: {nombre_equipo: estadisticas}
        "jornadas": [],             # Lista de jornadas (cada jornada es una lista de partidos)
        "historial_partidos": [],   # Lista de partidos completados: [{'local', 'visitante', 'goles_local', 'goles_visitante'}]
        "jornada_actual_idx": 0,    # Índice de la jornada en disputa
        "partido_actual_idx": 0,    # Índice del partido dentro de la jornada activa
        "liga_finalizada": False    # Indicador de fin de temporada
    }


def registrar_equipo_torneo(torneo: Dict[str, Any], nombre_equipo: str) -> None:
    """
    Registra un nuevo equipo dentro del torneo.
    Valida que no esté vacío ni duplicado.
    """
    nombre_limpio = nombre_equipo.strip()
    if not nombre_limpio:
        raise ValueError("El nombre del equipo no puede estar vacío.")

    if nombre_limpio in torneo["equipos"]:
        raise ValueError(f"El equipo '{nombre_limpio}' ya está registrado.")

    registrar_en_tabla(torneo["equipos"], nombre_limpio)


def generar_calendario(torneo: Dict[str, Any]) -> None:
    """
    Genera el calendario completo a dos vueltas (Ida y Vuelta) mediante el
    algoritmo de rotación Round-Robin. Si la cantidad de equipos es impar,
    incluye la marca de descanso.
    """
    nombres = list(torneo["equipos"].keys())
    if len(nombres) < 2:
        raise ValueError("Se necesitan al menos 2 equipos para generar el calendario de la liga.")

    equipos_rotacion = nombres.copy()
    tiene_impar = len(equipos_rotacion) % 2 != 0
    if tiene_impar:
        equipos_rotacion.append("DESCANSA")

    n = len(equipos_rotacion)
    partidos_ida = []

    # Primera vuelta (Ida)
    for i in range(n - 1):
        jornada = []
        for j in range(n // 2):
            eq1 = equipos_rotacion[j]
            eq2 = equipos_rotacion[n - 1 - j]
            if eq1 != "DESCANSA" and eq2 != "DESCANSA":
                if i % 2 == 0:
                    partido = {
                        "local": eq1,
                        "visitante": eq2,
                        "goles_local": 0,
                        "goles_visitante": 0,
                        "jugado": False
                    }
                else:
                    partido = {
                        "local": eq2,
                        "visitante": eq1,
                        "goles_local": 0,
                        "goles_visitante": 0,
                        "jugado": False
                    }
                jornada.append(partido)
        partidos_ida.append(jornada)
        # Rotación circular fija en el primer elemento
        equipos_rotacion = [equipos_rotacion[0]] + [equipos_rotacion[-1]] + equipos_rotacion[1:-1]

    # Segunda vuelta (Vuelta): se invierten las localías de la primera vuelta
    partidos_vuelta = []
    for jornada_ida in partidos_ida:
        jornada_vuelta = [
            {
                "local": p["visitante"],
                "visitante": p["local"],
                "goles_local": 0,
                "goles_visitante": 0,
                "jugado": False
            }
            for p in jornada_ida
        ]
        partidos_vuelta.append(jornada_vuelta)

    torneo["jornadas"] = partidos_ida + partidos_vuelta
    torneo["jornada_actual_idx"] = 0
    torneo["partido_actual_idx"] = 0
    torneo["liga_finalizada"] = False


def registrar_partido_jugado(
    torneo: Dict[str, Any],
    equipo_local: str,
    equipo_visitante: str,
    goles_local: int,
    goles_visitante: int
) -> None:
    """
    Registra el resultado de un partido disputado:
    1. Actualiza las estadísticas oficiales en la tabla maestra.
    2. Agrega el enfrentamiento al historial permanente del torneo.
    """
    actualizar_estadisticas(
        torneo["equipos"],
        equipo_local,
        equipo_visitante,
        goles_local,
        goles_visitante
    )

    registro_partido = {
        "local": equipo_local,
        "visitante": equipo_visitante,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "jugado": True
    }
    torneo["historial_partidos"].append(registro_partido)


def consultar_historial_equipo(torneo: Dict[str, Any], nombre_equipo: str) -> List[Dict[str, Any]]:
    """
    Retorna todos los partidos jugados en los que participó el equipo buscado,
    sea como local o como visitante.
    Lanza EquipoNoRegistradoError si el equipo no forma parte del torneo.
    """
    nombre_limpio = nombre_equipo.strip()
    if nombre_limpio not in torneo["equipos"]:
        raise EquipoNoRegistradoError(nombre_limpio)

    return [
        partido for partido in torneo["historial_partidos"]
        if partido["local"] == nombre_limpio or partido["visitante"] == nombre_limpio
    ]

