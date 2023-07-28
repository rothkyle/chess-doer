import pygame
import chess
import chess_master as cm
import time

pygame.init()
WIDTH = 800
HEIGHT = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (227, 193, 111)
BLACK = (184, 139, 74)
EMPTY_HIGHLIGHTED_COLOR = (50, 100, 100)
PIECE_HIGHLIGHTED_COLOR = (255, 100, 50)
PIECE_IMAGE_SIZE = (WIDTH // COLS, HEIGHT // ROWS)
CAPTURE_SOUND = pygame.mixer.Sound("piece_sounds/capture.mp3")
NO_CAPTURE_SOUND = pygame.mixer.Sound("piece_sounds/nocapture.mp3")
CHECK_SOUND = pygame.mixer.Sound("piece_sounds/check.mp3")

scrn = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load("chess_icon.png"))


# convert board to list so we can iterate over it and place the pieces on top of checkerboard
def make_matrix(board): #type(board) == chess.Board()
    pgn = board.epd()
    foo = []  #Final board
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  #This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo


def update_board(board, highlighted):
    matrix = make_matrix(board)
    # checkerboard pattern
    scrn.fill(BLACK)
    for row in range(ROWS):
        #for col in range(row % 2, ROWS, 2):
        for col in range(COLS):
            if col % 2 == row % 2: pygame.draw.rect(scrn, WHITE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = matrix[row][col]
            if piece != '.':
                piece_color = 'w' if piece.isupper() else 'b'
                piece_img = pygame.image.load(f'piece_imgs/{piece_color}{piece.lower()}.png')
                piece_img = pygame.transform.scale(piece_img, PIECE_IMAGE_SIZE)
                scrn.blit(piece_img, (col*SQUARE_SIZE, row*SQUARE_SIZE))
    
    # Draw highlighted squares
    for square in highlighted:
        # Does the square have a piece on it?
        is_piece = game.board.piece_at(chess.parse_square(square[0:2]))

        # Convert square location in chess notation to screen location
        rank, file = ord(square[0]) - 97, abs(8 - int(square[1]))
        x, y = rank*SQUARE_SIZE + SQUARE_SIZE/2, file*SQUARE_SIZE + SQUARE_SIZE/2

        # Select color of highlight based off if the square has a piece on it or not
        if is_piece: pygame.draw.circle(scrn, PIECE_HIGHLIGHTED_COLOR, (x,y), SQUARE_SIZE / 6)
        else: pygame.draw.circle(scrn, EMPTY_HIGHLIGHTED_COLOR, (x,y), SQUARE_SIZE / 6)
    pygame.display.flip()

# get_square(mouse_pos): Returns the square the mouse is currently at in chess notation
def get_square(mouse_pos):
    rank, file = mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE
    rank = chr(97 + rank)
    file = abs(8 - file)
    return f'{rank}{file}'

def get_legal_moves(square, board):
    # list of all legal moves
    moves = list(map(lambda x: str(x), list(board.legal_moves)))
    # list of all legal moves from {square}
    moves = list(filter(lambda x: (x.find(square) == 0), moves))
    # list of all squares the piece on {square} can move to
    moves = list(map(lambda x: x[2:5], moves))
    if moves: return moves
    else: return None

game = cm.BotGame(cm.minimax, cm.minimax, 'w')
update_board(game.board, [])
running = True
selected_square = None
available_moves = []
turn = 'w'
while running:
    if game.pygame_player == turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                square = get_square(pos)
                if available_moves and len(available_moves[0]) == 3: square+='q' # PROMOTION HERE <-------------------------------

                # Checking if piece can move to square and move piece if so
                if square in available_moves:
                    action = game.manual_move(f'{selected_square}{square}')
                    turn = 'b' if turn == 'w' else 'w'
                    if game.is_over(): running=False

                    # Sound effects
                    if action == 'check': pygame.mixer.Sound.play(CHECK_SOUND)
                    elif action == 'cap': pygame.mixer.Sound.play(CAPTURE_SOUND)
                    else: pygame.mixer.Sound.play(NO_CAPTURE_SOUND)

                legal_moves = get_legal_moves(square, game.board)
                # Highlighting square to move
                if legal_moves and square != selected_square:
                    selected_square = square
                    available_moves = legal_moves
                    update_board(game.board, legal_moves)

                # Unhighlight square
                else:
                    selected_square = None
                    available_moves = []
                    update_board(game.board, [])
                
            # Check for QUIT event      
            if event.type == pygame.QUIT:
                running = False
    else:
        # Bot movement
        #time.sleep(1)
        if turn == 'w': action = game.white_move()
        else: action = game.black_move()
        if game.is_over(): running=False
        turn = 'b' if turn == 'w' else 'w'
        
        # Sound effects
        if action == 'check': pygame.mixer.Sound.play(CHECK_SOUND)
        elif action == 'cap': pygame.mixer.Sound.play(CAPTURE_SOUND)
        else: pygame.mixer.Sound.play(NO_CAPTURE_SOUND)
        update_board(game.board, [])
        