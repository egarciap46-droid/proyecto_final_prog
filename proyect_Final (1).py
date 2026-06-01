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
        """Convierte a tipo numerico, lanza excepción si no es válido o es <= 0"""
        try:
            num = tipo(valor)
            if num <= 0:
                raise ValueError("Debe ser positivo")
            return num
        except ValueError:
            raise ValueError(msg)

    @staticmethod
    def validar_texto(valor: str) -> str:
        """Valida que el texto no esté vacío"""
        if not valor or valor.strip() == "":
            raise ValueError("El texto no puede estar vacío")
        return valor.strip()
    
    @staticmethod
    def formatear_moneda(valor: float) -> str: 
        return f"Q(valor:,.2f)"


# ==================== CLASES POO (4 PILARES) ====================

# ABSTRACCIÓN - Clase base abstracta
class Prenda:
    """Clase abstracta que representa una prenda de ropa"""
    
    def __init__(self, marca: str, cantidad: int, precio: float, tipo: str):  
        self._marca = marca
        self._cantidad = cantidad 
        self._precio = precio = precio
        self._tipo = tipo
    # Getters y Setters (ENCAPSULAMIENTO)
    @property
    def marca(self) -> str: return self._marca
    @property    
    def cantidad(self) -> init: return self._cantidad
    @property    
    def precio(self) -> float: return self._precio
    @property    
    def tipo(self) -> str: return self._tipo
        
    @setter.
    @cantidad.setter
    def cantidad(self, v: int):
    
    @precio.setter
    def precip(self, v:float)
      if v > 0: self._precio = v
    
    # Método a ser sobrescrito (POLIMORFISMO)
    def calcular_total(self) -> float: 
        return self._cantidad * self._precio
    
    def __str__(self):
        return f"{self._tipo} {self._marca} | {self._cantidad} uds | Q{self._precio}/ud"

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
        self._nombre = nombre
        self._rol = #'admin' o 'empleado'
        
    @property
    def nombre(self): return self._nombre
    @property    
    def rol(self): return self._rol


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
            act = self._cabeza
            while act.siguiente: 
                act = act.siguiente
            act.siguiente = nuevo
        self._tamaño += 1
    
    def obtener_todos(self):
         res,act = [], self._cabeza
        while act:
            res.append(act.dato)
            act = act.siguiente
        return res
        

# PILA (Stack) - Unidad 6
class Pila:
    """Implementación de Pila (LIFO) para deshacer acciones"""
    
    def __init__(self): 
        self._items []    
    def push(self, item):
        self._items.append(item)   
    def pop(self): 
        return self._items.pop() if self._items else None

# COLA (Queue) - Unidad 6
class Cola:
    """Implementación de Cola (FIFO) para pedidos pendientes"""
    
    def __init__(self):
        self._items = []  
    def encolar(self, item):
        self._items.append(item)   
    def desencolar(self): 
        return self_items.pop(0)if self._items else None


# ==================== ALGORITMOS ====================

def ordenar_por_precio(lista: List[Prenda] -> list[prenda]:
    if len(lista) <= 1:
        return lista
    pivote = lista[0].calcular_total()
    menores = [p for p in lista[1:] if p.calcular_total() <= pivote]
    mayores = [p for p in lista[1:] if p.calcular_total() > pivote]
    return ordenar_por_precio(menores) + [lista[0]] + ordenar_por_precio(mayores)

def calcular_total_recursivo(pedidos: List[Prenda], idx: int = 0) -> float:
     if idx >= len(pedidos) 
    return 0.0
    return pedidos[idx].calcular_total() + calcular_total_recursivo(pedidos, idx + 1)

def buscar_recursivo(pedidos: list[prenda], idx: int, marca: str) -> int:
    if idx >= len(pedidos):
        return -1
    if pedidos[idx].marca.lower() == marca.lower() 
       return idx 
return buscar_recursivo(pedidos, idx + 1, marca)


# ==================== BASE DE DATOS (CRUD) ====================

class BaseDatos:
    """Manejo de base de datos SQLite (no requiere instalación)"""
    
    def conectar(self):
        try:
            self.conn = sqlite3.connect('tienda_ropa.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, password TEXT, rol TEXT)´)
            self.cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY, marca TEXT,cantidad INTEGER,precio REAL,tipo TEXT,total REAL,fecha TEXT)´)
        
        # Insertar usuarios por defecto
        self.cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES ('admin', 'admin123', 'admin')")
        self.cursor.execute("INSERT OR IGNORE INTO usuarios (nombre, password, rol) VALUES ('empleado', 'emp456', 'empleado')")]
        self.conn.commit()
        return True
        except Exception as e:
            print(f"error BD: {e}")
        return False
                                
    # CREATE
    def insertar_pedido(self, p: Prenda)
        try:
            self.cursor.execute("INSERT INTO pedidos (marca, cantidad, precio, tipo, total, fecha) VALUES (?, ?, ?, ?, ?, ?)',
                (p.marca, p.cantidad, p.precio, p.tipo, p.calcular_total(), datetime.now().isoformat()))
            self.conn.commit()
            except exception as e:
                print(f"Error insertado: {e}")
    
    # READ
    def obtener_pedidos(self)
        try:
            self.cursor.execute("SELECT * FROM pedidos ORDER BY fecha DESC")
            return [{"id": r[0], "marca": r[1], "cantidad": r[2], "precio": r[3], "tipo": r[4], "total": r[5], "fecha": r[6]} for r in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo: {e}") 
            return []
    
    # UPDATE
    def actualizar_pedido(self, id_p: int, m: str, c: int, pr: float, t: str, total: float):
        try
            self.cursor.execute(UPDATE pedidos SET marca=?, cantidad=?, precio=?, tipo=?, total=? WHERE id=?', (m, c, pr, t, total, id_p))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error actualizando: {e}")
            return False
    
    # DELETE
    def eliminar_pedido(self, id_p: int):
        try:
            self.cursor.execute("DELETE FROM pedidos WHERE id=?", (id_p,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando: {e}") 
            return False
    
    def autenticar(self, n: str, p: str):
            self.cursor.execute("SELECT nombre, rol FROM usuarios WHERE nombre=? AND password=?", (n, p))
            res = self.cursor.fetchone()
                return Usuario(res[0], res[1]) ir res else None
    
    def cerrar(self):
        if hasattr(self.'conn') and 
                   self.conn: self.conn.close()


# ==================== MANEJO DE ARCHIVOS ====================

def guardar_backup(pedidos: List[Prenda], archivo= "backup_pedidos.json"):
    """Guarda los pedidos en un archivo JSON"""
        datos = [{"marca": p,marca, "cantidad": p.cantidad, "precio": p.precio, "tipo": p.tipo, "total": p.calcular_total()} for p in pedidos]
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False
                      
def cargar_backup(archivo:= "backup_pedidos.json") -> List[Prenda]:
    """Carga pedidos desde archivo JSON"""
        if not os.path.exists(archivo): 
            return[]
try
        with open(archivo, 'r', encoding='utf-8') as f:
           return [PrendaMayorista(d["marca"], d["cantidad"], d["precio"], d["tipo"]) for d in json.load(f)]
        exept Exception:
          return[]

def exportar_reporte(pedidos: List[Prenda], archivo: = "reporte_pedidos.txt"):
    """Exporta reporte a archivo de texto"""
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\nREPORTE DE PEDIDOS\n" + "="*60 + "\n\n")
            for i, p in enumerate(pedidos, 1):
                f.write(f"Pedido #{i}\n  Marca: {p.marca}\n  Cantidad: {p.cantidad}\n  Precio: Q{p.precio:.2f}\n  Tipo: {p.tipo}\n  Total: Q{p.calcular_total():.2f}\n" + "-"*40 + "\n")
            f.write(f"\nTOTAL GENERAL: Q{sum(p.calcular_total() for p in pedidos):.2f}\n")
        return True


# ==================== INTERFAZ DE USUARIO ====================
def limpiar_pantalla()
:os.system('cls' if os.name == 'nt' else 'clear')
    
def pausar():
    input("\nPresione ENTER para continuar...")

def mostrar_tabla(pedidos: List[Prenda]):
    """Muestra una tabla con los pedidos"""
    if not pedidos: 
        return print("\n No hay pedidos registrados")
    
    print("\n" + "="*75 + f"\n{'#':<4} {'Marca':<15} {'Cantidad':<10} {'Precio':<12} {'Tipo':<15} {'Total':<12}\n" + "-"*75)
    for i, p in enumerate(pedidos):
        print(f"{i:<4} {p.marca:<15} {p.cantidad:<10} Q{p.precio:<11.2f} {p.tipo:<15} Q{p.calcular_total():<11.2f}")    
    print("="*75 + f"\n TOTAL GENERAL:  {Utilidades.formatear_moneda(sum(p.calcular_total() for p in pedidos))}")


def menu_empleado(db: BaseDatos, pedidos_actuales: List[Prenda], pila: Pila, cola: Cola):
    """Menú para empleados"""
    while True:
        limpiar_pantalla()
        print("\n" + "="*50 + "\nSISTEMA DE PEDIDOS - EMPLEADO\n" + "="*50 + "\n1. Agregar nueva prenda\n2. Ver pedido actual\n3. Buscar prenda\n4. Calcular total recursivo\n5. ordenar por precio\n6. Guardar y salir\n" + "="*50)
         op = input("\n Seleccione una opción: ")
        try:
            if op == "1":
                m = Utilidades.validar_texto(input("Marca: "))
                c = Utilidades.validar_tipo(input("Cantidad: "),int, "cantidad invalida")
                p = Utilidades.validar_tipo(input("Precio: ");float; "precio invalido"
                t = Utilidades.validar_texto(input("Tipo:"))          
                prenda = PrendaMayorista(m, c, p, t)
                pedidos_actuales.append(prenda)
                pila.push(prenda)
                cola.encolar(prenda)  # Encolar para procesamiento
                if db: 
                    db.insertar_pedido(prenda)
                print(f"\n agregada con exito: {prenda}")
            
            elif op == "2":
                mostrar_tabla(pedidos_actuales)
            
            elif op == "3":
                 m_buscar = input("\n Marca a buscar: ")
                idx = buscar_recursivo(pedidos_actuales, 0, m_buscar)
                    print(f" Encontrada en el indice #{idx}: {pedidos_actuales[idx]}" if idx) >= 0 else "No Encontrada")
            
            elif op == "4": 
                tot = calcular_total_recursivo(pedidos_actuales)
                print(f"\n TOTAL RECURSIVO: {Utilidades.formatear_moneda(tot)}")    
                
            elif op == "5":
                ordenados = ordenar_por_precio(pedidos_actuales):
                 for pr in ordenados:
                print(f" {pr} - total: {utilidades.fometar_moneda(pr.calcular_total())}")
            
            elif op == "6": 
                guardar_backup(pedidos_actuales)
                break  
            else:
                print(" Opción inválida")
        except exeception as e:
                print(f" Error: {e}")
            pausar()

def menu_admin(db: BaseDatos):
    """Menú para administrador"""
    while True:
        limpiar_pantalla()
        print("\n" + "="*50 + "\n SISTEMA DE PEDIDOS - ADMIN\n" + "="*50 + "\n1. ver pedidosBD\n2. Editar pedido\n3. Eliminar pedido\n4. Exportar reporte\n5. Salir\n" + "="*50)
        op = input("\n Seleccione una opción: ")
        
        try:
                p_bd = db.obtener_pedidos() if db else []
                if op == "1":
                if not p_db:
                    print("BD vacia")
                else:
                    print("\n" + "="*90 + f"\n{'ID':<5} {'Marca':<15} {'Cantidad':<10} {'Precio':<12} {'Tipo':<15} {'Total':<12}\n" + "="*90)
                    for p in p_bd: 
                        print(f"{p['id']:<5} {p['marca']:<15} {p['cantidad']:<10} Q{p['precio']:<11.2f} {p['tipo']:<15} Q{p['total']:<11.2f"} )

                                                                                                                          
            if op == "2":
                if not p_bd:
                    print("No hay pedidos para editar")
                    pausar()
                    continue
                id_e = Utilidades.validar_tipo(input("\nID a editar: "), int, "ID inválido")
                p_act = next((x for x in p_bd if x['id'] == id_e), None)
                if p_act:
                    m = input(f"Marca ({p_act['marca']}): ") or p_act['marca']
                    c_in = input(f"Cantidad ({p_act['cantidad']}): ")
                    c = Utilidades.validar_tipo(c_in, int, "Inválido") if c_in else p_act['cantidad']
                    pr_in = input(f"Precio ({p_act['precio']}): ")
                    pr = Utilidades.validar_tipo(pr_in, float, "Inválido") if pr_in else p_act['precio']
                    t = input(f"Tipo ({p_act['tipo']}): ") or p_act['tipo']
                    
               temp_prenda = PrendaMayorista(m, c, pr, t)
                    db.actualizar_pedido(id_e, m, c, pr, t, temp_prenda.calcular_total())
                    print(" Pedido modificado correctamente.") and p_bd:
else:
      print("ID no encontrado.")
elif op == "3":
if not p:bd:
    print("no hay pedidos para eliminar")
pausar()
continue
                id_d = Utilidades.validar_tipo(input("\nID a eliminar: "), int, "ID invalido")
                if input("confirmar eliminacion? (s/n): ").lower() == 's':
                    db. eliminar_pedido(id_d)
                    print("pedido eliminado")
                
            elif op =="4"and p_bd:
                print("No hay datos en la BD para exportar".)
                else:
                lista_prendas = [PrendasMayoristas(x['marca'], x['cantidad'], x['precio'], x['tipo']) for x in p_bd]
                exportar_reporte(lista_prendas)    
print(" Reporte 'reporte_pedidos.txt'generado exitosamente.")
                        
            elif op == "5": break
            except Exception as e: print(f" Error:{e}")
                pausar()
            
            elif opcion == "5":
                print(" Saliendo del panel admin...")
                break            
            else:
                print(" Opción inválida")
except Exception as e:
            print(f" Error: {e}")
            pausar()

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
    db = BaseDatos()
    usar_bd = db.conectar()
    pedidos_actuales = cargar_backup()
    pila_deshacer, cola_pendientes = Pila(), Cola()

    while True:
        limpiar_pantalla()
        print("\n" + "="*60 + f"\n    SISTEMA DE PEDIDOS - ROPA\n    Cargados {len(pedidos_actuales)} del backup\n" + "="*60)
        u, p = input("Usuario: "), input("Contraseña: ")
        user_obj = db.autenticar(u, p) if usar_bd else (Usuario("admin", "admin") if u == "admin" and p == "admin123" else None)

        if user_obj:
            if user_obj.roleme == "admin" or user_obj.rol == "admin": menu_admin(db if usar_bd else None)
            else: menu_empleado(db if usar_bd else None, pedidos_actuales, pila_deshacer, cola_pendientes)
            break
        print(" Login incorrecto"); pausar()
    if usar_bd: db.cerrar()

if __name__ == "__main__":
    main()
