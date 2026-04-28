from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

class TicTacToe4x4:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.human = 1
        self.ai = -1
        self.nodes_explored_minimax = 0
        self.nodes_explored_alphabeta = 0
    
    def reset(self):
        """Reinicia el tablero"""
        self.board = [[0] * 4 for _ in range(4)]
        self.nodes_explored_minimax = 0
        self.nodes_explored_alphabeta = 0
    
    def get_board_state(self):
        """Retorna el estado actual del tablero"""
        return self.board
    
    def is_valid_move(self, row, col):
        """Verifica si un movimiento es válido"""
        return 0 <= row < 4 and 0 <= col < 4 and self.board[row][col] == 0
    
    def get_available_moves(self):
        moves = []
        center = [(1,1),(1,2),(2,1),(2,2)]

        # Primero centro
        for r,c in center:
            if self.board[r][c] == 0:
                moves.append((r,c))

        # Luego resto
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0 and (i,j) not in center:
                    moves.append((i,j))

        return moves
    
    def make_move(self, row, col, player):
        """Realiza un movimiento"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def undo_move(self, row, col):
        """Deshace un movimiento"""
        self.board[row][col] = 0
    
    def check_winner(self):
        """Verifica si hay un ganador (1: humano, -1: IA, 0: sin ganador)"""
        # Filas
        for i in range(4):
            if all(self.board[i][j] == 1 for j in range(4)):
                return 1
            if all(self.board[i][j] == -1 for j in range(4)):
                return -1

        # Columnas
        for j in range(4):
            if all(self.board[i][j] == 1 for i in range(4)):
                return 1
            if all(self.board[i][j] == -1 for i in range(4)):
                return -1

        # Diagonales
        if all(self.board[i][i] == 1 for i in range(4)):
            return 1
        if all(self.board[i][i] == -1 for i in range(4)):
            return -1

        if all(self.board[i][3-i] == 1 for i in range(4)):
            return 1
        if all(self.board[i][3-i] == -1 for i in range(4)):
            return -1
        return 0
    
    def is_board_full(self):
        """Verifica si el tablero está lleno"""
        return len(self.get_available_moves()) == 0
    
    def evaluate_heuristic(self, player):
        score = 0

        lines = []

        # Filas
        for i in range(4):
            lines.append(self.board[i])

        # Columnas
        for j in range(4):
            lines.append([self.board[i][j] for i in range(4)])

        # Diagonales
        lines.append([self.board[i][i] for i in range(4)])
        lines.append([self.board[i][3 - i] for i in range(4)])

        def evaluate_line(line):
            p = line.count(player)
            o = line.count(-player)

            if o == 0:
                if p == 4:
                    return 1000
                elif p == 3:
                    return 800
                elif p == 2:
                    return 50
            elif p == 0:
                if o == 4:
                    return -1000
                elif o == 3:
                    return -400
                elif o == 2:
                    return -40

            return 0

        for line in lines:
            score += evaluate_line(line)

        # Centro
        center = [(1,1),(1,2),(2,1),(2,2)]
        for r,c in center:
            if self.board[r][c] == player:
                score += 30
            elif self.board[r][c] == -player:
                score -= 30

        return score
    
    def minimax(self, depth, is_maximizing, max_depth=4):
        """
        Algoritmo Minimax sin poda Alfa-Beta
        """
        self.nodes_explored_minimax += 1
        
        winner = self.check_winner()
        if winner == self.ai:
            return 10000 - depth, None
        elif winner == self.human:
            return -10000 + depth, None
        elif self.is_board_full():
            return 0, None
        elif depth >= max_depth:
            return self.evaluate_heuristic(self.ai), None
        
        available_moves = self.get_available_moves()
        if not available_moves:
            return 0, None
        
        best_move = None
        
        if is_maximizing:  # IA juega
            max_eval = float('-inf')
            for row, col in available_moves:
                self.make_move(row, col, self.ai)
                eval_score, _ = self.minimax(depth + 1, False, max_depth)
                self.undo_move(row, col)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (row, col)
            
            return max_eval, best_move
        else:  # Humano juega
            min_eval = float('inf')
            for row, col in available_moves:
                self.make_move(row, col, self.human)
                eval_score, _ = self.minimax(depth + 1, True, max_depth)
                self.undo_move(row, col)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (row, col)
            
            return min_eval, best_move
    
    def minimax_alphabeta(self, depth, alpha, beta, is_maximizing, max_depth=4):
        """
        Algoritmo Minimax con poda Alfa-Beta
        """
        self.nodes_explored_alphabeta += 1
        
        winner = self.check_winner()
        if winner == self.ai:
            return 10000 - depth, None
        elif winner == self.human:
            return -10000 + depth, None
        elif self.is_board_full():
            return 0, None
        elif depth >= max_depth:
            return self.evaluate_heuristic(self.ai), None
        
        available_moves = self.get_available_moves()
        if not available_moves:
            return 0, None
        
        best_move = None
        
        if is_maximizing:  # IA juega
            max_eval = float('-inf')
            for row, col in available_moves:
                self.make_move(row, col, self.ai)
                eval_score, _ = self.minimax_alphabeta(depth + 1, alpha, beta, False, max_depth)
                self.undo_move(row, col)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (row, col)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda
            
            return max_eval, best_move
        else:  # Humano juega
            min_eval = float('inf')
            for row, col in available_moves:
                self.make_move(row, col, self.human)
                eval_score, _ = self.minimax_alphabeta(depth + 1, alpha, beta, True, max_depth)
                self.undo_move(row, col)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (row, col)
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda
            
            return min_eval, best_move
    
    def get_ai_move(self, use_alphabeta=True):
        """Obtiene el mejor movimiento de la IA"""
        if use_alphabeta:
            self.nodes_explored_alphabeta = 0
            _, best_move = self.minimax_alphabeta(0, float('-inf'), float('inf'), True, max_depth=5)
            return best_move, self.nodes_explored_alphabeta
        else:
            self.nodes_explored_minimax = 0
            _, best_move = self.minimax(0, True, max_depth=5)
            return best_move, self.nodes_explored_minimax

# Instancia global
game = TicTacToe4x4()

@app.route('/')
def serve_index():
    """Sirve la página principal"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return '''
        <html>
        <head><title>Tic Tac Toe 4x4</title></head>
        <body>
        <h1>Tic Tac Toe 4x4 - Servidor Iniciado</h1>
        <p>Error cargando index.html. Asegúrate de que el archivo existe en el directorio actual.</p>
        <p>Acceso a API: <a href="/api/game/state">GET /api/game/state</a></p>
        </body>
        </html>
        '''

@app.route('/api/game/state', methods=['GET'])
def get_state():
    """Obtiene el estado actual del juego"""
    return jsonify({
        'board': game.board,
        'game_over': game.check_winner() != 0 or game.is_board_full(),
        'winner': game.check_winner()
    })

@app.route('/api/game/move', methods=['POST'])
def make_player_move():
    """Realiza un movimiento del jugador"""
    data = request.json
    row, col = data['row'], data['col']
    
    if not game.is_valid_move(row, col):
        return jsonify({'success': False, 'error': 'Movimiento inválido'}), 400
    
    game.make_move(row, col, game.human)
    
    # Verificar si el humano ganó
    winner = game.check_winner()
    if winner == game.human:
        return jsonify({
            'success': True,
            'board': game.board,
            'game_over': True,
            'winner': game.human
        })
    
    if game.is_board_full():
        return jsonify({
            'success': True,
            'board': game.board,
            'game_over': True,
            'winner': 0
        })
    
    # Turno de la IA
    use_alphabeta = data.get('use_alphabeta', True)
    ai_move, nodes_explored = game.get_ai_move(use_alphabeta)
    
    if ai_move:
        game.make_move(ai_move[0], ai_move[1], game.ai)
        
        winner = game.check_winner()
        is_game_over = winner != 0 or game.is_board_full()
        
        return jsonify({
            'success': True,
            'board': game.board,
            'ai_move': {'row': ai_move[0], 'col': ai_move[1]},
            'nodes_explored': nodes_explored,
            'algorithm': 'Alpha-Beta' if use_alphabeta else 'Minimax',
            'game_over': is_game_over,
            'winner': winner
        })
    
    return jsonify({
        'success': True,
        'board': game.board,
        'game_over': True,
        'winner': 0
    })

@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    """Reinicia el juego"""
    game.reset()
    return jsonify({'success': True, 'board': game.board})

@app.route('/api/game/analyze', methods=['POST'])
def analyze_move():
    """Analiza un movimiento con ambos algoritmos"""
    data = request.json
    row, col = data['row'], data['col']
    
    if not game.is_valid_move(row, col):
        return jsonify({'success': False, 'error': 'Movimiento inválido'}), 400
    
    game.make_move(row, col, game.human)
    
    # Minimax
    game.nodes_explored_minimax = 0
    _, move_minimax = game.minimax(0, True, max_depth=6)
    nodes_minimax = game.nodes_explored_minimax
    
    # Alpha-Beta
    game.nodes_explored_alphabeta = 0
    _, move_alphabeta = game.minimax_alphabeta(0, float('-inf'), float('inf'), True, max_depth=6)
    nodes_alphabeta = game.nodes_explored_alphabeta
    
    game.undo_move(row, col)
    
    return jsonify({
        'success': True,
        'minimax': {
            'nodes_explored': nodes_minimax,
            'best_move': move_minimax
        },
        'alphabeta': {
            'nodes_explored': nodes_alphabeta,
            'best_move': move_alphabeta
        },
        'reduction': f"{(1 - nodes_alphabeta/nodes_minimax) * 100:.1f}%" if nodes_minimax > 0 else "0%"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
