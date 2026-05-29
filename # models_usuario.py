# models_usuario.py
# la clase usuario sirve para la autenticación

class Usuario:
    """
    Clase que representa un usuario del sistema.
    ENCAPSULAMIENTO: Atributos privados con getters.
    """
    
    def __init__(self, nombre: str, rol: str):
        """
        Constructor de Usuario.
        
        Args:
            nombre: Nombre del usuario
            rol: Rol ('admin' o 'empleado')
        """
        self._nombre = nombre
        self._rol = rol
    
    def get_nombre(self) -> str:
        """Retorna el nombre del usuario"""
        return self._nombre
    
    def get_rol(self) -> str:
        """Retorna el rol del usuario"""
        return self._rol
    
    def es_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self._rol == "admin"
    
    def es_empleado(self) -> bool:
        """Verifica si el usuario es empleado"""
        return self._rol == "empleado"
    
    def __str__(self) -> str:
        return f"Usuario: {self._nombre} ({self._rol})"