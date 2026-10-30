# =============================================================================
# ARCHIVO: main.py
# DESCRIPCIÓN: Punto de entrada principal del Simulador de Liga Deportiva.
#              Orquesta el flujo general del programa conectando la interfaz
#              con la lógica de negocio y gestionando la navegación por menús.
# FUNDAMENTO: Sección 1.2 - Modularización: separación de responsabilidades.
#             "Ningún ejercicio puede estar escrito en un solo archivo main.py.
#              Deben existir paquetes, módulos y una clara separación de
#              responsabilidades (lógica de negocio vs. interfaz de usuario)."
# =============================================================================

# ---- IMPORTACIONES DE EXCEPCIONES -------------------------------------------
from excepciones import EquipoNoRegistradoError

# ---- IMPORTACIONES DEL PAQUETE 'liga' (Lógica de Negocio) -------------------
from liga.torneo import (
    crear_torneo,
    registrar_equipo_torneo,
    generar_calendario,
    registrar_partido_jugado,
    consultar_historial_equipo
)
from liga.tabla import ordenar_tabla, buscar_equipo
from liga.partidos import procesar_lote

# ---- IMPORTACIONES DEL PAQUETE 'interfaz' (Entrada/Salida de Consola) -------
from interfaz.consola import (
    limpiar_pantalla,
    pausar_continuar,
    pedir_nombre_liga,
    mostrar_bienvenida,
    mostrar_menu,
    pedir_opcion_menu,
    pedir_nombres_equipos,
    asistente_carga_partidos,
    pedir_goles_equipo,
    pedir_partidos_lote,
    mostrar_tabla_posiciones,
    pedir_nombre_equipo_buscar,
    mostrar_estadisticas_equipo,
    mostrar_historial_equipo,
    mostrar_errores_lote,
    mostrar_mensaje,
    mostrar_error
)


def ejecutar_simulacion_jornadas(torneo):
    """
    Sub-flujo interactivo para disputar la liga jornada por jornada.
    Permite cargar marcadores de cada encuentro o pausar para volver al menú.
    """
    if not torneo["jornadas"]:
        mostrar_error("Primero debes registrar al menos 2 equipos (Opción 1) para generar el calendario.")
        pausar_continuar()
        return

    if torneo["liga_finalizada"]:
        mostrar_mensaje("¡La temporada ya ha finalizado! No hay más partidos pendientes.")
        mostrar_tabla_posiciones(ordenar_tabla(torneo["equipos"]), torneo["nombre"])
        pausar_continuar()
        return

    while torneo["jornada_actual_idx"] < len(torneo["jornadas"]):
        idx_jornada = torneo["jornada_actual_idx"]
        jornada = torneo["jornadas"][idx_jornada]

        limpiar_pantalla()
        print("=" * 60)
        print(f"        JORNADA {idx_jornada + 1} DE {len(torneo['jornadas'])} - {torneo['nombre'].upper()}")
        print("=" * 60)

        salir_al_menu = False

        while torneo["partido_actual_idx"] < len(jornada):
            idx_partido = torneo["partido_actual_idx"]
            partido = jornada[idx_partido]

            if partido["jugado"]:
                torneo["partido_actual_idx"] += 1
                continue

            print()
            print(f"  Encuentro {idx_partido + 1} de {len(jornada)}:")
            print(f"  ⚽  {partido['local']}  VS  {partido['visitante']}")
            entrada = input("  Ingrese marcador (ej. 2-1) o 'salir' para pausar: ").strip()

            if entrada.lower() in {"salir", "menu", "volver"}:
                mostrar_mensaje("Progreso retenido. Regresando al menú principal...")
                salir_al_menu = True
                break

            try:
                if "-" not in entrada:
                    raise ValueError("Debe ingresar el marcador separado con guion (ejemplo: 2-1).")

                partes = entrada.split("-", maxsplit=1)
                g_local = int(partes[0].strip())
                g_visitante = int(partes[1].strip())

                if g_local < 0 or g_visitante < 0:
                    raise ValueError("Los goles no pueden ser números negativos.")

                partido["goles_local"] = g_local
                partido["goles_visitante"] = g_visitante
                partido["jugado"] = True

                registrar_partido_jugado(
                    torneo,
                    partido["local"],
                    partido["visitante"],
                    g_local,
                    g_visitante
                )

                torneo["partido_actual_idx"] += 1
                mostrar_mensaje(f"  -> Resultado registrado: {partido['local']} {g_local} - {g_visitante} {partido['visitante']}")

            except ValueError as error:
                mostrar_error(f"Entrada inválida: {error}")

        if salir_al_menu:
            pausar_continuar()
            break

        # Al completar la jornada actual
        limpiar_pantalla()
        print("=" * 60)
        print(f"   🎉 ¡FIN DE LA JORNADA {idx_jornada + 1}! CLASIFICACIÓN AL MOMENTO:")
        print("=" * 60)
        mostrar_tabla_posiciones(ordenar_tabla(torneo["equipos"]), torneo["nombre"])

        torneo["jornada_actual_idx"] += 1
        torneo["partido_actual_idx"] = 0

        if torneo["jornada_actual_idx"] < len(torneo["jornadas"]):
            opc_avance = input("  Presione [Enter] para continuar la siguiente jornada (o escriba 'menu' para salir): ").strip()
            if opc_avance.lower() in {"menu", "salir", "volver"}:
                break
        else:
            torneo["liga_finalizada"] = True
            mostrar_mensaje("🏆 ¡Felicidades! La temporada completa ha finalizado con éxito.")
            pausar_continuar()
            break


def ejecutar_simulador():
    """Función principal que orquesta el simulador de liga deportiva."""

    limpiar_pantalla()

    # Paso inicial: Configuración de la Liga
    nombre_liga = pedir_nombre_liga()
    torneo = crear_torneo(nombre_liga)

    limpiar_pantalla()
    mostrar_bienvenida(torneo["nombre"])
    mostrar_mensaje(f"Liga '{torneo['nombre']}' inicializada correctamente.")
    pausar_continuar()

    # Bucle principal de navegación
    while True:
        limpiar_pantalla()
        mostrar_menu(torneo["nombre"])
        opcion = pedir_opcion_menu()

        # ---- OPCIÓN 1: Registrar equipos de la liga -------------------------
        if opcion == "1":
            limpiar_pantalla()
            nombres = pedir_nombres_equipos()

            equipos_nuevos = 0
            for nombre in nombres:
                try:
                    registrar_equipo_torneo(torneo, nombre)
                    equipos_nuevos += 1
                except ValueError as e:
                    mostrar_error(f"{e}")

            if equipos_nuevos > 0:
                mostrar_mensaje(f"Se registraron {equipos_nuevos} equipo(s) con éxito.")

            # Si hay 2 o más equipos, se genera o actualiza el calendario
            total_equipos = len(torneo["equipos"])
            if total_equipos >= 2:
                try:
                    generar_calendario(torneo)
                    mostrar_mensaje(
                        f"Calendario oficial generado: {len(torneo['jornadas'])} jornadas para {total_equipos} equipos."
                    )
                except ValueError as err:
                    mostrar_error(f"{err}")
            else:
                mostrar_mensaje("Aviso: Se requieren al menos 2 equipos para habilitar el calendario de jornadas.")

            pausar_continuar()

        # ---- OPCIÓN 2: Asistente interactivo guiado de partidos ------------
        elif opcion == "2":
            limpiar_pantalla()
            if not torneo["equipos"]:
                mostrar_error("No hay equipos registrados en la liga. Ingrese primero la opción 1.")
                pausar_continuar()
                continue

            asistente_carga_partidos(torneo, registrar_partido_jugado)
            pausar_continuar()

        # ---- OPCIÓN 3: Carga masiva de partidos (Lote en texto) ------------
        elif opcion == "3":
            limpiar_pantalla()
            if not torneo["equipos"]:
                mostrar_error("No hay equipos registrados en la liga. Ingrese primero la opción 1.")
                pausar_continuar()
                continue

            lista_partidos = pedir_partidos_lote()

            if not lista_partidos:
                mostrar_mensaje("No se ingresó ningún partido en el lote.")
                pausar_continuar()
                continue

            errores = procesar_lote(torneo, lista_partidos)
            mostrar_errores_lote(errores)
            pausar_continuar()

        # ---- OPCIÓN 4: Ver tabla de posiciones ------------------------------
        elif opcion == "4":
            limpiar_pantalla()
            tabla_ordenada = ordenar_tabla(torneo["equipos"])
            mostrar_tabla_posiciones(tabla_ordenada, torneo["nombre"])
            pausar_continuar()

        # ---- OPCIÓN 5: Buscar estadísticas de un equipo ---------------------
        elif opcion == "5":
            limpiar_pantalla()
            nombre_buscado = pedir_nombre_equipo_buscar()
            estadisticas = buscar_equipo(torneo["equipos"], nombre_buscado)

            if estadisticas is None:
                mostrar_error(f"El equipo '{nombre_buscado}' no está registrado en la liga.")
            else:
                mostrar_estadisticas_equipo(nombre_buscado, estadisticas)

            pausar_continuar()

        # ---- OPCIÓN 6: Consultar historial de enfrentamientos --------------
        elif opcion == "6":
            limpiar_pantalla()
            nombre_buscado = pedir_nombre_equipo_buscar()
            try:
                historial = consultar_historial_equipo(torneo, nombre_buscado)
                mostrar_historial_equipo(nombre_buscado, historial)
            except EquipoNoRegistradoError as e:
                mostrar_error(f"{e}")

            pausar_continuar()

        # ---- OPCIÓN 7: Salir del simulador ----------------------------------
        elif opcion == "7":
            limpiar_pantalla()
            mostrar_mensaje(f"¡Hasta luego! Gracias por usar el Simulador de {torneo['nombre']}.")
            break

        # ---- OPCIÓN INVÁLIDA ------------------------------------------------
        else:
            mostrar_error(f"Opción '{opcion}' no válida. Ingrese un número del 1 al 7.")
            pausar_continuar()


if __name__ == "__main__":
    ejecutar_simulador()
