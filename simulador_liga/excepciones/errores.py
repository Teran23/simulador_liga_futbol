
# DESCRIPCIÓN: Define las clases de excepción personalizadas para el simulador de liga.
# FUNDAMENTO: Manejo de Errores:
#             La sentencia 'raise' permite lanzar nuestras propias excepciones.
#             Una clase que hereda de 'Exception' se convierte en excepción personalizada.



class EquipoNoRegistradoError(Exception):

    """Excepción lanzada cuando se intenta consultar o procesar un equipo que no existe."""

    def __init__(self, nombre_equipo):
        self.nombre_equipo = nombre_equipo
        self.mensaje = f"Error: El equipo '{nombre_equipo}' no está registrado en la liga."
        super().__init__(self.mensaje)


class FormatoPartidoInvalidoError(ValueError):

    """Excepción lanzada cuando una línea de resultado de partido no respeta el formato esperado."""

    def __init__(self, linea_invalida, detalle="Formato no reconocido"):
        self.linea_invalida = linea_invalida
        self.mensaje = f"Error de formato en '{linea_invalida}': {detalle}"
        super().__init__(self.mensaje)

