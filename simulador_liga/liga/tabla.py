# =============================================================================
# MÓDULO: tabla.py
# PAQUETE: liga
# DESCRIPCIÓN: Gestiona el diccionario maestro de equipos y sus estadísticas.
#              Aquí vive toda la lógica de la tabla de posiciones.
# FUNDAMENTO: Sección 1.1 - Tipos de datos: dict, int, str, bool (Fundamentos A)
#             Sección 1.1 - Estructuras de control: if, elif, else, for (Fundamentos A)
#             Fundamentos B - Funciones: def, parámetros, return
#             Sección 1.4 - Manejo de Errores: raise (para lanzar excepciones)
# =============================================================================


# Se importa la excepción personalizada desde el paquete modular 'excepciones'.
# Fundamento 1.2: "from nombre_modulo import elemento" - importación específica.
from excepciones import EquipoNoRegistradoError


# -----------------------------------------------------------------------------
# FUNCIÓN: crear_tabla
# -----------------------------------------------------------------------------
def crear_tabla():
    # Crea y retorna el diccionario maestro vacío que almacenará todos los equipos.
    # Fundamento 1.1: Un diccionario (dict) almacena datos en pares clave-valor.
    # La clave será el nombre del equipo (str) y el valor sus estadísticas (dict).
    tabla_maestra = {}                       # Se inicializa el diccionario vacío

    # Se retorna el diccionario vacío listo para recibir equipos.
    # Fundamento B: La sentencia 'return' devuelve el resultado de la función.
    return tabla_maestra


# -----------------------------------------------------------------------------
# FUNCIÓN: registrar_equipo
# -----------------------------------------------------------------------------
def registrar_equipo(tabla, nombre_equipo):
    # Registra un nuevo equipo en la tabla maestra con todas sus estadísticas en cero.
    # Parámetros:
    #   tabla        → el diccionario maestro donde se guardan todos los equipos
    #   nombre_equipo → cadena de texto (str) con el nombre del equipo a registrar

    # Se verifica si el equipo ya existe para evitar duplicados.
    # Fundamento 1.1: El operador 'in' permite verificar si una clave existe en un dict.
    if nombre_equipo in tabla:
        # Si el equipo ya existe, no se hace nada y se retorna sin error.
        # La palabra clave 'return' detiene la función en este punto.
        return

    # Si el equipo NO existía, se agrega al diccionario con estadísticas inicializadas.
    # Se crea un diccionario anidado (dict dentro de dict) con todos los contadores en 0.
    # Fundamento 1.1: Los valores enteros (int) se inicializan en cero.
    tabla[nombre_equipo] = {
        "PJ": 0,     # Partidos Jugados: total de partidos disputados por el equipo
        "PG": 0,     # Partidos Ganados: partidos en los que el equipo obtuvo victoria
        "PE": 0,     # Partidos Empatados: partidos que terminaron en igualdad
        "PP": 0,     # Partidos Perdidos: partidos en los que el equipo fue derrotado
        "GF": 0,     # Goles a Favor: total de goles que el equipo ha anotado
        "GC": 0,     # Goles en Contra: total de goles que le han anotado al equipo
        "DIF": 0,    # Diferencia de Goles: GF menos GC (puede ser negativo)
        "PTS": 0     # Puntos Acumulados: 3 por victoria, 1 por empate, 0 por derrota
    }


# -----------------------------------------------------------------------------
# FUNCIÓN: obtener_equipo
# -----------------------------------------------------------------------------
def obtener_equipo(tabla, nombre_equipo):
    # Busca un equipo en la tabla y retorna sus estadísticas.
    # Si el equipo no existe, lanza la excepción personalizada EquipoNoRegistradoError.
    # Parámetros:
    #   tabla        → el diccionario maestro de equipos
    #   nombre_equipo → nombre del equipo a buscar (str)

    # Se verifica si el equipo existe en la tabla usando el operador 'in'.
    # Fundamento 1.1: Operador de pertenencia 'in' para diccionarios.
    if nombre_equipo not in tabla:
        # Si el equipo no está registrado, se lanza la excepción personalizada.
        # Fundamento 1.4: La sentencia 'raise' lanza una excepción de forma deliberada.
        raise EquipoNoRegistradoError(nombre_equipo)

    # Si el equipo sí existe, se retorna el sub-diccionario con sus estadísticas.
    # Fundamento 1.1: Acceso al valor de un diccionario mediante su clave (tabla[clave]).
    return tabla[nombre_equipo]


# -----------------------------------------------------------------------------
# FUNCIÓN: actualizar_estadisticas
# -----------------------------------------------------------------------------
def actualizar_estadisticas(tabla, equipo_local, equipo_visitante, goles_local, goles_visitante):
    # Actualiza las estadísticas de ambos equipos según el resultado del partido.
    # Cumple las reglas oficiales de fútbol:
    #   - Victoria: +3 puntos, Empate: +1 punto, Derrota: 0 puntos
    #   - Simetría de goles: GF local = GC visitante y GF visitante = GC local
    #   - Invariantes: PJ = PG + PE + PP y DIF = GF - GC
    # Parámetros:
    #   tabla             → diccionario maestro de equipos
    #   equipo_local      → nombre del equipo que juega en casa (str)
    #   equipo_visitante  → nombre del equipo que juega de visita (str)
    #   goles_local       → goles anotados por el equipo local (int)
    #   goles_visitante   → goles anotados por el equipo visitante (int)

    # Se llama a obtener_equipo para verificar que ambos equipos existen en la tabla.
    # Si alguno no existe, esta función lanzará EquipoNoRegistradoError automáticamente.
    estadisticas_local = obtener_equipo(tabla, equipo_local)
    estadisticas_visitante = obtener_equipo(tabla, equipo_visitante)

    # Se acumulan los Goles con estricta simetría:
    # Los GF del local son los GC del visitante y viceversa.
    estadisticas_local["GF"] += goles_local
    estadisticas_local["GC"] += goles_visitante
    estadisticas_visitante["GF"] += goles_visitante
    estadisticas_visitante["GC"] += goles_local

    # Se determina el resultado y se actualizan victorias (PG), empates (PE),
    # derrotas (PP) y puntos (PTS) siguiendo las reglas oficiales.
    # Fundamento 1.1: Estructura condicional if/elif/else para evaluar el marcador.
    if goles_local > goles_visitante:
        # CASO 1: Victoria local (+3 PTS al local, 0 al visitante).
        estadisticas_local["PG"] += 1
        estadisticas_local["PTS"] += 3
        estadisticas_visitante["PP"] += 1

    elif goles_visitante > goles_local:
        # CASO 2: Victoria visitante (+3 PTS al visitante, 0 al local).
        estadisticas_visitante["PG"] += 1
        estadisticas_visitante["PTS"] += 3
        estadisticas_local["PP"] += 1

    else:
        # CASO 3: Empate (+1 PTS a cada equipo).
        estadisticas_local["PE"] += 1
        estadisticas_visitante["PE"] += 1
        estadisticas_local["PTS"] += 1
        estadisticas_visitante["PTS"] += 1

    # Recálculo automático de invariantes matemáticas para ambos equipos:
    # 1. PJ = PG + PE + PP (asegura coherencia total en los partidos jugados)
    estadisticas_local["PJ"] = (
        estadisticas_local["PG"] + estadisticas_local["PE"] + estadisticas_local["PP"]
    )
    estadisticas_visitante["PJ"] = (
        estadisticas_visitante["PG"] + estadisticas_visitante["PE"] + estadisticas_visitante["PP"]
    )

    # 2. DIF = GF - GC (diferencia de goles)
    estadisticas_local["DIF"] = estadisticas_local["GF"] - estadisticas_local["GC"]
    estadisticas_visitante["DIF"] = estadisticas_visitante["GF"] - estadisticas_visitante["GC"]


# -----------------------------------------------------------------------------
# FUNCIÓN: ordenar_tabla
# -----------------------------------------------------------------------------
def ordenar_tabla(tabla):
    # Ordena y retorna la tabla de posiciones de forma descendente aplicando
    # la jerarquía de desempate oficial del fútbol:
    #   1. Puntos (PTS) (Mayor a menor)
    #   2. Diferencia de Goles (DIF) (Mayor a menor)
    #   3. Goles a Favor (GF) (Mayor a menor)
    # Parámetros:
    #   tabla → el diccionario maestro de equipos

    # Se convierte el diccionario en una lista de tuplas (nombre, estadisticas)
    # usando .items() para poder ordenarla.
    # Fundamento 1.1: El método .items() de un dict retorna pares (clave, valor).
    lista_equipos = list(tabla.items())

    # Se ordena la lista usando la función built-in sorted().
    # La tupla en key=(PTS, DIF, GF) define la prioridad de desempate en cascada.
    # 'reverse=True' asegura el orden descendente (de mayor a menor).
    # Fundamento B: Funciones lambda para criterios personalizados de ordenamiento.
    tabla_ordenada = sorted(
        lista_equipos,
        key=lambda equipo: (
            equipo[1]["PTS"],
            equipo[1]["DIF"],
            equipo[1]["GF"]
        ),
        reverse=True
    )

    # Se retorna la lista ordenada de tuplas (nombre_equipo, estadisticas).
    return tabla_ordenada


# -----------------------------------------------------------------------------
# FUNCIÓN: buscar_equipo
# -----------------------------------------------------------------------------
def buscar_equipo(tabla, nombre_equipo):
    # Busca un equipo específico en la tabla y retorna sus estadísticas.
    # Si no existe, retorna None para que el llamador decida qué hacer.
    # Parámetros:
    #   tabla        → el diccionario maestro de equipos
    #   nombre_equipo → nombre del equipo a buscar (str)

    # Se usa .get() que retorna None si la clave no existe, sin lanzar error.
    # Fundamento 1.1: El método .get(clave) es más seguro que tabla[clave] para búsquedas.
    estadisticas = tabla.get(nombre_equipo)

    # Se retorna las estadísticas encontradas o None si no existe el equipo.
    return estadisticas
