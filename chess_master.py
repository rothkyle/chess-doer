import chess
import random

# Bot will select a random move
def random_move(board):
    random.seed()
    return str(random.choice(list(board.legal_moves)))



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