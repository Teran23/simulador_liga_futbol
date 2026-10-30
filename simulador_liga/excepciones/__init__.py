# =============================================================================
# ARCHIVO: __init__.py
# PAQUETE: excepciones
# DESCRIPCIÓN: Inicializador del paquete 'excepciones'.
#              Exporta las clases de error para permitir importaciones directas.
# FUNDAMENTO: Sección 1.2 - Modularización: Paquetes y archivos __init__.py.
# =============================================================================

from excepciones.errores import EquipoNoRegistradoError, FormatoPartidoInvalidoError

__all__ = ["EquipoNoRegistradoError", "FormatoPartidoInvalidoError"]

