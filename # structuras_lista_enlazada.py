# structuras_lista_enlazada.py
# ESTRUCTURA DE DATOS: LISTA ENLAZADA (Unidad 5)
# Autor: [Tu Nombre]
# Fecha: Mayo 2026

"""
Implementación de una lista enlazada simple.
Requisitos:
- Clases auto-referenciadas (Nodo)
- Manejo de memoria dinámica (Python lo maneja automáticamente)
- Operaciones básicas: agregar, eliminar, buscar
"""

from typing import Any, Optional, Iterator
from utils.utilidades import Utilidades


class Nodo:
    """
    Clase auto-referenciada para los nodos de la lista enlazada.
    Cada nodo contiene un dato y una referencia al siguiente nodo.
    """
    
    def __init__(self, dato: Any):
        """
        Constructor del nodo.
        
        Args:
            dato: El dato que almacenará el nodo
        """
        self.dato = dato      # Dato almacenado
        self.siguiente = None # Referencia al siguiente nodo (None si es el último)
    
    def __str__(self) -> str:
        """Representación del nodo"""
        return f"Nodo({self.dato})"


class ListaEnlazada:
    """
    Implementación de lista enlazada simple.
    
    Características:
    - Inserción al final O(n)
    - Eliminación por índice O(n)
    - Búsqueda O(n)
    
    Estructura:
        [Nodo1] -> [Nodo2] -> [Nodo3] -> None
    """
    
    def __init__(self):
        """Inicializa una lista enlazada vacía"""
        self._cabeza: Optional[Nodo] = None  # Primer nodo de la lista
        self._tamaño: int = 0                # Número de elementos
    
    # ============ OPERACIONES BÁSICAS ============
    
    def agregar(self, dato: Any) -> None:
        """
        Agrega un elemento al final de la lista.
        
        Args:
            dato: El dato a agregar
        """
        nuevo_nodo = Nodo(dato)
        
        if self._cabeza is None:
            # Lista vacía: el nuevo nodo es la cabeza
            self._cabeza = nuevo_nodo
        else:
            # Recorrer hasta el último nodo
            actual = self._cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self._tamaño += 1
    
    def agregar_al_inicio(self, dato: Any) -> None:
        """
        Agrega un elemento al inicio de la lista.
        
        Args:
            dato: El dato a agregar
        """
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self._cabeza
        self._cabeza = nuevo_nodo
        self._tamaño += 1
    
    def eliminar(self, indice: int) -> bool:
        """
        Elimina el elemento en la posición que se explica.
        
        Args:
            indice: Índice del elemento a eliminar (0-based)
            
        Returns:
            bool: True si se eliminó, False si el índice es inválido
        """
        if indice < 0 or indice >= self._tamaño:
            return False
        
        if indice == 0:
            # Eliminar la cabeza
            self._cabeza = self._cabeza.siguiente
        else:
            # Buscar el nodo anterior al que queremos eliminar
            actual = self._cabeza
            for _ in range(indice - 1):
                actual = actual.siguiente
            # Saltar el nodo a eliminar
            actual.siguiente = actual.siguiente.siguiente
        
        self._tamaño -= 1
        return True
    
    def eliminar_por_valor(self, valor: Any) -> bool:
        """
        Elimina la primera ocurrencia de un valor.
        
        Args:
            valor: El valor a eliminar
            
        Returns:
            bool: True si se encontró y eliminó, False si no existe
        """
        if self._cabeza is None:
            return False
        
        # Si el valor está en la cabeza
        if self._cabeza.dato == valor:
            self._cabeza = self._cabeza.siguiente
            self._tamaño -= 1
            return True
        
        # Buscar en el resto de la lista
        actual = self._cabeza
        while actual.siguiente:
            if actual.siguiente.dato == valor:
                actual.siguiente = actual.siguiente.siguiente
                self._tamaño -= 1
                return True
            actual = actual.siguiente
        
        return False
    
    def obtener(self, indice: int) -> Optional[Any]:
        """
        Obtiene el elemento en la posición especificada.
        
        Args:
            indice: Índice del elemento (0-based)
            
        Returns:
            El dato en esa posición, o None si el índice es inválido
        """
        if indice < 0 or indice >= self._tamaño:
            return None
        
        actual = self._cabeza
        for _ in range(indice):
            actual = actual.siguiente
        
        return actual.dato
    
    def buscar(self, valor: Any) -> int:
        """
        Busca la primera ocurrencia de un valor.
        
        Args:
            valor: Valor a buscar
            
        Returns:
            int: Índice del valor, o -1 si no existe
        """
        actual = self._cabeza
        indice = 0
        
        while actual:
            if actual.dato == valor:
                return indice
            actual = actual.siguiente
            indice += 1
        
        return -1
    
    # ============ MÉTODOS DE UTILIDAD ============
    
    def obtener_todos(self) -> list:
        """
        Convierte la lista enlazada a una lista de Python.
        
        Returns:
            list: Lista con todos los elementos
        """
        resultado = []
        actual = self._cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado
    
    def tamaño(self) -> int:
        """Retorna el número de elementos en la lista"""
        return self._tamaño
    
    def esta_vacia(self) -> bool:
        """Verifica si la lista está vacía"""
        return self._tamaño == 0
    
    def limpiar(self) -> None:
        """Elimina todos los elementos de la lista"""
        self._cabeza = None
        self._tamaño = 0
    
    def invertir(self) -> None:
        """Invierte el orden de la lista"""
        anterior = None
        actual = self._cabeza
        
        while actual:
            siguiente = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = siguiente
        
        self._cabeza = anterior
    
    # ============ MÉTODOS ESPECIALES ============
    
    def __len__(self) -> int:
        """Permite usar len(lista)"""
        return self._tamaño
    
    def __getitem__(self, indice: int) -> Any:
        """Permite usar lista[indice]"""
        elemento = self.obtener(indice)
        if elemento is None:
            raise IndexError("Índice fuera de rango")
        return elemento
    
    def __setitem__(self, indice: int, valor: Any) -> None:
        """Permite usar lista[indice] = valor"""
        if indice < 0 or indice >= self._tamaño:
            raise IndexError("Índice fuera de rango")
        
        actual = self._cabeza
        for _ in range(indice):
            actual = actual.siguiente
        actual.dato = valor
    
    def __iter__(self) -> Iterator:
        """Permite iterar sobre la lista: for item in lista"""
        actual = self._cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
    
    def __str__(self) -> str:
        """Representación en string de la lista"""
        if self.esta_vacia():
            return "[]"
        
        elementos = []
        actual = self._cabeza
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        
        return "[" + " -> ".join(elementos) + "]"
    
    def __repr__(self) -> str:
        """Representación para depuración"""
        return f"ListaEnlazada({self.obtener_todos()})"


# ============ FUNCIONES DE PRUEBA ============

def probar_lista_enlazada():
    """Función de prueba para verificar que la lista funciona correctamente"""
    print("\n" + "="*50)
    print("PRUEBA DE LISTA ENLAZADA")
    print("="*50)
    
    # Crear lista
    lista = ListaEnlazada()
    print(f" Lista creada: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    
    # Agregar elementos
    print("\n--- Agregando elementos ---")
    for i in range(5):
        lista.agregar(f"Elemento {i}")
        print(f"Agregado: Elemento {i} - Lista: {lista}")
    
    print(f"\nTamaño: {len(lista)}")
    
    # Obtener elementos
    print("\n--- Obteniendo elementos ---")
    for i in range(len(lista)):
        print(f"Posición {i}: {lista[i]}")
    
    # Buscar
    print("\n--- Búsqueda ---")
    print(f"Buscar 'Elemento 2': índice {lista.buscar('Elemento 2')}")
    print(f"Buscar 'Inexistente': índice {lista.buscar('Inexistente')}")
    
    # Eliminar
    print("\n--- Eliminando ---")
    lista.eliminar(2)
    print(f"Después de eliminar índice 2: {lista}")
    
    lista.eliminar_por_valor("Elemento 4")
    print(f"Después de eliminar 'Elemento 4': {lista}")
    
    # Invertir
    print("\n--- Invirtiendo ---")
    lista.invertir()
    print(f"Lista invertida: {lista}")
    
    # Iterar
    print("\n--- Iterando ---")
    for i, elemento in enumerate(lista):
        print(f"  {i}: {elemento}")
    
    # Limpiar
    print("\n--- Limpiando ---")
    lista.limpiar()
    print(f"Lista después de limpiar: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    
    print("\n Todas las pruebas pasaron!")


if __name__ == "__main__":
    probar_lista_enlazada()