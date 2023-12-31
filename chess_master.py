import chess
import random
import math
import copy
import time

PIECE_VALUES = {
    'k': -900, 'K': 900,
    'q': -90, 'Q': 90,
    'r': -50, 'R': 50,
    'b': -32, 'B': 32,
    'n': -31,'N': 31,
    'p': -10, 'P': 10
}

# Bot will select a random move
def random_move(board: chess.Board):
    random.seed()
    return str(random.choice(list(board.legal_moves)))

def pseudo_move(board: chess.Board, move=None):
    new_board = copy.copy(board)
    new_board.turn = board.turn
    if move: new_board.push(move)
    return new_board

def eval(board: chess.Board):
    total_moves = len(board.move_stack)
    if board.is_checkmate():
        if board.turn == chess.WHITE: return (-1000 + total_moves)
        else: return (1000 - total_moves)
    if board.is_check():
        if board.turn == chess.WHITE: return -.3
        else: return .3
    if board.outcome(): return 0.0
    fen = board.board_fen()
    '''
    score = 0
    for x in fen:
        if x in PIECE_VALUES: score += PIECE_VALUES[x]
    '''
    wRook = fen.count('R')
    wKnight = fen.count('N')
    wQueen = fen.count('Q')
    wBishop = fen.count('B')
    wPawn = fen.count('P')
    bRook = fen.count('r')
    bKnight = fen.count('n')
    bQueen = fen.count('q')
    bBishop = fen.count('b')
    bPawn = fen.count('p')
    whiteValue = 50 * wRook + 31 * wKnight + 90 * wQueen + 32 * wBishop + 10 * wPawn
    blackValue = 50 * bRook + 31 * bKnight + 90 * bQueen + 32 * bBishop + 10 * bPawn
    return (whiteValue - blackValue) / 10

def get_piece_val(piece: chess.Piece):
    if not piece: return 0
    return PIECE_VALUES[piece.symbol()]

def sort_moves(board: chess.Board):
    legal_moves = list(board.legal_moves)
    if not legal_moves: return []
    move_estimates = []
    for move in legal_moves:
        estimate = 0
        '''
        if board.is_capture(move):
            start = board.piece_at(chess.parse_square(str(move)[0:2]))
            target = board.piece_at(chess.parse_square(str(move)[2:4]))
            estimate += get_piece_val(target) + get_piece_val(start)
        '''
        if board.is_capture(move): estimate += 1
        if board.is_into_check(move): estimate += 1
        move_estimates.append((estimate, move))
    # Sort moves by their estimated value
    move_estimates.sort(reverse=True, key=lambda x: x[0])
    # Extract the moves from this list
    move_estimates = [x[1] for x in move_estimates]
    return move_estimates
'''
def minimax(board: chess.Board):
    max_depth = 5
    turn = board.turn
    if turn == chess.WHITE: best_score = -math.inf
    else: best_score = math.inf
    best_move = list(board.legal_moves)[0]
    start_time = time.time()
    for move in list(board.legal_moves):
        if turn == chess.WHITE:
            move_score = mini(pseudo_move(board, move), max_depth, -math.inf, math.inf)
            if move_score > best_score:
                best_move = move
                best_score = move_score
        else:
            move_score = maxi(pseudo_move(board, move), max_depth, -math.inf, math.inf)
            #print(move_score, move)
            if move_score < best_score:
                best_move = move
                best_score = move_score
    
    total_time = round(time.time() - start_time, 3)
    # CODE KNOWS EVAL IS BAD BUT STILL PLAYS???
    print(f'Minimax w/ alpha beta pruning\nDepth: {max_depth}\nTime taken: {total_time} seconds\nEvaluation: {best_score}')
    return str(best_move)

def mini(board: chess.Board, depth: int, alpha, beta):
    if not depth: return eval(board)
    best_val = math.inf
    board.turn = chess.BLACK
    for move in list(board.legal_moves):
        score = maxi(pseudo_move(board, move), depth - 1, alpha, beta)
        best_val = min(best_val, score)
        beta = min(beta, best_val)
        if beta <= alpha or best_val == -math.inf: break
    return best_val

def maxi(board: chess.Board, depth, alpha, beta):
    if not depth: return eval(board)
    best_val = -math.inf
    board.turn = chess.WHITE
    for move in list(board.legal_moves):
        score = mini(pseudo_move(board, move), depth - 1, alpha, beta)
        best_val = max(best_val, score)
        alpha = max(alpha, best_val)
        if beta <= alpha or best_val == math.inf: break

    return best_val
'''

def minimax(board: chess.Board):
    max_depth = 5
    start_time = time.time()
    if board.turn == chess.WHITE:
        best_move = maxi(board, max_depth, -math.inf, math.inf)
    else:
        best_move = mini(board, max_depth, -math.inf, math.inf)
    
    total_time = round(time.time() - start_time, 3)
    print(f'Minimax w/ AB pruning\nDepth: {max_depth}\nTime taken: {total_time} seconds\nEvaluation: {best_move[0]}')
    return str(best_move[1])

# mini() and maxi() return (best_eval, best_move) from position
def mini(board: chess.Board, depth: int, alpha, beta):
    board.turn = chess.BLACK
    if not depth or not board.legal_moves:
        # TODO: check for free capture
        return (eval(board), board.pop())
    best_val = (math.inf, list(board.legal_moves)[0])
    sorted_moves = sort_moves(board)
    for move in sorted_moves:
        if move not in list(board.legal_moves): continue
        score = (maxi(pseudo_move(board, move), depth - 1, alpha, beta)[0], move)
        best_val = min([best_val, score], key = lambda t: t[0])
        beta = min(beta, best_val[0])
        if beta <= alpha: break

    return best_val

def maxi(board: chess.Board, depth: int, alpha, beta):
    if not depth or not board.legal_moves:
        return (eval(board), board.pop())
    best_val = (-math.inf, list(board.legal_moves)[0])
    sorted_moves = sort_moves(board)
    for move in sorted_moves:
        if move not in list(board.legal_moves): continue
        score = (mini(pseudo_move(board, move), depth - 1, alpha, beta)[0], move)
        best_val = max([best_val, score], key = lambda t: t[0])
        alpha = max(alpha, best_val[0])
        if beta <= alpha: break
    return best_val

# Allows human player to make moves through the terminal
def terminal_player(board):
    while True:
        move = input('Your move:\n')
        realmove = chess.Move.from_uci(move)
        #print(map(make_string, list(board.legal_moves)))
        if realmove in list(board.legal_moves):
            return move
        print(f'"{move}" is an invalid move. Try again.')

class BotGame:
    def __init__(self, white_func, black_func, pygame_player=None):
        self.board = chess.Board()
        self.white_func = white_func
        self.black_func = black_func
        self.pygame_player = pygame_player
        self.outcome = 'N/A'
    

    # is_over(): Returns true if the game has ended and false otherwise. Will also store the outcome once the game has ended.
    def is_over(self):
        if self.board.outcome():
            print(f"FINAL GAME STATE:\n{self.board}")
            self.outcome = self.board.outcome()
            print(self.outcome)
            return True
        else: return False


    # white_move(): Plays the move the player with the white pieces will make
    def white_move(self):
        move = self.white_func(self.board)
        capture = self.board.is_capture(chess.Move.from_uci(move))
        self.board.push_uci(move)
        check = self.board.is_check()

        print(f'White played the move {move}.\n')
        if check: return 'check'
        if capture: return 'cap'
        return 'nocap'
    

    # black_move(): Plays the move the player with the black pieces will make
    def black_move(self):
        move = self.black_func(self.board)
        capture = self.board.is_capture(chess.Move.from_uci(move))
        self.board.push_uci(move)
        check = self.board.is_check()

        print(f'Black played the move {move}.\n')
        if check: return 'check'
        if capture: return 'cap'
        return 'nocap'
    

    # manual_move(uci): Input a move manually into the game
    def manual_move(self, uci):
        capture = self.board.is_capture(chess.Move.from_uci(uci))
        self.board.push_uci(uci)
        check = self.board.is_check()

        print(f'Manually played the move {uci}.\n')
        if check: return 'check'
        if capture: return 'cap'
        return 'nocap'


        

# game loop testing
'''
game = BotGame(random_move, terminal_player)
turn = 'w'
print(game.board._board_state)
while not game.is_over():
    print(game.board)
    print('\n')
    if turn == 'b':
        game.black_move()
    else:
        game.white_move()
    turn = 'b' if turn == 'w' else 'w'

print(game.outcome)
'''