"""
Script de Pruebas - Tic Tac Toe 4x4 Minimax
Este archivo contiene ejemplos y pruebas del funcionamiento de los algoritmos
"""

from tictactoe_server import TicTacToe4x4
import time

def print_board(board):
    """Imprime el tablero de forma visual"""
    print("\n  0 1 2 3")
    for row in range(4):
        print(f"{row} ", end="")
        for col in range(4):
            val = board[row][col]
            if val == 1:
                print("✕ ", end="")
            elif val == -1:
                print("◯ ", end="")
            else:
                print(". ", end="")
        print()
    print()

def test_heuristic():
    """Prueba la función heurística"""
    print("=" * 60)
    print("PRUEBA 1: Función Heurística")
    print("=" * 60)
    
    game = TicTacToe4x4()
    
    # Test 1: Tablero vacío
    print("\n1. Tablero vacío:")
    print_board(game.board)
    score = game.evaluate_heuristic(game.ai)
    print(f"Evaluación: {score} (debe ser cercano a 0)")
    
    # Test 2: IA con 3 fichas en línea + espacio
    print("\n2. IA con 3 fichas horizontales + espacio:")
    game.reset()
    game.board[0][0] = -1
    game.board[0][1] = -1
    game.board[0][2] = -1
    game.board[0][3] = 0
    print_board(game.board)
    score = game.evaluate_heuristic(game.ai)
    print(f"Evaluación: {score} (debe ser ALTO, ~500+)")
    
    # Test 3: Control del centro
    print("\n3. IA controla el centro (todas las posiciones centrales):")
    game.reset()
    game.board[1][1] = -1
    game.board[1][2] = -1
    game.board[2][1] = -1
    game.board[2][2] = -1
    print_board(game.board)
    score = game.evaluate_heuristic(game.ai)
    print(f"Evaluación: {score} (debe incluir +120 por control del centro)")
    
    # Test 4: Defensa necesaria
    print("\n4. Humano con 3 fichas en línea + espacio (debe defenderse):")
    game.reset()
    game.board[1][1] = 1
    game.board[1][2] = 1
    game.board[1][3] = 1
    game.board[1][0] = 0
    print_board(game.board)
    score = game.evaluate_heuristic(game.ai)
    print(f"Evaluación: {score} (debe ser negativo o incluir +400 de bloqueo)")

def test_minimax_vs_alphabeta():
    """Compara Minimax vs Alpha-Beta"""
    print("\n" + "=" * 60)
    print("PRUEBA 2: Minimax vs Alpha-Beta")
    print("=" * 60)
    
    game = TicTacToe4x4()
    
    # Setup inicial: algunos movimientos
    print("\nConfigurando posición inicial...")
    game.board[0][0] = 1      # Humano
    game.board[1][1] = 1      # Humano
    game.board[2][2] = -1     # IA
    
    print_board(game.board)
    
    # Prueba Minimax
    print("\n📊 Evaluando con MINIMAX (sin poda)...")
    print("-" * 60)
    
    game.nodes_explored_minimax = 0
    start_time = time.time()
    score_mm, move_mm = game.minimax(0, True, max_depth=3)
    time_mm = time.time() - start_time
    nodes_mm = game.nodes_explored_minimax
    
    print(f"Mejor movimiento: {move_mm}")
    print(f"Evaluación: {score_mm}")
    print(f"Nodos explorados: {nodes_mm:,}")
    print(f"Tiempo: {time_mm:.4f}s")
    
    # Prueba Alpha-Beta
    print("\n📊 Evaluando con ALPHA-BETA (con poda)...")
    print("-" * 60)
    
    game.nodes_explored_alphabeta = 0
    start_time = time.time()
    score_ab, move_ab = game.minimax_alphabeta(0, float('-inf'), float('inf'), True, max_depth=3)
    time_ab = time.time() - start_time
    nodes_ab = game.nodes_explored_alphabeta
    
    print(f"Mejor movimiento: {move_ab}")
    print(f"Evaluación: {score_ab}")
    print(f"Nodos explorados: {nodes_ab:,}")
    print(f"Tiempo: {time_ab:.4f}s")
    
    # Comparación
    print("\n📈 COMPARACIÓN:")
    print("-" * 60)
    print(f"Movimientos iguales: {'✓ Sí' if move_mm == move_ab else '✗ No'}")
    print(f"Evaluaciones iguales: {'✓ Sí' if score_mm == score_ab else '✗ No'}")
    
    reduction = (1 - nodes_ab / nodes_mm) * 100 if nodes_mm > 0 else 0
    speedup = time_mm / time_ab if time_ab > 0 else 0
    
    print(f"\nNodos explorados:")
    print(f"  Minimax:    {nodes_mm:,}")
    print(f"  Alpha-Beta: {nodes_ab:,}")
    print(f"  Reducción:  {reduction:.1f}%")
    
    print(f"\nTiempo de ejecución:")
    print(f"  Minimax:    {time_mm:.4f}s")
    print(f"  Alpha-Beta: {time_ab:.4f}s")
    print(f"  Speedup:    {speedup:.2f}x")

def test_game_flow():
    """Prueba un flujo de juego completo"""
    print("\n" + "=" * 60)
    print("PRUEBA 3: Flujo de Juego Completo")
    print("=" * 60)
    
    game = TicTacToe4x4()
    move_count = 0
    
    print("\nJuego: Humano vs IA (Alpha-Beta)")
    print("Humano es ✕, IA es ◯\n")
    
    # Simulación de algunos movimientos
    moves_humano = [(0, 0), (0, 2), (1, 1)]
    
    for idx, (row, col) in enumerate(moves_humano):
        move_count += 1
        print(f"--- MOVIMIENTO {move_count} ---")
        print(f"Movimiento humano: ({row}, {col})")
        
        game.make_move(row, col, game.human)
        
        winner = game.check_winner()
        if winner != 0:
            print("¡Ganó el humano!")
            print_board(game.board)
            break
        
        if game.is_board_full():
            print("¡Empate!")
            break
        
        print("Turno IA...")
        game.nodes_explored_alphabeta = 0
        score, ai_move = game.minimax_alphabeta(0, float('-inf'), float('inf'), True, max_depth=3)
        
        if ai_move:
            game.make_move(ai_move[0], ai_move[1], game.ai)
            print(f"Movimiento IA: {ai_move}")
            print(f"Nodos explorados: {game.nodes_explored_alphabeta:,}")
        
        print_board(game.board)
        
        winner = game.check_winner()
        if winner == game.ai:
            print("¡Ganó la IA!")
            break
        
        if game.is_board_full():
            print("¡Empate!")
            break
        
        if idx < len(moves_humano) - 1:
            print()

def test_performance():
    """Prueba de rendimiento con diferentes profundidades"""
    print("\n" + "=" * 60)
    print("PRUEBA 4: Análisis de Rendimiento")
    print("=" * 60)
    
    game = TicTacToe4x4()
    
    # Setup
    game.board[1][1] = 1
    game.board[1][2] = -1
    
    print("\nMidiendo rendimiento a diferentes profundidades...")
    print("\n" + "Profundidad | Minimax Nodos | Alpha-Beta Nodos | Reducción")
    print("-" * 60)
    
    for depth in range(1, 5):
        # Minimax
        game.nodes_explored_minimax = 0
        game.minimax(0, True, max_depth=depth)
        nodes_mm = game.nodes_explored_minimax
        
        # Alpha-Beta
        game.nodes_explored_alphabeta = 0
        game.minimax_alphabeta(0, float('-inf'), float('inf'), True, max_depth=depth)
        nodes_ab = game.nodes_explored_alphabeta
        
        reduction = (1 - nodes_ab / nodes_mm) * 100 if nodes_mm > 0 else 0
        
        print(f"    {depth}      |    {nodes_mm:8,}     |    {nodes_ab:8,}      |  {reduction:6.1f}%")

def test_edge_cases():
    """Prueba casos especiales"""
    print("\n" + "=" * 60)
    print("PRUEBA 5: Casos Especiales")
    print("=" * 60)
    
    game = TicTacToe4x4()
    
    # Caso 1: Ganar con 3 fichas
    print("\nCaso 1: Ganar con 3 fichas en línea")
    game.reset()
    game.board[0][0] = -1
    game.board[0][1] = -1
    game.board[0][2] = -1
    
    winner = game.check_winner()
    print(f"Ganador detectado: {winner} (debe ser -1)")
    print_board(game.board)
    
    # Caso 2: Ganar con 4 fichas
    print("Caso 2: Ganar con 4 fichas en línea")
    game.reset()
    game.board[1][0] = 1
    game.board[1][1] = 1
    game.board[1][2] = 1
    game.board[1][3] = 1
    
    winner = game.check_winner()
    print(f"Ganador detectado: {winner} (debe ser 1)")
    print_board(game.board)
    
    # Caso 3: Diagonal
    print("Caso 3: Victoria en diagonal")
    game.reset()
    game.board[0][0] = -1
    game.board[1][1] = -1
    game.board[2][2] = -1
    game.board[3][3] = -1
    
    winner = game.check_winner()
    print(f"Ganador detectado: {winner} (debe ser -1)")
    print_board(game.board)
    
    # Caso 4: Tablero lleno
    print("Caso 4: Tablero lleno (empate)")
    game.reset()
    for i in range(4):
        for j in range(4):
            game.board[i][j] = 1 if (i + j) % 2 == 0 else -1
    
    is_full = game.is_board_full()
    print(f"Tablero lleno: {is_full} (debe ser True)")
    print_board(game.board)

def main():
    """Ejecuta todas las pruebas"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  TIC TAC TOE 4x4 - SUITE DE PRUEBAS".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        test_heuristic()
        test_minimax_vs_alphabeta()
        test_game_flow()
        test_performance()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
