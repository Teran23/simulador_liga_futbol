
# DESCRIPCIÓN: Maneja TODA la entrada y salida por consola/terminal del simulador.
#              Aquí viven los print() e input(). NO contiene lógica de negocio.
#              La separación de I/O y lógica permite cambiar la interfaz sin
#              tocar las reglas del juego.
# FUNDAMENTO: Entrada/Salida: print(), input(), f-strings (Fundamentos A)
#              Separación de responsabilidades (lógica vs interfaz)


import os # modulo nativo para limpiar la consola 


# -----------------------------------------------------------------------------
# FUNCIÓN: limpiar_pantalla
# -----------------------------------------------------------------------------
def limpiar_pantalla():
    """Limpia el contenido de la consola/terminal ejecutando cls en Windows o clear en Unix."""
    os.system('cls' if os.name == 'nt' else 'clear')


# -----------------------------------------------------------------------------
# FUNCIÓN: pausar_continuar
# -----------------------------------------------------------------------------
def pausar_continuar():
    """Pausa la ejecución hasta que el usuario presione Enter para continuar."""
    input("\n  Presione Enter para continuar...")


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_nombre_liga
# -----------------------------------------------------------------------------
def pedir_nombre_liga():
    """Solicita al usuario el nombre del torneo o liga deportiva."""
    print("=" * 60)
    print("   🏆  CONFIGURACIÓN DE LA LIGA DEPORTIVA")
    print("=" * 60)
    print()
    nombre = input("  Ingrese el nombre de la Liga (Enter para 'Liga Oficial'): ").strip()
    return nombre if nombre else "Liga Oficial"


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_bienvenida
# -----------------------------------------------------------------------------
def mostrar_bienvenida(nombre_liga="Liga Oficial"):
    """Muestra en pantalla el encabezado principal del simulador con el nombre del torneo."""
    print("\n" * 1)
    print("=" * 65)
    print(f"   🏆  SIMULADOR DE TABLA DE POSICIONES - {nombre_liga.upper()}")
    print("=" * 65)
    print()


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_menu
# -----------------------------------------------------------------------------
def mostrar_menu(nombre_liga="Liga Oficial"):
    """Imprime en consola el menú principal con las opciones disponibles."""
    print()
    print("-" * 55)
    print(f"       MENÚ PRINCIPAL - {nombre_liga.upper()}")
    print("-" * 55)
    print("  1. Registrar equipos de la liga")
    print("  2. Asistente interactivo de partidos (Paso a paso)")
    print("  3. Carga masiva de partidos (Lote en texto)")
    print("  4. Ver tabla de posiciones")
    print("  5. Buscar estadísticas de un equipo")
    print("  6. Consultar historial de enfrentamientos")
    print("  7. Salir del simulador")
    print("-" * 55)


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_opcion_menu
# -----------------------------------------------------------------------------
def pedir_opcion_menu():
    """Captura la opción del menú elegida por el usuario."""
    opcion = input("  Ingrese su opción (1-7): ")
    return opcion.strip()


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_nombres_equipos
# -----------------------------------------------------------------------------
def pedir_nombres_equipos():
    """
    Solicita al usuario los nombres de los equipos.
    Diseño UX intuitivo y tolerante: para finalizar se puede ingresar
    'ok', 'listo', 'fin' o simplemente presionar Enter en blanco.
    """
    print()
    print("=" * 60)
    print("               REGISTRO DE EQUIPOS")
    print("=" * 60)
    print("  • Ingrese los nombres de los equipos (uno por línea).")
    print("  • Cuando termine, escriba 'ok' o presione [Enter] en blanco.")
    print("-" * 60)

    nombres_equipos = []
    comandos_fin = {"ok", "listo", "fin", "done"}

    while True:
        nombre = input("  Nombre del equipo: ").strip()

        # Condición flexible e intuitiva para finalizar
        if not nombre or nombre.lower() in comandos_fin:
            break

        # Evitar agregar duplicados en la misma tanda de entrada
        if nombre in nombres_equipos:
            print(f"  ⚠️ El equipo '{nombre}' ya fue ingresado en esta sesión.")
            continue

        nombres_equipos.append(nombre)
        print(f"  -> Equipo '{nombre}' añadido temporalmente.")

    return nombres_equipos


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_goles_equipo
# -----------------------------------------------------------------------------
def pedir_goles_equipo(nombre_equipo, rol="Local"):
    """
    Solicita de forma interactiva y guiada los goles de un equipo en particular.
    Valida que la entrada sea un número entero no negativo.
    Permite al usuario escribir 'salir', 'cancelar' o dejar en blanco para abortar de forma segura.
    Retorna un int con los goles, o None si el usuario decide salir.
    """
    while True:
        entrada = input(f"  > Ingrese goles para [{rol}] {nombre_equipo}: ").strip()

        # Opciones seguras para regresar al menú
        if entrada.lower() in {"salir", "cancelar", "menu", "volver"}:
            return None

        try:
            goles = int(entrada)
            if goles < 0:
                print("  ❌ Los goles no pueden ser un número negativo. Intente de nuevo.")
                continue
            return goles
        except ValueError:
            print(f"  ❌ Entrada inválida: '{entrada}'. Ingrese solo un número entero (ej. 0, 1, 2) o 'salir'.")


# -----------------------------------------------------------------------------
# FUNCIÓN: asistente_carga_partidos
# -----------------------------------------------------------------------------
def asistente_carga_partidos(torneo, registrar_partido_func):
    """
    Asistente interactivo guiado paso a paso para la carga de resultados.
    Elimina los formatos complejos de texto.
    Si hay jornadas generadas en el torneo, guía al usuario partido por partido de la jornada activa.
    Si no hay calendario, permite seleccionar local y visitante y registrar sus goles.
    """
    print()
    print("=" * 65)
    print("       ASISTENTE GUIADO: REGISTRO DE PARTIDOS (PASO A PASO)")
    print("=" * 65)
    print("  • Ingrese únicamente el número de goles de cada equipo.")
    print("  • Puede escribir 'salir' en cualquier momento para regresar al menú.")
    print("-" * 65)

    # Caso 1: Con calendario de jornadas
    if torneo.get("jornadas"):
        if torneo.get("liga_finalizada"):
            print("  ℹ️ La temporada ya ha finalizado. No hay partidos pendientes.")
            return

        idx_jornada = torneo.get("jornada_actual_idx", 0)
        jornadas = torneo["jornadas"]

        if idx_jornada >= len(jornadas):
            torneo["liga_finalizada"] = True
            print("  ℹ️ Todas las jornadas del calendario ya han sido disputadas.")
            return

        jornada = jornadas[idx_jornada]
        print(f"\n  📋 Disputando JORNADA {idx_jornada + 1} de {len(jornadas)}:")
        print("-" * 65)

        partidos_registrados = 0
        while torneo["partido_actual_idx"] < len(jornada):
            idx_partido = torneo["partido_actual_idx"]
            partido = jornada[idx_partido]

            if partido.get("jugado"):
                torneo["partido_actual_idx"] += 1
                continue

            print(f"\n  Encuentro {idx_partido + 1} de {len(jornada)}:")
            print(f"  ⚽ [Local] {partido['local']}  VS  [Visitante] {partido['visitante']}")

            # Pedir goles del local
            goles_local = pedir_goles_equipo(partido['local'], "Local")
            if goles_local is None:
                print("\n  [Operación pausada] Regresando al menú principal...")
                return

            # Pedir goles del visitante
            goles_visitante = pedir_goles_equipo(partido['visitante'], "Visitante")
            if goles_visitante is None:
                print("\n  [Operación pausada] Regresando al menú principal...")
                return

            # Registro oficial del partido
            partido["goles_local"] = goles_local
            partido["goles_visitante"] = goles_visitante
            partido["jugado"] = True

            registrar_partido_func(
                torneo,
                partido['local'],
                partido['visitante'],
                goles_local,
                goles_visitante
            )

            torneo["partido_actual_idx"] += 1
            partidos_registrados += 1
            print(f"\n  ✅ ¡Partido registrado con éxito! ({partido['local']} {goles_local} - {goles_visitante} {partido['visitante']})")

        # Si se completaron todos los partidos de la jornada
        if torneo["partido_actual_idx"] >= len(jornada):
            torneo["jornada_actual_idx"] += 1
            torneo["partido_actual_idx"] = 0
            if torneo["jornada_actual_idx"] >= len(jornadas):
                torneo["liga_finalizada"] = True
                print(f"\n  🎉 ¡Jornada {idx_jornada + 1} completada y TEMPORADA FINALIZADA!")
            else:
                print(f"\n  🎉 ¡Jornada {idx_jornada + 1} completada con éxito!")

    # Caso 2: Carga interactiva libre (cuando no hay calendario formal o se registra un amistoso/partido libre)
    else:
        equipos = list(torneo.get("equipos", {}).keys())
        if len(equipos) < 2:
            print("  ❌ Se necesitan al menos 2 equipos registrados para cargar partidos.")
            return

        while True:
            print("\n  Equipos disponibles:")
            for i, eq in enumerate(equipos, 1):
                print(f"    {i}. {eq}")
            print("  (Escriba 'salir' para volver al menú)")

            local_input = input("\n  Seleccione el equipo LOCAL (número o nombre): ").strip()
            if local_input.lower() in {"salir", "cancelar", "menu"}:
                break

            # Determinar equipo local
            if local_input.isdigit() and 1 <= int(local_input) <= len(equipos):
                eq_local = equipos[int(local_input) - 1]
            elif local_input in torneo["equipos"]:
                eq_local = local_input
            else:
                print(f"  ❌ Equipo '{local_input}' no reconocido.")
                continue

            visita_input = input("  Seleccione el equipo VISITANTE (número o nombre): ").strip()
            if visita_input.lower() in {"salir", "cancelar", "menu"}:
                break

            # Determinar equipo visitante
            if visita_input.isdigit() and 1 <= int(visita_input) <= len(equipos):
                eq_visita = equipos[int(visita_input) - 1]
            elif visita_input in torneo["equipos"]:
                eq_visita = visita_input
            else:
                print(f"  ❌ Equipo '{visita_input}' no reconocido.")
                continue

            if eq_local == eq_visita:
                print("  ❌ Un equipo no puede jugar contra sí mismo.")
                continue

            print(f"\n  ⚽ Encuentro: [Local] {eq_local} VS [Visitante] {eq_visita}")
            goles_local = pedir_goles_equipo(eq_local, "Local")
            if goles_local is None:
                break

            goles_visitante = pedir_goles_equipo(eq_visita, "Visitante")
            if goles_visitante is None:
                break

            registrar_partido_func(torneo, eq_local, eq_visita, goles_local, goles_visitante)
            print(f"\n  ✅ ¡Partido registrado con éxito! ({eq_local} {goles_local} - {goles_visitante} {eq_visita})")

            mas = input("\n  ¿Desea registrar otro partido? (Enter para Sí / 'no' para volver al menú): ").strip()
            if mas.lower() in {"no", "n", "salir"}:
                break


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_partidos_lote (Mantenida como alternativa opcional / compatibilidad)
# -----------------------------------------------------------------------------
def pedir_partidos_lote():
    """
    Solicita al usuario ingresar líneas de partidos en lote si desea usar carga masiva de texto.
    Termina al presionar Enter en blanco o escribir 'ok'/'listo'.
    """
    print()
    print("=" * 65)
    print("            CARGA DE PARTIDOS POR LOTE (TEXTO)")
    print("=" * 65)
    print("  Formato requerido por línea:")
    print("  EquipoLocal - GolesLocal | EquipoVisitante - GolesVisitante")
    print("  Para finalizar, presione [Enter] en blanco o escriba 'ok'.")
    print("-" * 65)

    lista_partidos = []
    comandos_fin = {"ok", "listo", "fin"}

    while True:
        linea = input("  Partido: ").strip()
        if not linea or linea.lower() in comandos_fin:
            break
        lista_partidos.append(linea)

    return lista_partidos


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_tabla_posiciones
# -----------------------------------------------------------------------------
def mostrar_tabla_posiciones(tabla_ordenada, nombre_liga="Liga Oficial"):
    """Muestra la tabla de posiciones clasificada y formateada."""
    print()
    print("=" * 76)
    print(f"                 TABLA DE POSICIONES - {nombre_liga.upper()}")
    print("=" * 76)
    print(f"{'#':<4} {'EQUIPO':<22} {'PJ':>4} {'PG':>4} {'PE':>4} {'PP':>4} {'GF':>4} {'GC':>4} {'DIF':>5} {'PTS':>5}")
    print("-" * 76)

    if not tabla_ordenada:
        print("  (No hay equipos registrados en la liga todavía)")
        print("=" * 76)
        return

    for posicion, (nombre, estadisticas) in enumerate(tabla_ordenada, start=1):
        print(
            f"{posicion:<4}"
            f"{nombre:<22}"
            f"{estadisticas['PJ']:>5}"
            f"{estadisticas['PG']:>5}"
            f"{estadisticas['PE']:>5}"
            f"{estadisticas['PP']:>5}"
            f"{estadisticas['GF']:>5}"
            f"{estadisticas['GC']:>5}"
            f"{estadisticas['DIF']:>6}"
            f"{estadisticas['PTS']:>6}"
        )

    print("=" * 76)
    print()


# -----------------------------------------------------------------------------
# FUNCIÓN: pedir_nombre_equipo_buscar
# -----------------------------------------------------------------------------
def pedir_nombre_equipo_buscar():
    """Solicita el nombre del equipo a buscar."""
    print()
    nombre = input("  Ingrese el nombre del equipo a buscar: ")
    return nombre.strip()


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_estadisticas_equipo
# -----------------------------------------------------------------------------
def mostrar_estadisticas_equipo(nombre_equipo, estadisticas):
    """Muestra el desglose detallado de estadísticas de un equipo específico."""
    print()
    print("=" * 45)
    print(f"   ESTADÍSTICAS: {nombre_equipo.upper()}")
    print("=" * 45)
    print(f"  {'Partidos Jugados (PJ):':<25} {estadisticas['PJ']}")
    print(f"  {'Partidos Ganados (PG):':<25} {estadisticas['PG']}")
    print(f"  {'Partidos Empatados (PE):':<25} {estadisticas['PE']}")
    print(f"  {'Partidos Perdidos (PP):':<25} {estadisticas['PP']}")
    print(f"  {'Goles a Favor (GF):':<25} {estadisticas['GF']}")
    print(f"  {'Goles en Contra (GC):':<25} {estadisticas['GC']}")
    print(f"  {'Diferencia de Goles (DIF):':<25} {estadisticas['DIF']}")
    print(f"  {'Puntos Acumulados (PTS):':<25} {estadisticas['PTS']}")
    print("=" * 45)
    print()


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_historial_equipo
# -----------------------------------------------------------------------------
def mostrar_historial_equipo(nombre_equipo, historial_partidos):
    """Muestra la lista de enfrentamientos registrados de un equipo."""
    print()
    print("=" * 60)
    print(f"   HISTORIAL DE PARTIDOS: {nombre_equipo.upper()}")
    print("=" * 60)

    if not historial_partidos:
        print("  (El equipo no registra partidos disputados aún)")
    else:
        for p in historial_partidos:
            marcador = f"{p['local']} {p['goles_local']} - {p['goles_visitante']} {p['visitante']}"
            print(f"  • {marcador}")

    print("=" * 60)
    print()


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_errores_lote
# -----------------------------------------------------------------------------
def mostrar_errores_lote(lista_errores):
    """Muestra los errores o la confirmación de éxito en el procesamiento por lotes."""
    if len(lista_errores) == 0:
        print("  ✅ Todos los partidos fueron procesados correctamente.")
    else:
        print(f"  ⚠️  Se encontraron {len(lista_errores)} error(es) durante el procesamiento:")
        print()
        for error in lista_errores:
            print(f"    - {error}")


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_mensaje
# -----------------------------------------------------------------------------
def mostrar_mensaje(mensaje):
    """Muestra un mensaje informativo formateado."""
    print(f"  {mensaje}")


# -----------------------------------------------------------------------------
# FUNCIÓN: mostrar_error
# -----------------------------------------------------------------------------
def mostrar_error(mensaje_error):
    """Muestra un mensaje de error formateado."""
    print(f"  ❌ ERROR: {mensaje_error}")
