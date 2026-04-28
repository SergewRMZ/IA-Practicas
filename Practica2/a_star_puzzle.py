import heapq
import time
import tracemalloc

class Puzzle:
    # Estado inicial arreglo, objetivo []. casillas, función lambda
    def __init__(self, estado, objetivo, n, heuristica):
        self.estado = estado
        self.objetivo = objetivo
        self.n = n
        self.heuristica = heuristica
        self.nodos_explorados = 0

    def get_vecinos(self, estado):
        vecinos = []
        i = estado.index(0)
        fila, col = divmod(i, self.n)
        # (fila, columna)
        movimientos = [(-1,0),(1,0),(0,-1),(0,1)]

        for df, dc in movimientos:
            nf, nc = fila + df, col + dc
            if 0 <= nf < self.n and 0 <= nc < self.n:
                nuevo = list(estado) # Convierte la tupla estado en una lista.
                ni = nf * self.n + nc # Convierte una posición fila columna a un índice de lista
                nuevo[i], nuevo[ni] = nuevo[ni], nuevo[i]
                vecinos.append(tuple(nuevo)) # Convierte la lista "nuevo" en una tupla y la agrega

        return vecinos

    def resolver(self):
        inicio = tuple(self.estado)
        objetivo = tuple(self.objetivo)

        abiertos = []
        heapq.heappush(abiertos, (0, inicio))

        g = {inicio: 0}
        padre = {inicio: None}

        while abiertos:
            _, actual = heapq.heappop(abiertos)
            self.nodos_explorados += 1

            if actual == objetivo:
                return self.reconstruir_camino(padre, actual)

            for vecino in self.get_vecinos(actual):
                nuevo_g = g[actual] + 1

                if vecino not in g or nuevo_g < g[vecino]:
                    g[vecino] = nuevo_g
                    f = nuevo_g + self.heuristica(vecino)
                    heapq.heappush(abiertos, (f, vecino))
                    padre[vecino] = actual

        return None

    def reconstruir_camino(self, padre, estado):
        camino = []
        while estado:
            camino.append(estado)
            estado = padre[estado]
        return camino[::-1]


# ---------------- HEURÍSTICAS ----------------

def h_fuera_de_lugar(estado, objetivo):
    fuera = 0
    for i in range(len(estado)):
        if estado[i] != 0 and estado[i] != objetivo[i]:
            fuera += 1
    return fuera


def h_manhattan(estado, objetivo, n):
    distancia = 0
    for i in range(len(estado)):
        valor = estado[i]
        if valor != 0:
            fila_actual, col_actual = divmod(i, n)
            indice_obj = objetivo.index(valor)
            fila_obj, col_obj = divmod(indice_obj, n)
            distancia += abs(fila_actual - fila_obj) + abs(col_actual - col_obj)
    return distancia

def h_personalizada_conflictos(estado, objetivo, n):
    # Primero calculamos Manhattan base
    distancia = h_manhattan(estado, objetivo, n)
    conflictos = 0

    # Conflictos Horizontales
    for fila in range(n):
        fichas_en_fila = []
        for col in range(n):
            valor = estado[fila * n + col]
            if valor != 0:
                # ¿Este valor pertenece a esta fila en el objetivo?
                indice_obj = objetivo.index(valor)
                if indice_obj // n == fila:
                    fichas_en_fila.append((col, indice_obj % n))
        
        # Revisar si hay fichas cruzadas
        for i in range(len(fichas_en_fila)):
            for j in range(i + 1, len(fichas_en_fila)):
                # Si la ficha i está antes que j, pero su destino está después
                if fichas_en_fila[i][0] < fichas_en_fila[j][0] and \
                   fichas_en_fila[i][1] > fichas_en_fila[j][1]:
                    conflictos += 1

    # Conflictos Verticales
    for col in range(n):
        fichas_en_col = []
        for fila in range(n):
            valor = estado[fila * n + col]
            if valor != 0:
                # ¿Este valor pertenece a esta columna en el objetivo?
                indice_obj = objetivo.index(valor)
                if indice_obj % n == col:
                    fichas_en_col.append((fila, indice_obj // n))
        
        for i in range(len(fichas_en_col)):
            for j in range(i + 1, len(fichas_en_col)):
                if fichas_en_col[i][0] < fichas_en_col[j][0] and \
                   fichas_en_col[i][1] > fichas_en_col[j][1]:
                    conflictos += 1

    # Cada conflicto añade 2 movimientos obligatorios
    return distancia + (2 * conflictos)

def h_propia_vecindad(estado, objetivo, n):
    costo = 0
    for i in range(len(estado)):
        valor = estado[i]
        if valor == 0: continue
        
        # 1. Base: Distancia de Manhattan (porque funciona)
        f_act, c_act = divmod(i, n)
        idx_obj = objetivo.index(valor)
        f_obj, c_obj = divmod(idx_obj, n)
        dist = abs(f_act - f_obj) + abs(c_act - c_obj)
        costo += dist
        
        # 2. "Lógica Propia": El vecino de la derecha
        # Si no estoy en la última columna, miro quién tengo a la derecha
        if c_act < n - 1:
            vecino_derecha = estado[i + 1]
            # Buscamos quién debería estar a la derecha de 'valor' en el objetivo
            if idx_obj + 1 < len(objetivo) and (idx_obj + 1) % n != 0:
                deberia_ser = objetivo[idx_obj + 1]
                if vecino_derecha != deberia_ser and vecino_derecha != 0:
                    costo += 1 # Castigo por no tener al compañero correcto
                    
    return costo

# ---------------- EJECUCIÓN ----------------

def ejecutar_puzzle(inicial, objetivo, n, nombre, heuristica_func):
    print(f"\n--- {nombre} ---")

    puzzle = Puzzle(inicial, objetivo, n, heuristica_func)

    tracemalloc.start()
    inicio_tiempo = time.time()

    solucion = puzzle.resolver()

    fin_tiempo = time.time()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solucion:
        print(f"Movimientos: {len(solucion)-1}")
    else:
        print("Sin solución")

    print(f"Nodos explorados: {puzzle.nodos_explorados}")
    print(f"Tiempo: {fin_tiempo - inicio_tiempo:.6f} segundos")
    print(f"Memoria pico: {memoria_pico / 1024:.2f} KB")
# ---------------- MAIN ----------------

if __name__ == "__main__":

    # -------- 8 PUZZLE --------
    inicial_8 = [8, 6, 7, 2, 5, 4, 3, 0, 1]

    objetivo_8 = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    ]

    # Fuera de lugar
    ejecutar_puzzle(
        inicial_8,
        objetivo_8,
        3,
        "8-Puzzle | Fuera de lugar",
        lambda e: h_fuera_de_lugar(e, objetivo_8)
    )

    # Manhattan
    ejecutar_puzzle(
        inicial_8,
        objetivo_8,
        3,
        "8-Puzzle | Manhattan",
        lambda e: h_manhattan(e, objetivo_8, 3)
    )

    # Personalizada (Manhattan + Linear Conflict)
    # ejecutar_puzzle(
    #     inicial_8,
    #     objetivo_8,
    #     3,
    #     "8-Puzzle | Personalizada (Conflictos)",
    #     lambda e: h_personalizada_conflictos(e, objetivo_8, 3)
    # )

    ejecutar_puzzle(
        inicial_8,
        objetivo_8,
        3,
        "8-Puzzle | Personalizada",
        lambda e: h_propia_vecindad(e, objetivo_8, 3)
    )



    # -------- 15 PUZZLE (caso fácil) --------
    inicial_15 = [
        5, 1, 11, 3,
        13, 9, 0, 4,
        14, 7, 6, 2,
        10, 15, 12, 8
    ]

    objetivo_15 = [
        1, 2, 3, 4,
        5, 6, 7, 8,
        9,10,11,12,
        13,14,15,0
    ]

    # Fuera de lugar
    ejecutar_puzzle(
        inicial_15,
        objetivo_15,
        4,
        "15-Puzzle | Fuera de lugar",
        lambda e: h_fuera_de_lugar(e, objetivo_15)
    )

    # Manhattan
    ejecutar_puzzle(
        inicial_15,
        objetivo_15,
        4,
        "15-Puzzle | Manhattan",
        lambda e: h_manhattan(e, objetivo_15, 4)
    )

    ejecutar_puzzle(
        inicial_15,
        objetivo_15,
        4,
        "15-Puzzle | Personalizada",
        lambda e: h_propia_vecindad(e, objetivo_15, 4)
    )