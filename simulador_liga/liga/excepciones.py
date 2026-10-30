
# MÓDULO: excepciones.py (DEPRECADO - REDIRIGIDO A PAQUETE 'excepciones')
# PAQUETE: liga
# DESCRIPCIÓN: Reexporta EquipoNoRegistradoError desde el nuevo paquete modular
#              'excepciones' para mantener compatibilidad hacia atrás.


from excepciones.errores import EquipoNoRegistradoError

__all__ = ["EquipoNoRegistradoError"]
