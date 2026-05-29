"""
PROYECTO FINAL - PROGRAMACIÓN I
Sistema de Pedidos de Ropa al Por Mayor
Fecha: Mayo 2026

Este código cumple con TODOS los requisitos del proyecto:
- POO 
- CRUD completo
- Estructuras de datos
- Principios SOLID (3 aplicados)
- Base de datos (SQLite)
- Algoritmos (búsqueda binaria, ordenamiento)
- Recursividad
- Manejo de archivos
- Excepciones
- Biblioteca propia
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional, Dict

# ==================== BIBLIOTECA PROPIA (Requisito Unidad 1) ====================
class Utilidades:
    """Biblioteca de funciones útiles - BIBLIOTECA PROPIA"""
    
    @staticmethod
    def validar_entero(valor: str) -> int:
        """Convierte a entero, lanza excepción si no es válido"""
        try:
            num = int(valor)
            if num <= 0:
                raise ValueError("Debe ser positivo")
            return num
        except ValueError:
            raise ValueError(f"'{valor}' no es un número entero válido")
    
    @staticmethod
    def validar_flotante(valor: str) -> float:
        """Convierte a float, lanza excepción si no es válido"""
        try:
            num = float(valor)
            if num <= 0:
                raise ValueError("Debe ser positivo")
            return num
        except ValueError:
            raise ValueError(f"'{valor}' no es un número válido")
    
    @staticmethod
    def validar_texto(valor: str) -> str:
        """Valida que el texto no esté vacío"""
        if not valor or valor.strip() == "":
            raise ValueError("El texto no puede estar vacío")
        return valor.strip()
    
    @staticmethod
    def formatear_moneda(valor: float) -> str:
        """Formatea como moneda"""
        return f"${valor:,.2f}"
    
    @staticmethod
    def generar_id() -> int:
        """Genera ID único basado en timestamp"""
        return int(datetime.now().timestamp() * 1000)


# ==================== CLASES POO (4 PILARES) ====================

# ABSTRACCIÓN - Clase base abstracta
class Prenda:
    """Clase abstracta que representa una prenda de ropa"""
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):
        # ENCAPSULAMIENTO - Atributos privados
        self._marca = marca
        self._cantidad = cantidad
        self._precio = precio
        self._tipo = tipo
    
    # Getters y Setters (ENCAPSULAMIENTO)
    def get_marca(self): return self._marca
    def get_cantidad(self): return self._cantidad
    def get_precio(self): return self._precio
    def get_tipo(self): return self._tipo
    
    def set_cantidad(self, cantidad): 
        if cantidad > 0: self._cantidad = cantidad
    
    def set_precio(self, precio): 
        if precio > 0: self._precio = precio
    
    # Método a ser sobrescrito (POLIMORFISMO)
    def calcular_total(self) -> float:
        return self._cantidad * self._precio
    
    def __str__(self):
        return f"{self._tipo} {self._marca} | {self._cantidad} uds | ${self._precio}/ud"


# HERENCIA - Clase que hereda de Prenda
class PrendaMayorista(Prenda):
    """Las prendas al por mayor tienen descuento por volumen"""
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):
        super().__init__(marca, cantidad, precio, tipo)
        self._descuento = 0.10  # 10% de descuento
    
    # POLIMORFISMO - Sobrescribe el método
    def calcular_total(self) -> float:
        total = self._cantidad * self._precio
        if self._cantidad >= 100:
            total *= (1 - self._descuento)
        return total


# Clase Usuario (ENCAPSULAMIENTO)
class Usuario:
    def __init__(self, nombre: str, rol: str):
        self._nombre = nombre
        self._rol = rol  # 'admin' o 'empleado'
    
    def get_nombre(self): return self._nombre
    def get_rol(self): return self._rol


# ==================== ESTRUCTURAS DE DATOS ====================

# LISTA ENLAZADA (Unidad 5)
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    """Implementación de lista enlazada simple"""
    
    def __init__(self):
        self._cabeza = None
        self._tamaño = 0
    
    def agregar(self, dato):
        nuevo = Nodo(dato)
        if not self._cabeza:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamaño += 1
    
    def eliminar(self, indice: int) -> bool:
        if indice < 0 or indice >= self._tamaño:
            return False
        if indice == 0:
            self._cabeza = self._cabeza.siguiente
        else:
            actual = self._cabeza
            for _ in range(indice - 1):
                actual = actual.siguiente
            actual.siguiente = actual.siguiente.siguiente
        self._tamaño -= 1
        return True
    
    def obtener(self, indice: int):
        if indice < 0 or indice >= self._tamaño:
            return None
        actual = self._cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato
    
    def obtener_todos(self):
        resultado = []
        actual = self._cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado
    
    def tamaño(self): return self._tamaño


# PILA (Stack) - Unidad 6
class Pila:
    """Implementación de Pila (LIFO) para deshacer acciones"""
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self._items.pop()
        return None
    
    def top(self):
        if not self.esta_vacia():
            return self._items[-1]
        return None
    
    def esta_vacia(self):
        return len(self._items) == 0
    
    def tamaño(self):
        return len(self._items)


# COLA (Queue) - Unidad 6
class Cola:
    """Implementación de Cola (FIFO) para pedidos pendientes"""
    
    def __init__(self):
        self._items = []
    
    def encolar(self, item):
        self._items.append(item)
    
    def desencolar(self):
        if not self.esta_vacia():
            return self._items.pop(0)
        return None
    
    def frente(self):
        if not self.esta_vacia():
            return self._items[0]
        return None
    
    def esta_vacia(self):
        return len(self._items) == 0
    
    def tamaño(self):
        return len(self._items)


# ==================== ALGORITMOS ====================

def busqueda_binaria(lista: List[Prenda], marca_buscar: str) -> int:
    """
    ALGORITMO DE BÚSQUEDA BINARIA (Unidad 3)
    Requiere lista ordenada por marca
    """
    izquierda, derecha = 0, len(lista) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        marca_actual = lista[medio].get_marca().lower()
        
        if marca_actual == marca_buscar.lower():
            return medio
        elif marca_actual < marca_buscar.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


def ordenar_por_precio(lista: List[Prenda]) -> List[Prenda]:
    """
    ALGORITMO DE ORDENAMIENTO (QuickSort) - Unidad 3
    Ordena prendas por precio total
    """
    if len(lista) <= 1:
        return lista
    
    pivote = lista[0].calcular_total()
    menores = [p for p in lista[1:] if p.calcular_total() <= pivote]
    mayores = [p for p in lista[1:] if p.calcular_total() > pivote]
    
    return ordenar_por_precio(menores) + [lista[0]] + ordenar_por_precio(mayores)


# FUNCIÓN RECURSIVA (Unidad 2)
def calcular_total_recursivo(pedidos: List[Prenda], indice: int = 0) -> float:
    """
    Calcula el total de todos los pedidos usando RECURSIVIDAD
    """
    if indice >= len(pedidos):
        return 0
    return pedidos[indice].calcular_total() + calcular_total_recursivo(pedidos, indice + 1)


def buscar_recursivo(pedidos: List[Prenda], indice: int, marca: str) -> int:
    """
    Búsqueda recursiva de una prenda por marca
    """
    if indice >= len(pedidos):
        return -1
    if pedidos[indice].get_marca().lower() == marca.lower():
        return indice
    return buscar_recursivo(pedidos, indice + 1, marca)


# ==================== BASE DE DATOS (CRUD) ====================

class BaseDatos:
    """Manejo de base de datos SQLite (no requiere instalación)"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.conn = sqlite3.connect('tienda_ropa.db')
            self.cursor = self.conn.cursor()
            self._crear_tablas()
            return True
        except Exception as e:
            print(f"Error de BD: {e}")
            return False
    
    def _crear_tablas(self):
        """DDL - Creación de tablas"""
        # Tabla de usuarios
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        ''')
        
        # Tabla de pedidos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                tipo TEXT NOT NULL,
                total REAL NOT NULL,
                fecha TEXT NOT NULL
            )
        ''')
        
        # Insertar usuarios por defecto
        self.cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES ('admin', 'admin123', 'admin')")
        self.cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES ('empleado', 'emp456', 'empleado')")
        self.conn.commit()
    
    # CREATE
    def insertar_pedido(self, prenda: Prenda) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO pedidos (marca, cantidad, precio, tipo, total, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (prenda.get_marca(), prenda.get_cantidad(), prenda.get_precio(),
                  prenda.get_tipo(), prenda.calcular_total(), datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error insertando: {e}")
            return False
    
    # READ
    def obtener_pedidos(self) -> List[Dict]:
        try:
            self.cursor.execute("SELECT * FROM pedidos ORDER BY fecha DESC")
            resultados = self.cursor.fetchall()
            return [{"id": r[0], "marca": r[1], "cantidad": r[2], "precio": r[3], "tipo": r[4], "total": r[5], "fecha": r[6]} for r in resultados]
        except Exception as e:
            print(f"Error obteniendo: {e}")
            return []
    
    # UPDATE
    def actualizar_pedido(self, id_pedido: int, marca: str, cantidad: int, precio: float, tipo: str) -> bool:
        try:
            total = cantidad * precio
            self.cursor.execute('''
                UPDATE pedidos SET marca=?, cantidad=?, precio=?, tipo=?, total=?
                WHERE id=?
            ''', (marca, cantidad, precio, tipo, total, id_pedido))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error actualizando: {e}")
            return False
    
    # DELETE
    def eliminar_pedido(self, id_pedido: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM pedidos WHERE id=?", (id_pedido,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando: {e}")
            return False
    
    def autenticar(self, nombre: str, password: str) -> Optional[Usuario]:
        try:
            self.cursor.execute("SELECT nombre, rol FROM usuarios WHERE nombre=? AND password=?", (nombre, password))
            resultado = self.cursor.fetchone()
            if resultado:
                return Usuario(resultado[0], resultado[1])
            return None
        except Exception as e:
            print(f"Error autenticando: {e}")
            return None
    
    def cerrar(self):
        if self.conn:
            self.conn.close()


# ==================== MANEJO DE ARCHIVOS ====================

def guardar_backup(pedidos: List[Prenda], archivo: str = "backup_pedidos.json"):
    """Guarda los pedidos en un archivo JSON"""
    try:
        datos = []
        for p in pedidos:
            datos.append({
                "marca": p.get_marca(),
                "cantidad": p.get_cantidad(),
                "precio": p.get_precio(),
                "tipo": p.get_tipo(),
                "total": p.calcular_total(),
                "fecha": datetime.now().isoformat()
            })
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando backup: {e}")
        return False


def cargar_backup(archivo: str = "backup_pedidos.json") -> List[Prenda]:
    """Carga pedidos desde archivo JSON"""
    try:
        if not os.path.exists(archivo):
            return []
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        pedidos = []
        for d in datos:
            p = PrendaMayorista(d["marca"], d["cantidad"], d["precio"], d["tipo"])
            pedidos.append(p)
        return pedidos
    except Exception as e:
        print(f"Error cargando backup: {e}")
        return []


def exportar_reporte(pedidos: List[Prenda], archivo: str = "reporte_pedidos.txt"):
    """Exporta reporte a archivo de texto"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("REPORTE DE PEDIDOS\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            for i, p in enumerate(pedidos, 1):
                f.write(f"Pedido #{i}\n")
                f.write(f"  Marca: {p.get_marca()}\n")
                f.write(f"  Cantidad: {p.get_cantidad()}\n")
                f.write(f"  Precio unitario: ${p.get_precio():.2f}\n")
                f.write(f"  Tipo: {p.get_tipo()}\n")
                f.write(f"  Total: ${p.calcular_total():.2f}\n")
                f.write("-"*40 + "\n")
            
            total = sum(p.calcular_total() for p in pedidos)
            f.write(f"\nTOTAL GENERAL: ${total:.2f}\n")
        return True
    except Exception as e:
        print(f"Error exportando: {e}")
        return False


# ==================== INTERFAZ DE USUARIO ====================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPresione ENTER para continuar...")


def mostrar_tabla(pedidos: List[Prenda]):
    """Muestra una tabla con los pedidos"""
    if not pedidos:
        print("\n No hay pedidos registrados")
        return
    
    print("\n" + "="*75)
    print(f"{'#':<4} {'Marca':<15} {'Cantidad':<10} {'Precio':<12} {'Tipo':<15} {'Total':<12}")
    print("-"*75)
    
    total_general = 0
    for i, p in enumerate(pedidos):
        total = p.calcular_total()
        total_general += total
        print(f"{i:<4} {p.get_marca():<15} {p.get_cantidad():<10} ${p.get_precio():<11.2f} {p.get_tipo():<15} ${total:<11.2f}")
    
    print("="*75)
    print(f" TOTAL GENERAL: ${total_general:.2f}")


def menu_empleado(db: BaseDatos, pedidos_actuales: List[Prenda], pila: Pila, cola: Cola):
    """Menú para empleados"""
    while True:
        limpiar_pantalla()
        print("\n" + "="*50)
        print("    SISTEMA DE PEDIDOS - EMPLEADO")
        print("="*50)
        print("1. Agregar nueva prenda")
        print("2. Ver pedido actual (tabla)")
        print("3. Buscar prenda (recursivo)")
        print("4. Calcular total (recursivo)")
        print("5. Ordenar pedidos por precio")
        print("6. Guardar y salir")
        print("="*50)
        
        opcion = input("\n Seleccione una opción: ")
        
        try:
            if opcion == "1":
                print("\n--- NUEVA PRENDA ---")
                marca = Utilidades.validar_texto(input("Marca: "))
                cantidad = Utilidades.validar_entero(input("Cantidad: "))
                precio = Utilidades.validar_flotante(input("Precio unitario: "))
                tipo = Utilidades.validar_texto(input("Tipo (remera/pantalón/etc): "))
                
                prenda = PrendaMayorista(marca, cantidad, precio, tipo)
                pedidos_actuales.append(prenda)
                pila.push(prenda)  # Apilar para posible deshacer
                cola.encolar(prenda)  # Encolar para procesamiento
                db.insertar_pedido(prenda)
                
                print(f"\n Prenda agregada: {prenda}")
                print(f" Total: {Utilidades.formatear_moneda(prenda.calcular_total())}")
                pausar()
            
            elif opcion == "2":
                mostrar_tabla(pedidos_actuales)
                pausar()
            
            elif opcion == "3":
                marca = input("\n Marca a buscar: ")
                indice = buscar_recursivo(pedidos_actuales, 0, marca)
                if indice >= 0:
                    print(f" Prenda encontrada en posición #{indice}")
                    print(f"   {pedidos_actuales[indice]}")
                else:
                    print(" Prenda no encontrada")
                pausar()
            
            elif opcion == "4":
                total = calcular_total_recursivo(pedidos_actuales)
                print(f"\n TOTAL RECURSIVO: {Utilidades.formatear_moneda(total)}")
                pausar()
            
            elif opcion == "5":
                if pedidos_actuales:
                    ordenados = ordenar_por_precio(pedidos_actuales)
                    print("\n PEDIDOS ORDENADOS POR PRECIO:")
                    for p in ordenados:
                        print(f"   {p} - Total: {Utilidades.formatear_moneda(p.calcular_total())}")
                else:
                    print(" No hay pedidos para ordenar")
                pausar()
            
            elif opcion == "6":
                guardar_backup(pedidos_actuales)
                print(" Saliendo...")
                break
            
            else:
                print(" Opción inválida")
                pausar()
        
        except ValueError as e:
            print(f" Error: {e}")
            pausar()
        except Exception as e:
            print(f" Error inesperado: {e}")
            pausar()


def menu_admin(db: BaseDatos):
    """Menú para administrador"""
    while True:
        limpiar_pantalla()
        print("\n" + "="*50)
        print("    SISTEMA DE PEDIDOS - ADMINISTRADOR")
        print("="*50)
        print("1. Ver todos los pedidos (Base de Datos)")
        print("2. Editar pedido (UPDATE)")
        print("3. Eliminar pedido (DELETE)")
        print("4. Exportar reporte a TXT")
        print("5. Salir")
        print("="*50)
        
        opcion = input("\n Seleccione una opción: ")
        
        try:
            if opcion == "1":
                pedidos_bd = db.obtener_pedidos()
                if not pedidos_bd:
                    print("\n No hay pedidos en la base de datos")
                else:
                    print("\n" + "="*90)
                    print(f"{'ID':<5} {'Marca':<15} {'Cantidad':<10} {'Precio':<12} {'Tipo':<15} {'Total':<12} {'Fecha':<20}")
                    print("-"*90)
                    for p in pedidos_bd:
                        print(f"{p['id']:<5} {p['marca']:<15} {p['cantidad']:<10} ${p['precio']:<11.2f} {p['tipo']:<15} ${p['total']:<11.2f} {p['fecha'][:19]}")
                pausar()
            
            elif opcion == "2":
                pedidos_bd = db.obtener_pedidos()
                if not pedidos_bd:
                    print("📭 No hay pedidos para editar")
                    pausar()
                    continue
                
                mostrar_tabla_simple_bd(pedidos_bd)
                id_editar = Utilidades.validar_entero(input("\nID del pedido a editar: "))
                
                # Buscar el pedido
                pedido_a_editar = None
                for p in pedidos_bd:
                    if p['id'] == id_editar:
                        pedido_a_editar = p
                        break
                
                if not pedido_a_editar:
                    print(" ID no encontrado")
                    pausar()
                    continue
                
                print(f"\nEditando pedido #{id_editar}")
                print(f"Datos actuales: {pedido_a_editar['marca']} - {pedido_a_editar['cantidad']} uds")
                
                nueva_marca = input(f"Nueva marca ({pedido_a_editar['marca']}): ") or pedido_a_editar['marca']
                nueva_cantidad = input(f"Nueva cantidad ({pedido_a_editar['cantidad']}): ")
                nueva_cantidad = Utilidades.validar_entero(nueva_cantidad) if nueva_cantidad else pedido_a_editar['cantidad']
                nuevo_precio = input(f"Nuevo precio ({pedido_a_editar['precio']}): ")
                nuevo_precio = Utilidades.validar_flotante(nuevo_precio) if nuevo_precio else pedido_a_editar['precio']
                nuevo_tipo = input(f"Nuevo tipo ({pedido_a_editar['tipo']}): ") or pedido_a_editar['tipo']
                
                if db.actualizar_pedido(id_editar, nueva_marca, nueva_cantidad, nuevo_precio, nuevo_tipo):
                    print(" Pedido actualizado correctamente")
                else:
                    print(" Error al actualizar")
                pausar()
            
            elif opcion == "3":
                pedidos_bd = db.obtener_pedidos()
                if not pedidos_bd:
                    print(" No hay pedidos para eliminar")
                    pausar()
                    continue
                
                mostrar_tabla_simple_bd(pedidos_bd)
                id_eliminar = Utilidades.validar_entero(input("\nID del pedido a eliminar: "))
                
                confirmar = input(f" ¿Seguro que desea eliminar el pedido #{id_eliminar}? (s/n): ")
                if confirmar.lower() == 's':
                    if db.eliminar_pedido(id_eliminar):
                        print(" Pedido eliminado correctamente")
                    else:
                        print(" Error al eliminar")
                else:
                    print(" Eliminación cancelada")
                pausar()
            
            elif opcion == "4":
                pedidos_bd = db.obtener_pedidos()
                if not pedidos_bd:
                    print(" No hay pedidos para exportar")
                else:
                    # Convertir a objetos Prenda para exportar
                    prendas_export = []
                    for p in pedidos_bd:
                        prenda = PrendaMayorista(p['marca'], p['cantidad'], p['precio'], p['tipo'])
                        prendas_export.append(prenda)
                    
                    if exportar_reporte(prendas_export):
                        print(" Reporte exportado a 'reporte_pedidos.txt'")
                    else:
                        print(" Error al exportar")
                pausar()
            
            elif opcion == "5":
                print(" Saliendo del panel admin...")
                break
            
            else:
                print(" Opción inválida")
                pausar()
        
        except ValueError as e:
            print(f" Error: {e}")
            pausar()
        except Exception as e:
            print(f" Error inesperado: {e}")
            pausar()


def mostrar_tabla_simple_bd(pedidos):
    """Muestra tabla simple para la BD"""
    print("\n" + "="*70)
    print(f"{'ID':<5} {'Marca':<15} {'Cantidad':<10} {'Precio':<10} {'Tipo':<12} {'Total':<12}")
    print("-"*70)
    for p in pedidos:
        print(f"{p['id']:<5} {p['marca']:<15} {p['cantidad']:<10} ${p['precio']:<9.2f} {p['tipo']:<12} ${p['total']:<11.2f}")


# ==================== PRINCIPIO SOLID APLICADOS ====================
# 1. SRP - Single Responsibility: Cada clase tiene una única responsabilidad
#    - BaseDatos: solo maneja BD
#    - Utilidades: solo funciones auxiliares
#    - ListaEnlazada, Pila, Cola: cada una su estructura

# 2. OCP - Open/Closed: Las clases Prenda están abiertas para extensión
#    (podemos crear nuevos tipos de prenda sin modificar el código existente)

# 3. DIP - Dependency Inversion: Las funciones dependen de abstracciones
#    (trabajan con listas de Prenda, no con implementaciones concretas)


# ==================== PROGRAMA PRINCIPAL ====================

def main():
    """Punto de entrada del programa"""
    print("\n" + "="*60)
    print("    SISTEMA DE PEDIDOS - ROPA AL POR MAYOR")
    print("   PROYECTO FINAL - PROGRAMACIÓN I")
    print("="*60)
    
    # Inicializar componentes
    db = BaseDatos()
    
    try:
        if not db.conectar():
            print(" Error con BD, usando modo local")
            usar_bd = False
        else:
            usar_bd = True
            print(" Base de datos conectada")
    except Exception as e:
        print(f" No se pudo conectar a BD: {e}")
        usar_bd = False
    
    # Cargar datos
    pedidos_actuales = cargar_backup()
    pila_deshacer = Pila()
    cola_pendientes = Cola()
    
    print(f" Cargados {len(pedidos_actuales)} pedidos del backup")
    
    # Login
    while True:
        print("\n" + "-"*40)
        print(" INICIO DE SESIÓN")
        print("-"*40)
        usuario = input("Usuario: ")
        password = input("Contraseña: ")
        
        if usar_bd:
            user_obj = db.autenticar(usuario, password)
        else:
            # Modo local sin BD
            if usuario == "admin" and password == "admin123":
                user_obj = Usuario("admin", "admin")
            elif usuario == "empleado" and password == "emp456":
                user_obj = Usuario("empleado", "empleado")
            else:
                user_obj = None
        
        if user_obj:
            print(f"\n Bienvenido {user_obj.get_nombre()} (Rol: {user_obj.get_rol()})")
            pausar()
            
            if user_obj.get_rol() == "admin":
                menu_admin(db if usar_bd else None)
            else:
                menu_empleado(db if usar_bd else None, pedidos_actuales, pila_deshacer, cola_pendientes)
            break
        else:
            print("❌ Usuario o contraseña incorrectos")
            pausar()
    
    db.cerrar()
    print("\n ¡Gracias por usar el sistema!")


if __name__ == "__main__":
    main()