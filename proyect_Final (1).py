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
    def validar_tipo(valor: str,tipo,msg:str)
        """Convierte a entero, lanza excepción si no es válido"""
        try:
            num = tipo(valor)
            if num <= 0:raise ValueError("Debe ser positivo")
            return num
        except ValueError:raise ValueError(msg)
    
    @staticmethod
    def validar_texto(valor: str) -> str:
        """Convierte a str, valor numerico para validar que sea positivo"""
            if not valor or not valor.strip():raise valueError("el texto no puede estar vacio"
            return valor.strip()
    
    @staticmethod
    def validar_texto(valor: str) -> str:
        """Valida que el texto no esté vacío"""
        if not valor or valor.strip() == "":
            raise ValueError("El texto no puede estar vacío")
        return valor.strip()
    
    @staticmethod
    def formatear_moneda(valor: float) -> str: return f"Q(valor:,.2f)"


# ==================== CLASES POO (4 PILARES) ====================

# ABSTRACCIÓN - Clase base abstracta
class Prenda:
    """Clase abstracta que representa una prenda de ropa"""
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):  
        self._marca, self._cantidad, self._precio, self._tipo=marca, cantidad, precio,tipo
    # Getters y Setters (ENCAPSULAMIENTO)
    @property
    def get_marca(self): return self._marca
    @property    
    def get_cantidad(self): return self._cantidad
    @property    
    def get_precio(self): return self._precio
    @property    
    def get_tipo(self): return self._tipo
        
    @cantidad.setter
    def cantidad(self, V): self._cantidad =v if v > 0 else self._cantidad
    
    def precio(self, v): self._precio=v if v > 0 else self._precio
    
    # Método a ser sobrescrito (POLIMORFISMO)
    def calcular_total(self) -> float: return self._cantidad * self._precio
    
    def __str__(self): return f"{self._tipo} {self._marca} | {self._cantidad} uds | Q{self._precio}/ud"

# HERENCIA - Clase que hereda de Prenda
class PrendaMayorista(Prenda):
    """Las prendas al por mayor tienen descuento por volumen"""
    
    # POLIMORFISMO - Sobrescribe el método
    def calcular_total(self) -> float:
        total = super().calcular_total()
        return total * 0.90 if self._cantidad >= 100 else total
        
# Clase Usuario (ENCAPSULAMIENTO)
class Usuario:
    def __init__(self, nombre: str, rol: str):
        self._nombre, self._rol = nombre, rol  # 'admin' o 'empleado'
    @property
    def nombre(self): return self._nombre
    @property    
    def rol(self): return self._rol


# ==================== ESTRUCTURAS DE DATOS ====================

# LISTA ENLAZADA (Unidad 5)
class Nodo:
    def __init__(self, dato):
        self.dato, self.siguiente = dato, None

class ListaEnlazada:
    """Implementación de lista enlazada simple"""
    
    def __init__(self):
        self._cabeza, self._tamaño = None, 0
    
    def agregar(self, dato):
        nuevo = Nodo(dato)
        if not self._cabeza: self._cabeza = nuevo
        else:
            act = self._cabeza
            while act.siguiente: act = act.siguiente
            act.siguiente = nuevo
        self._tamaño += 1
    
    def obtener_todos(self):
         res,act = [], self._cabeza
        while act: res.append(act.dato);act = act.siguiente
        return res
        

# PILA (Stack) - Unidad 6
class Pila:
    """Implementación de Pila (LIFO) para deshacer acciones"""
    
    def __init__(self): self._items []    
    def push(self, item): self._items.append(item)   
    def pop(self): return self._items.pop() if self._items else None

# COLA (Queue) - Unidad 6
class Cola:
    """Implementación de Cola (FIFO) para pedidos pendientes"""
    
    def __init__(self): self._items = []  
    def encolar(self, item):self._items.append(item)   
    def desencolar(self): return self._items.pop(0) if self._items else None


# ==================== ALGORITMOS ====================

def ordenar_por_precio(lista: List[Prenda] -> list[prenda]:
    if len(lista) <= 1: return lista
    pivote = lista[0].calcular_total()
    menores = [p for p in lista[1:] if p.calcular_total() <= pivote]
    mayores = [p for p in lista[1:] if p.calcular_total() > pivote]
    return ordenar_por_precio(menores) + [lista[0]] + ordenar_por_precio(mayores)

def calcular_total_recursivo(pedidos: List[Prenda], idx: int = 0) -> float:
    return 0 if idx >= len(pedidos) else pedidos[idx].calcular_total() +
calcular_total_recursivo(pedidos, idx + 1)

def buscar_recursivo(pedidos: list[prenda], idx: int, marca: str) -> int:
    if idx >= len(pedidos): return -1
    return idx if pedidos[idx].marca.lower() == marca.lower() else buscar_recursivo(pedidos, idx + 1, marca)


# ==================== BASE DE DATOS (CRUD) ====================

class BaseDatos:
    """Manejo de base de datos SQLite (no requiere instalación)"""
    
    def conectar(self):
        try:
            self.conn = sqlite3.connect('tienda_ropa.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, password TEXT, rol TEXT)´)
            self.cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY, marca TEXT,cantidad INTEGER,precio REAL,tipo TEXT,total REA,fecha TEXT)´)
        
        # Insertar usuarios por defecto
        # self.cursor.executemany("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES (?,?,?)",[('admin', 'admin123', 'admin'),('empleado', 'emp456', 'empleado' 
        self.cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES ('empleado', 'emp456', 'empleado')")]
        self.conn.commit()
        return True
        except Exception as e: return print(f"error BD: {e}") or False
                                
    # CREATE
    def insertar_pedido(self, p: Prenda)
        try:
            self.cursor.execute("INSERT INTO pedidos (marca, cantidad, precio, tipo, total, fecha) VALUES (?, ?, ?, ?, ?, ?)',
                (p.marca, p.cantidad, p.precio, p.tipo, p.calcular_total(),
    datetime.now().isoformat()))
            self.conn.commit()
            except exception as e: print(f"Error insertado: {e}")
    
    # READ
    def obtener_pedidos(self)
        try:
            self.cursor.execute("SELECT * FROM pedidos ORDER BY fecha DESC")
            return [{"id": r[0], "marca": r[1], "cantidad": r[2], "precio": r[3], "tipo": r[4], "total": r[5], "fecha": r[6]} for r in self.cursor.fetchall()]
        except Exception as e: return print(f"Error obteniendo: {e}") or []
    
    # UPDATE
    def actualizar_pedido(self, id_p: int, m: str, c: int, pr: float, t: str):
        try
            self.cursor.execute(UPDATE pedidos SET marca=?, cantidad=?, precio=?, tipo=?, total=? WHERE id=?', (m, c, pr, t, c*pr, id_p))
            self.conn.commit()
            return True
        except Exception as e: return print(f"Error actualizando: {e}") or False
            return False
    
    # DELETE
    def eliminar_pedido(self, id_p: int):
        try:
            self.cursor.execute("DELETE FROM pedidos WHERE id=?", (id_p,))
            self.conn.commit()
            return True
        except Exception as e: return print(f"Error eliminando: {e}") or False
    
    def autenticar(self, n: str, p: str):
            self.cursor.execute("SELECT nombre, rol FROM usuarios WHERE nombre=? AND password=?", (n, p))
            res = self.cursor.fetchone()
                return Usuario(res[0], res[1]) ir res else None
    
    def cerrar(self):
        if hasattr(self.'conn') and self.conn: self.conn.close()


# ==================== MANEJO DE ARCHIVOS ====================

def guardar_backup(pedidos: List[Prenda], archivo= "backup_pedidos.json"):
    """Guarda los pedidos en un archivo JSON"""
        datos = [{"marca": p,marca, "cantidad": p.cantidad, "precio": p.precio, "tipo": p.tipo, "total": p.calcular_total(), "fecha": datetime.now().isoformat()} for p in pedidos]

        with open(archivo, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=2, ensure_ascii=False

def cargar_backup(archivo:= "backup_pedidos.json") -> List[Prenda]:
    """Carga pedidos desde archivo JSON"""
        if not os.path.exists(archivo): return[]
        with open(archivo, 'r', encoding='utf-8') as f:
           return [PrendaMayorista(d["marca"], d["cantidad"], d["precio"], d["tipo"]) for d in json.load(f)]

def exportar_reporte(pedidos: List[Prenda], archivo: = "reporte_pedidos.txt"):
    """Exporta reporte a archivo de texto"""
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\nREPORTE DE PEDIDOS\n" + "="*60 + "\n\n")
            for i, p in enumerate(pedidos, 1):
                f.write(f"Pedido #{i}\n" Marca: {p.marca}\n Cantidad: {p.cantidad}\n Precio: Q{p.precio:.2f}\n Tipo: {p.tipo}\n Total: Q{p.calcular_total():.2f}\n" + "-"*40 + "\n")
            f.write(f"\nTOTAL GENERAL: Q{sum(p.calcular_total() for p in pedidos):.2f}\n")
        return True


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
            print(" Usuario o contraseña incorrectos")
            pausar()
    
    db.cerrar()
    print("\n ¡Gracias por usar el sistema!")


if __name__ == "__main__":
    main()
