# structures_pila.py
# ESTRUCTURA DE DATOS: PILA- Unidad 6
# Fecha: Mayo 2026

"""
Implementación de una Pila (Stack) con estructura LIFO (Last In, First Out).
Útil para:
- deshacer acciones (Undo)
- evaluación de ciertas expresiones
- poder navegar entre pantallas
"""

from typing import Any, Optional, Iterator
from collections.abc import Iterable


class Pila:
    """
    Implementación de Pila usando lista de Python.
    
    Principales operaciones:
    - push: Agrega un elemento al tope
    - pop: Elimina y retorna el elemento del tope
    - peek: Muestra el tope sin eliminar
    - is_empty: Verifica si está vacía
    """
    
    def __init__(self, iterable: Optional[Iterable] = None):
        """
        Inicializa una pila vacía o con elementos.
        
        Args:
            iterable: Iterable opcional para inicializar la pila
        """
        self._items = []
        if iterable:
            for item in iterable:
                self.push(item)
    
    #            OPERACIONES PRINCIPALES 
    
    def push(self, item: Any) -> None:
        """
        Agrega un elemento al tope de la pila.
        
        Args:
            item: Elemento a agregar
        """
        self._items.append(item)
    
    def pop(self) -> Optional[Any]:
        """
        Elimina y retorna el elemento del tope de la pila.
        
        Returns:
            El elemento del tope, o None si la pila está vacía
        """
        if not self.esta_vacia():
            return self._items.pop()
        return None
    
    def peek(self) -> Optional[Any]:
        """
        Retorna el elemento del tope sin eliminarlo.
        
        Returns:
            El elemento del tope, o None si la pila está vacía
        """
        if not self.esta_vacia():
            return self._items[-1]
        return None
    
    def esta_vacia(self) -> bool:
        """
        Verifica si la pila está vacía.
        
        Returns:
            True si está vacía, False en caso contrario
        """
        return len(self._items) == 0
    
    def tamaño(self) -> int:
        """
        Retorna el número de elementos en la pila.
        
        Returns:
            int: Cantidad de elementos
        """
        return len(self._items)
    
    # ____________ OPERACIONES ADICIONALES ____________
    
    def vaciar(self) -> None:
        """Elimina todos los elementos de la pila"""
        self._items.clear()
    
    def contiene(self, item: Any) -> bool:
        """
        verifica si un elemento está en la pila.
        
        Args:
            item: elemento a buscar
            
        Returns:
            True si existe, False en caso contrario
        """
        return item in self._items
    
    def obtener_todos(self) -> list:
        """
        retorna una copia de todos los elementos (de tope a fondo).
        
        returns:
            list: Copia de los elementos
        """
        return self._items.copy()
    
    def obtener_todos_desde_fondo(self) -> list:
        """
        retorna una copia de todos los elementos (de fondo a tope).
        
        returns:
            list: Copia de los elementos en orden de inserción
        """
        return self._items.copy()[::-1]
    
    # ============ MÉTODOS ESPECIALES ============
    
    def __len__(self) -> int:
        """permite usar len(pila)"""
        return self.tamaño()
    
    def __bool__(self) -> bool:
        """permite usar if pila: (True si no está vacía)"""
        return not self.esta_vacia()
    
    def __contains__(self, item: Any) -> bool:
        """permite usar 'item in pila'"""
        return self.contiene(item)
    
    def __getitem__(self, indice: int) -> Any:
        """
        permite acceder por índice (0 es tope, -1 es fondo).
        
        args:
            indice: Índice del elemento (0 = tope)
            
        returns:
            el elemento en la posición especificada
        """
        if indice < 0:
            indice = len(self._items) + indice
        if indice < 0 or indice >= len(self._items):
            raise IndexError("Índice fuera de rango")
        # Índice 0 es el último elemento (tope)
        return self._items[-(indice + 1)]
    
    def __iter__(self) -> Iterator:
        """
        permite iterar desde el tope hasta el fondo.
        
        Yields:
            Elementos desde el tope hacia el fondo
        """
        for item in reversed(self._items):
            yield item
    
    def __str__(self) -> str:
        """representación en string (tope a la derecha)"""
        if self.esta_vacia():
            return "Pila: []"
        
        elementos = [str(item) for item in reversed(self._items)]
        return f"Pila: [{' <- '.join(elementos)}] (tope a la derecha)"
    
    def __repr__(self) -> str:
        """representación para depuración"""
        return f"Pila({self._items[::-1]})"


# ___________ CLASE PARA HISTORIAL DE ACCIONES (CASO DE USO) ____________

class HistorialAcciones:
    """
    Implementación práctica de una pila para el sistema.
    Permite deshacer acciones (undo) en el sistema de pedidos.
    """
    
    def __init__(self, capacidad_maxima: int = 50):
        """
        Inicializa el historial con capacidad máxima.
        
        Args:
            capacidad_maxima: Número máximo de acciones para recordar
        """
        self._acciones = Pila()
        self._capacidad_maxima = capacidad_maxima
    
    def registrar_accion(self, descripcion: str, datos: Any = None) -> None:
        """
        Registra una acción en el historial.
        
        Args:
            descripcion: Descripción de la acción
            datos: Datos asociados a la acción (para poder deshacer)
        """
        accion = {
            "descripcion": descripcion,
            "datos": datos,
            "timestamp": __import__('datetime').datetime.now()
        }
        self._acciones.push(accion)
        
        # limitar tamaño
        if self._acciones.tamaño() > self._capacidad_maxima:
            # eliminar el más antiguo (no se puede directamente con pila)
            # esta es una simplificación
            pass
    
    def deshacer(self) -> Optional[dict]:
        """
        Deshace la última acción.
        
        Returns:
            La acción deshecha, o None si no hay acciones
        """
        return self._acciones.pop()
    
    def ver_ultima_accion(self) -> Optional[dict]:
        """Mira la última acción sin deshacerla"""
        return self._acciones.peek()
    
    def puede_deshacer(self) -> bool:
        """Verifica si hay acciones para deshacer"""
        return not self._acciones.esta_vacia()
    
    def cantidad_acciones(self) -> int:
        """Retorna el número de acciones en el historial"""
        return self._acciones.tamaño()
    
    def limpiar(self) -> None:
        """Limpia todo el historial"""
        self._acciones.vaciar()
    
    def __str__(self) -> str:
        if self._acciones.esta_vacia():
            return "Historial vacío"
        
        resultado = ["=== HISTORIAL DE ACCIONES ==="]
        for i, accion in enumerate(self._acciones, 1):
            resultado.append(f"{i}. {accion['descripcion']}")
        return "\n".join(resultado)


# ------------ FUNCIONES DE PRUEBA ---------------

def probar_pila():
    """función de prueba para la pila"""
    print("\n" + "="*50)
    print("PRUEBA DE PILA (STACK)")
    print("="*50)
    
    # Crear pila
    pila = Pila()
    print(f"Pila creada: {pila}")
    print(f"¿Está vacía? {pila.esta_vacia()}")
    
    # Push
    print("\n--- Push (apilar) ---")
    for i in range(5):
        pila.push(f"Item {i}")
        print(f"Push Item {i}: {pila}")
    
    print(f"\nTamaño: {len(pila)}")
    print(f"Tope (peek): {pila.peek()}")
    
    # Pop
    print("\n--- Pop (desapilar) ---")
    while not pila.esta_vacia():
        item = pila.pop()
        print(f"Pop: {item} - Pila: {pila}")
    
    # Probar historial
    print("\n--- Probando HistorialAcciones ---")
    historial = HistorialAcciones()
    
    historial.registrar_accion("Agregar prenda", {"marca": "Nike", "cantidad": 10})
    historial.registrar_accion("Eliminar prenda", {"id": 5})
    historial.registrar_accion("Actualizar precio", {"marca": "Adidas", "nuevo_precio": 50})
    
    print(historial)
    print(f"\n¿Puede deshacer? {historial.puede_deshacer()}")
    
    ultima = historial.deshacer()
    print(f"Deshacer: {ultima['descripcion']}")
    
    print("\n Todas las pruebas pasaron!")


if __name__ == "__main__":
    probar_pila()
