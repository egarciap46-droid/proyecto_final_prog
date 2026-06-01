# models/prenda.py
# CLASES POO - 4 PILARES DE LA PROGRAMACIÓN ORIENTADA A OBJETOS
# Autor: Emerson
# Fecha: Mayo 2026

"""
Implementación de las clases base para el sistema de pedidos.
Demuestra los 4 pilares de POO:
1. ABSTRACCIÓN: Clase Prenda define la interfaz
2. ENCAPSULAMIENTO: Atributos privados con getters/setters
3. HERENCIA: PrendaMayorista tiene herencia de prenda
4. POLIMORFISMO: Método calcular_total() se comporta diferente
"""

from typing import Optional


class Prenda:
    """
    Clase base abstracta que representa una prenda de ropa.
    ABSTRACCIÓN: Define la estructura mínima que toda prenda debe tener.
    ENCAPSULAMIENTO: Los atributos son privados (convención _ en Python).
    """
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):
        """
        Constructor de la clase Prenda.
        
        Args:
            marca: Marca de la prenda (ej: pepe, zara)
            cantidad: Número de unidades
            precio: Precio por unidad
            tipo: Tipo de prenda (camisa, pantalón, etc.)
        """
        # Atributos privados (ENCAPSULAMIENTO)
        self._marca = marca
        self._cantidad = cantidad
        self._precio = precio
        self._tipo = tipo
    
    # ============ GETTERS (acceso controlado) ============
    def get_marca(self) -> str:
        """Retorna la marca de la prenda"""
        return self._marca
    
    def get_cantidad(self) -> int:
        """Retorna la cantidad de unidades"""
        return self._cantidad
    
    def get_precio(self) -> float:
        """Retorna el precio unitario"""
        return self._precio
    
    def get_tipo(self) -> str:
        """Retorna el tipo de prenda"""
        return self._tipo
    
    # ============ SETTERS (validación de datos) ============
    def set_marca(self, marca: str):
        """Actualiza la marca con validación"""
        if marca and marca.strip():
            self._marca = marca.strip()
    
    def set_cantidad(self, cantidad: int):
        """Actualiza la cantidad (solo si es positiva)"""
        if cantidad > 0:
            self._cantidad = cantidad
    
    def set_precio(self, precio: float):
        """Actualiza el precio del producto (solo si es positivo)"""
        if precio > 0:
            self._precio = precio
    
    def set_tipo(self, tipo: str):
        """Actualiza el tipo con validación"""
        if tipo and tipo.strip():
            self._tipo = tipo.strip()
    
    # ============ MÉTODOS DE NEGOCIO ============
    def calcular_total(self) -> float:
        """
        Calcula el total sin descuentos.
        POLIMORFISMO: Este método es ederado por las clases hijas.
        
        Returns:
            float: Precio total (cantidad * precio unitario)
        """
        return self._cantidad * self._precio
    
    def __str__(self) -> str:
        """
        Representación en string de la prenda.
        Sobrescribe el método str() de Python.
        """
        return f"{self._tipo} {self._marca} | {self._cantidad} uds | ${self._precio:.2f}/ud"
    
    def __repr__(self) -> str:
        """Representación para depuración"""
        return f"Prenda(marca='{self._marca}', cantidad={self._cantidad}, precio={self._precio}, tipo='{self._tipo}')"


class PrendaMayorista(Prenda):
    """
    Clase que hereda de Prenda para compras al por mayor.
    HERENCIA: Extiende la funcionalidad de Prenda.
    POLIMORFISMO: Sobrescribe calcular_total() para aplicar descuentos.
    
    """
    
    # Descuentos por volumen de compra
    DESCUENTOS = {
        50: 0.05,   # 5% de descuento para 50+ unidades
        100: 0.10,  # 10% para 100+ unidades
        500: 0.15,  # 15% para 500+ unidades
        1000: 0.20  # 20% para 1000+ unidades
    }
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):
        """
        Constructor de PrendaMayorista.
        Llama al constructor de la clase padre.
        """
        super().__init__(marca, cantidad, precio, tipo)
        self._calcular_descuento_aplicable()
    
    def _calcular_descuento_aplicable(self) -> float:
        """
        Calcula el descuento según la cantidad comprada.
        
        Returns:
            float: Porcentaje de descuento (0.0 a 0.20)
        """
        for umbral, descuento in sorted(self.DESCUENTOS.items(), reverse=True):
            if self._cantidad >= umbral:
                self._descuento = descuento
                return descuento
        self._descuento = 0.0
        return 0.0
    
    def get_descuento(self) -> float:
        """Retorna el porcentaje de descuento aplicado"""
        return self._descuento
    
    def calcular_total(self) -> float:
        """
        Calcula el total aplicando descuento por volumen.
        POLIMORFISMO: Sobrescribe el método de la clase padre.
        
        Returns:
            float: Total con descuento aplicado
        """
        total_bruto = super().calcular_total()
        self._calcular_descuento_aplicable()
        total_con_descuento = total_bruto * (1 - self._descuento)
        return round(total_con_descuento, 2)
    
    def __str__(self) -> str:
        """Representación en string incluyendo descuento"""
        base_str = super().__str__()
        if self._descuento > 0:
            return f"{base_str} (desc: {self._descuento*100:.0f}%)"
        return base_str


# Clase adicional para demostrar más herencia (opcional)
class PrendaOferta(Prenda):
    """
    Clase para prendas en oferta especial.
    Demuestra extensibilidad del sistema (OCP).
    """
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str, oferta: float = 0.30):
        super().__init__(marca, cantidad, precio, tipo)
        self._oferta = oferta  # 30% de descuento por defecto
    
    def calcular_total(self) -> float:
        """Aplica descuento por oferta especial"""
        total = super().calcular_total()
        return total * (1 - self._oferta)
    
    def __str__(self) -> str:
 main
        return f"{super().__str__()} ( OFERTA {self._oferta*100:.0f}%)"

        return f"{super().__str__()} ( OFERTA {self._oferta*100:.0f}%)"
 main
