import numpy as np
import time
import tracemalloc
import random
import math
import copy
from heapq import heappush, heappop

class SudokuAStar:
    def __init__(self, tablero, heuristica='conflictos'):
        self.tablero_inicial = copy.deepcopy(tablero)
        self.tablero = copy.deepcopy(tablero)
        self.n = 9
        self.heuristica_tipo = heuristica
        self.nodos_explorados = 0
        
    def obtener_vacios(self, tablero):
        """Obtiene las celdas vacías"""
        vacios = []
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    vacios.append((i, j))
        return vacios
    
    def obtener_posibles(self, tablero, fila, col):
        """Obtiene números posibles para una celda"""
        usados = set()
        
        # Fila
        for j in range(9):
            if tablero[fila][j] != 0:
                usados.add(tablero[fila][j])
        
        # Columna
        for i in range(9):
            if tablero[i][col] != 0:
                usados.add(tablero[i][col])
        
        # Subcuadrícula 3x3
        sub_fila = (fila // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_fila, sub_fila + 3):
            for j in range(sub_col, sub_col + 3):
                if tablero[i][j] != 0:
                    usados.add(tablero[i][j])
        
        posibles = [num for num in range(1, 10) if num not in usados]
        return posibles
    
    def heuristica_conflictos(self, tablero):
        """Heurística: número total de conflictos"""
        conflictos = 0
        
        # Verificar filas
        for i in range(9):
            fila = [tablero[i][j] for j in range(9) if tablero[i][j] != 0]
            conflictos += len(fila) - len(set(fila))
        
        # Verificar columnas
        for j in range(9):
            col = [tablero[i][j] for i in range(9) if tablero[i][j] != 0]
            conflictos += len(col) - len(set(col))
        
        # Verificar subcuadrículas 3x3
        for sub_i in range(3):
            for sub_j in range(3):
                sub = []
                for i in range(sub_i*3, sub_i*3 + 3):
                    for j in range(sub_j*3, sub_j*3 + 3):
                        if tablero[i][j] != 0:
                            sub.append(tablero[i][j])
                conflictos += len(sub) - len(set(sub))
        
        return conflictos
    
    def es_solucion(self, tablero):
        """Verifica si el tablero está completamente resuelto"""
        return self.heuristica_conflictos(tablero) == 0 and self.obtener_vacios(tablero) == []
    
    def generar_vecinos(self, tablero):
        """Genera estados vecinos llenando una celda vacía con un número posible"""
        vecinos = []
        vacios = self.obtener_vacios(tablero)
        
        if not vacios:
            return vecinos
        
        # Ordenar vacíos por número de posibles (MRV - Minimum Remaining Values)
        vacios_con_posibles = []
        for fila, col in vacios:
            posibles = self.obtener_posibles(tablero, fila, col)
            vacios_con_posibles.append((len(posibles), fila, col, posibles))
        
        vacios_con_posibles.sort()  # El que tiene menos posibles primero
        
        # Generar vecinos para el primer vacío
        _, fila, col, posibles = vacios_con_posibles[0]
        for num in posibles:
            nuevo = copy.deepcopy(tablero)
            nuevo[fila][col] = num
            vecinos.append(nuevo)
        
        return vecinos
    
    def resolver(self):
        """Resuelve Sudoku usando A*"""
        inicio = copy.deepcopy(self.tablero_inicial)
        
        # Usar tupla para hacer hash del estado
        def tablero_a_hash(t):
            return tuple(tuple(fila) for fila in t)
        
        abiertos = []
        g = {tablero_a_hash(inicio): 0}
        padre = {tablero_a_hash(inicio): None}
        
        # Costo inicial
        h_inicial = self.heuristica_conflictos(inicio)
        heappush(abiertos, (h_inicial, 0, inicio))  # (f, g, estado)
        
        self.nodos_explorados = 0
        
        while abiertos:
            f_actual, g_actual, actual = heappop(abiertos)
            self.nodos_explorados += 1
            
            if self.es_solucion(actual):
                return self.reconstruir_camino(padre, tablero_a_hash(actual))
            
            for vecino in self.generar_vecinos(actual):
                nuevo_g = g_actual + 1
                vecino_hash = tablero_a_hash(vecino)
                
                if vecino_hash not in g or nuevo_g < g[vecino_hash]:
                    g[vecino_hash] = nuevo_g
                    h = self.heuristica_conflictos(vecino)
                    f = nuevo_g + h
                    heappush(abiertos, (f, nuevo_g, vecino))
                    padre[vecino_hash] = tablero_a_hash(actual)
        
        return None
    
    def reconstruir_camino(self, padre, estado_hash):
        """Reconstruye la solución"""
        camino = []
        while estado_hash:
            # Convertir hash a lista
            estado = [list(fila) for fila in estado_hash]
            camino.append(estado)
            estado_hash = padre[estado_hash]
        return camino[::-1]


class SudokuSimulatedAnnealing:
    def __init__(self, tablero, temperatura_inicial=100, enfriamiento=0.99, iteraciones=10000):
        self.tablero_inicial = copy.deepcopy(tablero)
        self.temperatura = temperatura_inicial
        self.enfriamiento = enfriamiento
        self.iteraciones = iteraciones
        self.costo_final = 0
        self.iteraciones_realizadas = 0
        
    def obtener_vacios(self, tablero):
        """Obtiene las celdas vacías"""
        vacios = []
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    vacios.append((i, j))
        return vacios
    
    def obtener_posibles(self, tablero, fila, col):
        """Obtiene números posibles para una celda"""
        usados = set()
        
        for j in range(9):
            if tablero[fila][j] != 0:
                usados.add(tablero[fila][j])
        
        for i in range(9):
            if tablero[i][col] != 0:
                usados.add(tablero[i][col])
        
        sub_fila = (fila // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_fila, sub_fila + 3):
            for j in range(sub_col, sub_col + 3):
                if tablero[i][j] != 0:
                    usados.add(tablero[i][j])
        
        posibles = [num for num in range(1, 10) if num not in usados]
        return posibles
    
    def inicializar_aleatorio(self, tablero):
        """Llena las celdas vacías con números aleatorios válidos por fila"""
        tablero_lleno = copy.deepcopy(tablero)
        
        for i in range(9):
            fila = tablero_lleno[i]
            vacios_fila = [j for j, val in enumerate(fila) if val == 0]
            numeros_usados = [val for val in fila if val != 0]
            numeros_disponibles = [num for num in range(1, 10) if num not in numeros_usados]
            
            # Asignar números aleatorios a las celdas vacías de la fila
            random.shuffle(numeros_disponibles)
            for idx, j in enumerate(vacios_fila):
                if idx < len(numeros_disponibles):
                    tablero_lleno[i][j] = numeros_disponibles[idx]
        
        return tablero_lleno
    
    def costo_conflictos(self, tablero):
        """Calcula el número de conflictos en filas, columnas y subcuadrículas"""
        conflictos = 0
        
        # Conflictos en filas
        for i in range(9):
            for j in range(9):
                num = tablero[i][j]
                if num != 0:
                    # Revisar conflictos en fila
                    for k in range(j + 1, 9):
                        if tablero[i][k] == num:
                            conflictos += 1
                    # Revisar conflictos en columna
                    for k in range(i + 1, 9):
                        if tablero[k][j] == num:
                            conflictos += 1
        
        # Conflictos en subcuadrículas 3x3
        for sub_i in range(3):
            for sub_j in range(3):
                sub_cuad = []
                for i in range(sub_i*3, sub_i*3 + 3):
                    for j in range(sub_j*3, sub_j*3 + 3):
                        sub_cuad.append(tablero[i][j])
                
                for k in range(len(sub_cuad)):
                    if sub_cuad[k] != 0:
                        for l in range(k + 1, len(sub_cuad)):
                            if sub_cuad[l] == sub_cuad[k]:
                                conflictos += 1
        
        return conflictos
    
    def generar_vecino_aleatorio(self, tablero):
        """Genera un vecino intercambiando dos números en la misma fila"""
        vecino = copy.deepcopy(tablero)
        
        # Seleccionar una fila aleatoria
        fila = random.randint(0, 8)
        
        # Encontrar celdas que no sean fijas (que originalmente estaban vacías)
        celdas_cambiables = []
        for j in range(9):
            if self.tablero_inicial[fila][j] == 0:
                celdas_cambiables.append(j)
        
        if len(celdas_cambiables) >= 2:
            # Intercambiar dos celdas de la misma fila
            j1, j2 = random.sample(celdas_cambiables, 2)
            vecino[fila][j1], vecino[fila][j2] = vecino[fila][j2], vecino[fila][j1]
        
        return vecino
    
    def resolver(self):
        """Resuelve Sudoku usando Recocido Simulado"""
        actual = self.inicializar_aleatorio(self.tablero_inicial)
        costo_actual = self.costo_conflictos(actual)
        
        mejor = copy.deepcopy(actual)
        costo_mejor = costo_actual
        
        temperatura = self.temperatura
        
        for iteracion in range(self.iteraciones):
            # Generar vecino
            vecino = self.generar_vecino_aleatorio(actual)
            costo_vecino = self.costo_conflictos(vecino)
            
            # Decidir si aceptar el vecino
            delta = costo_vecino - costo_actual
            
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                actual = vecino
                costo_actual = costo_vecino
                
                if costo_actual < costo_mejor:
                    mejor = copy.deepcopy(actual)
                    costo_mejor = costo_actual
            
            # Enfriar
            temperatura *= self.enfriamiento
            
            # Si se alcanza solución perfecta, terminar
            if costo_mejor == 0:
                break
            
            self.iteraciones_realizadas = iteracion + 1
        
        self.costo_final = costo_mejor
        return mejor if costo_mejor == 0 else None


# ==================== FUNCIONES DE PRUEBA ====================

def generar_sudoku_desde_vacios(base, num_vacios):
    """Genera un Sudoku con cierto número de celdas vacías"""
    sudoku = copy.deepcopy(base)
    vacios = []
    for i in range(9):
        for j in range(9):
            vacios.append((i, j))
    
    random.shuffle(vacios)
    for k in range(num_vacios):
        i, j = vacios[k]
        sudoku[i][j] = 0
    
    return sudoku

def imprimir_sudoku(tablero, titulo=""):
    """Imprime un Sudoku de forma legible"""
    if titulo:
        print(titulo)
    print("+-------+-------+-------+")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("+-------+-------+-------+")
        for j in range(9):
            if j % 3 == 0:
                print("|", end=" ")
            val = tablero[i][j]
            print(val if val != 0 else ".", end=" ")
        print("|")
    print("+-------+-------+-------+")

def ejecutar_prueba(sudoku_inicial, nivel, algoritmo, parametros=None):
    """Ejecuta una prueba con el algoritmo especificado"""
    print(f"\n{'='*60}")
    print(f"Nivel: {nivel} | Algoritmo: {algoritmo}")
    print('='*60)
    
    tracemalloc.start()
    inicio_tiempo = time.time()
    
    if algoritmo == "A*":
        solver = SudokuAStar(sudoku_inicial, heuristica='conflictos')
        solucion = solver.resolver()
        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
        
        tiempo = time.time() - inicio_tiempo
        
        if solucion:
            estado_final = solucion[-1]
            es_valida = SudokuAStar(sudoku_inicial).es_solucion(estado_final)
            
            print(f"✓ Solución encontrada")
            print(f"  • Nodos explorados: {solver.nodos_explorados}")
            print(f"  • Tiempo: {tiempo:.4f} segundos")
            print(f"  • Memoria pico: {memoria_pico / 1024:.2f} KB")
            print(f"  • Válida: {'Sí' if es_valida else 'No'}")
            return {
                'exito': True,
                'nodos': solver.nodos_explorados,
                'tiempo': tiempo,
                'memoria': memoria_pico / 1024,
                'valida': es_valida
            }
        else:
            print("✗ No se encontró solución")
            return {
                'exito': False,
                'nodos': solver.nodos_explorados,
                'tiempo': tiempo,
                'memoria': memoria_pico / 1024,
                'valida': False
            }
    
    elif algoritmo == "Recocido Simulado":
        temp_inicial = parametros.get('temp', 100) if parametros else 100
        enfriamiento = parametros.get('enfriamiento', 0.99) if parametros else 0.99
        iteraciones = parametros.get('iteraciones', 50000) if parametros else 50000
        
        solver = SudokuSimulatedAnnealing(
            sudoku_inicial, 
            temperatura_inicial=temp_inicial,
            enfriamiento=enfriamiento,
            iteraciones=iteraciones
        )
        solucion = solver.resolver()
        memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
        
        tiempo = time.time() - inicio_tiempo
        
        if solucion:
            es_valida = SudokuAStar(sudoku_inicial).es_solucion(solucion)
            
            print(f"✓ Solución encontrada")
            print(f"  • Iteraciones: {solver.iteraciones_realizadas}")
            print(f"  • Costo final: {solver.costo_final}")
            print(f"  • Tiempo: {tiempo:.4f} segundos")
            print(f"  • Memoria pico: {memoria_pico / 1024:.2f} KB")
            print(f"  • Válida: {'Sí' if es_valida else 'No'}")
            return {
                'exito': True,
                'iteraciones': solver.iteraciones_realizadas,
                'tiempo': tiempo,
                'memoria': memoria_pico / 1024,
                'valida': es_valida
            }
        else:
            print(f"✗ No se encontró solución")
            print(f"  • Iteraciones: {solver.iteraciones_realizadas}")
            print(f"  • Costo final: {solver.costo_final}")
            print(f"  • Tiempo: {tiempo:.4f} segundos")
            print(f"  • Memoria pico: {memoria_pico / 1024:.2f} KB")
            return {
                'exito': False,
                'iteraciones': solver.iteraciones_realizadas,
                'tiempo': tiempo,
                'memoria': memoria_pico / 1024,
                'valida': False
            }
    
    tracemalloc.stop()

def mostrar_tabla_comparativa(resultados):
    """Muestra una tabla comparativa de resultados"""
    print("\n" + "="*100)
    print("TABLA COMPARATIVA DE RENDIMIENTO")
    print("="*100)
    
    print(f"{'Nivel':<15} {'Algoritmo':<20} {'Éxito':<8} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Nodos/Iter':<15} {'Válida':<8}")
    print("-"*100)
    
    for resultado in resultados:
        nivel = resultado['nivel']
        algoritmo = resultado['algoritmo']
        exito = "✓" if resultado['exito'] else "✗"
        tiempo = f"{resultado['tiempo']:.4f}"
        memoria = f"{resultado['memoria']:.2f}"
        
        if algoritmo == "A*":
            nodos = resultado.get('nodos', 'N/A')
            nodos_str = f"{nodos}"
        else:
            iteraciones = resultado.get('iteraciones', 'N/A')
            nodos_str = f"{iteraciones}"
        
        valida = "✓" if resultado.get('valida', False) else "✗"
        
        print(f"{nivel:<15} {algoritmo:<20} {exito:<8} {tiempo:<12} {memoria:<15} {nodos_str:<15} {valida:<8}")
    
    print("="*100)

# ==================== MAIN ====================

if __name__ == "__main__":
    # Sudoku base resuelto (para generar instancias)
    sudoku_base = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    # Niveles de dificultad
    niveles = {
        "Fácil (20 vacíos)": 20,
        "Intermedio (35 vacíos)": 35,
        "Difícil (45 vacíos)": 45
    }
    
    resultados = []
    
    # Semilla para reproducibilidad
    random.seed(42)
    
    # Probar cada nivel con ambos algoritmos
    for nombre_nivel, num_vacios in niveles.items():
        # Generar Sudoku con el nivel de dificultad
        sudoku_prueba = generar_sudoku_desde_vacios(sudoku_base, num_vacios)
        
        print(f"\nSudoku generado para {nombre_nivel}:")
        imprimir_sudoku(sudoku_prueba)
        
        # Probar A*
        resultado_a = ejecutar_prueba(sudoku_prueba, nombre_nivel, "A*")
        resultado_a['nivel'] = nombre_nivel
        resultado_a['algoritmo'] = "A*"
        resultados.append(resultado_a)
        
        # Probar Recocido Simulado
        # Ajustar parámetros según dificultad
        if num_vacios <= 20:
            params = {'temp': 100, 'enfriamiento': 0.99, 'iteraciones': 20000}
        elif num_vacios <= 35:
            params = {'temp': 150, 'enfriamiento': 0.995, 'iteraciones': 50000}
        else:
            params = {'temp': 200, 'enfriamiento': 0.998, 'iteraciones': 100000}
        
        resultado_rs = ejecutar_prueba(sudoku_prueba, nombre_nivel, "Recocido Simulado", params)
        resultado_rs['nivel'] = nombre_nivel
        resultado_rs['algoritmo'] = "Recocido Simulado"
        resultados.append(resultado_rs)
    
    # Mostrar tabla comparativa
    mostrar_tabla_comparativa(resultados)
    
    
