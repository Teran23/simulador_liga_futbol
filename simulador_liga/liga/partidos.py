
# DESCRIPCIÓN: Procesa resultados de partidos individuales y en lote (batch).
#              Lee líneas con formato: "EquipoLocal - GolesLocal | EquipoVisitante - GolesVisitante"

# FUNDAMENTO: Estructuras de control: for, if 
#             Manejo de Errores: try/except, raise 
#             Funciones: def, return, parámetros



# Se importan las funciones necesarias del módulo tabla dentro del mismo paquete liga.
# Fundamento 1.2: "from nombre_modulo import elemento" para importar funciones específicas.
from liga.tabla import actualizar_estadisticas

# Se importan las excepciones desde el paquete modular 'excepciones'.
from excepciones import EquipoNoRegistradoError, FormatoPartidoInvalidoError


# -----------------------------------------------------------------------------
# FUNCIÓN: procesar_resultado
# -----------------------------------------------------------------------------
def procesar_resultado(tabla, linea):
    # Procesa UNA sola línea de partido, la valida y actualiza la tabla de posiciones.
    # Esta función parsea (analiza) el texto, extrae los datos y llama a actualizar_estadisticas.
    # Parámetros:
    #   tabla → el diccionario maestro de equipos
    #   linea → cadena de texto (str) con el formato del partido

    # Se eliminan los espacios en blanco sobrantes al inicio y al final de la línea.
    # Fundamento 1.1: El método .strip() de una cadena (str) limpia espacios extremos.
    linea = linea.strip()

    # Se verifica que la línea no esté vacía antes de procesarla.
    # Fundamento 1.1: Una cadena vacía es falsy en Python (se evalúa como False).
    if not linea:
        # Si la línea está vacía, se lanza un ValueError con mensaje descriptivo.
        # Fundamento 1.4: 'raise' lanza excepciones deliberadamente para señalar errores.
        raise ValueError("La línea de partido está vacía.")

    # Se divide la línea usando el separador "|" para separar local de visitante.
    # El método .split("|") retorna una lista con las dos partes del partido.
    # Fundamento 1.1: El método .split(separador) divide una cadena en una lista.
    partes = linea.split("|")

    # Se verifica que la línea tenga exactamente 2 partes (local y visitante).
    # Si el formato es incorrecto, no habrá exactamente 2 partes.
    if len(partes) != 2:
        # Si el formato no tiene exactamente un "|", el partido es inválido.
        raise ValueError(f"Formato inválido de partido: '{linea}'. Use: EquipoLocal - GolesLocal | EquipoVisitante - GolesVisitante")

    # Se extrae y limpia cada parte del partido, eliminando espacios sobrantes.
    parte_local = partes[0].strip()        # Parte izquierda del "|": equipo local
    parte_visitante = partes[1].strip()    # Parte derecha del "|": equipo visitante

    # Se divide cada parte usando el separador " - " para separar nombre de goles.
    # Se usa maxsplit=1 para dividir solo en el primer " - " encontrado,
    # lo que permite nombres de equipos que contengan guiones (ej: "Bayern-Munich").
    datos_local = parte_local.split(" - ", maxsplit=1)
    datos_visitante = parte_visitante.split(" - ", maxsplit=1)

    # Se verifica que cada parte tenga exactamente 2 elementos (nombre y goles).
    if len(datos_local) != 2 or len(datos_visitante) != 2:
        # Si la división no resultó en exactamente 2 partes, el formato es incorrecto.
        raise ValueError(f"Formato inválido en los datos del partido: '{linea}'")

    # Se extrae el nombre del equipo local eliminando espacios con .strip().
    # Fundamento 1.1: Las cadenas (str) tienen métodos como .strip() para limpiarlas.
    nombre_local = datos_local[0].strip()

    # Se extrae el nombre del equipo visitante de la misma manera.
    nombre_visitante = datos_visitante[0].strip()

    # Se convierte los goles de texto (str) a número entero (int).
    # La función int() convierte una cadena numérica a entero.
    # Si el texto no es numérico, int() lanzará un ValueError automáticamente.
    # Fundamento 1.5: int() es una función built-in para conversión de tipos.
    goles_local = int(datos_local[1].strip())

    # Se convierte los goles del visitante de str a int de la misma forma.
    goles_visitante = int(datos_visitante[1].strip())

    # Se valida que los goles no sean números negativos (no tiene sentido en fútbol).
    # Fundamento 1.1: Operador relacional '<' para comparar valores numéricos.
    if goles_local < 0 or goles_visitante < 0:
        # Si algún valor de goles es negativo, se lanza un ValueError con mensaje claro.
        raise ValueError(f"Los goles no pueden ser negativos: local={goles_local}, visitante={goles_visitante}")

    # Con todos los datos validados y extraídos, se llama a actualizar_estadisticas.
    # Se pasa la tabla y los 4 datos del partido como argumentos.
    # Fundamento B: Las funciones reciben argumentos cuando se las llama/invoca.
    actualizar_estadisticas(tabla, nombre_local, nombre_visitante, goles_local, goles_visitante)


# -----------------------------------------------------------------------------
# FUNCIÓN: procesar_lote
# -----------------------------------------------------------------------------
def procesar_lote(torneo_o_tabla, lista_partidos):
    # Procesa una lista completa de partidos (lote/batch) uno por uno.
    # Si algún partido tiene error, lo registra y CONTINÚA con el siguiente.
    # Parámetros:
    #   torneo_o_tabla → diccionario del torneo o diccionario de equipos
    #   lista_partidos → lista (list) de cadenas (str), cada una es un partido
    # Retorna:
    #   errores_encontrados → lista con los mensajes de error de partidos fallidos

    # Determinamos si recibimos el diccionario maestro de equipos o la estructura completa del torneo.
    if isinstance(torneo_o_tabla, dict) and "equipos" in torneo_o_tabla:
        tabla = torneo_o_tabla["equipos"]
        torneo = torneo_o_tabla
    else:
        tabla = torneo_o_tabla
        torneo = None

    # Se inicializa una lista vacía para acumular los errores encontrados.
    # Fundamento 1.1: Una lista (list) vacía [] se crea con corchetes.
    errores_encontrados = []

    # Se recorre CADA línea de la lista de partidos usando un bucle for.
    # Fundamento 1.1: El bucle 'for' itera sobre cada elemento de una secuencia.
    for numero_linea, linea in enumerate(lista_partidos, start=1):
        # enumerate() agrega un contador automático a la iteración.
        # 'numero_linea' es el número del partido (1, 2, 3...) para identificar errores.
        # 'linea' es el texto del partido actual en esta iteración del bucle.

        # Se usa try/except para capturar errores sin detener el programa.
        # Fundamento 1.4: El bloque try contiene el código que puede fallar.
        try:
            # Se parsea y extrae la información del partido
            linea_limpia = linea.strip()
            if not linea_limpia:
                raise ValueError("La línea de partido está vacía.")

            partes = linea_limpia.split("|")
            if len(partes) != 2:
                raise ValueError(f"Formato inválido de partido: '{linea_limpia}'. Use: EquipoLocal - GolesLocal | EquipoVisitante - GolesVisitante")

            datos_local = partes[0].strip().split(" - ", maxsplit=1)
            datos_visitante = partes[1].strip().split(" - ", maxsplit=1)

            if len(datos_local) != 2 or len(datos_visitante) != 2:
                raise ValueError(f"Formato inválido en los datos del partido: '{linea_limpia}'")

            nombre_local = datos_local[0].strip()
            nombre_visitante = datos_visitante[0].strip()
            goles_local = int(datos_local[1].strip())
            goles_visitante = int(datos_visitante[1].strip())

            if goles_local < 0 or goles_visitante < 0:
                raise ValueError(f"Los goles no pueden ser negativos: local={goles_local}, visitante={goles_visitante}")

            # Se actualizan las estadísticas en la tabla
            actualizar_estadisticas(tabla, nombre_local, nombre_visitante, goles_local, goles_visitante)

            # Si se dispone del objeto torneo, registramos en el historial
            if torneo is not None and "historial_partidos" in torneo:
                torneo["historial_partidos"].append({
                    "local": nombre_local,
                    "visitante": nombre_visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "jugado": True
                })

        # Se atrapa específicamente el error de equipo no registrado.
        # Fundamento 1.4: Se usa except específico en lugar de genérico (mejor práctica).
        except EquipoNoRegistradoError as error:
            # Si el equipo no existe, se construye un mensaje de error descriptivo.
            mensaje_error = f"Partido {numero_linea}: {error}"
            errores_encontrados.append(mensaje_error)

        # Se atrapa el error de conversión de tipos o validación de datos.
        except ValueError as error:
            mensaje_error = f"Partido {numero_linea} (línea: '{linea.strip()}'): {error}"
            errores_encontrados.append(mensaje_error)

    # Se retorna la lista con todos los errores encontrados durante el procesamiento.
    return errores_encontrados
