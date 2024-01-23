import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128)]

# Tamaño de bloque y tablero
block_size = 30
board_width = width // block_size
board_height = height // block_size

# Función para crear una pieza nueva
def new_piece():
    piece = random.choice(pieces)
    color = random.choice(colors[1:])
    return {"piece": piece, "color": color, "x": board_width // 2 - 2, "y": 0}

# Definición de las piezas
pieces = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1]]
]

# Inicialización del juego
current_piece = new_piece()
board = [[0] * board_width for _ in range(board_height)]
clock = pygame.time.Clock()
game_over = False

# Función para dibujar el tablero
def draw_board():
    screen.fill(white)
    for y, row in enumerate(board):
        for x, color in enumerate(row):
            pygame.draw.rect(screen, colors[color], (x * block_size, y * block_size, block_size, block_size), 0)

# Función principal del juego
def run_game():
    global current_piece, game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_valid_move(current_piece, board, dx=-1):
                    current_piece["x"] -= 1
                elif event.key == pygame.K_RIGHT and is_valid_move(current_piece, board, dx=1):
                    current_piece["x"] += 1
                elif event.key == pygame.K_DOWN and is_valid_move(current_piece, board, dy=1):
                    current_piece["y"] += 1
                elif event.key == pygame.K_UP:
                    rotate_piece(current_piece, board)

        # Mover la pieza hacia abajo automáticamente
        if is_valid_move(current_piece, board, dy=1):
            current_piece["y"] += 1
        else:
            # Fijar la pieza en el tablero
            place_piece(current_piece, board)
            # Verificar si hay líneas completas
            check_lines()
            # Obtener una nueva pieza
            current_piece = new_piece()
            # Verificar si el juego ha terminado
            game_over = is_game_over(current_piece, board)

        # Dibujar el tablero y la pieza actual
        draw_board()
        draw_piece(current_piece)

        pygame.display.flip()
        clock.tick(5)  # Ajusta la velocidad del juego

# Función para verificar si el movimiento es válido
def is_valid_move(piece, board, dx=0, dy=0):
    for y, row in enumerate(piece["piece"]):
        for x, value in enumerate(row):
            if value:
                new_x, new_y = piece["x"] + x + dx, piece["y"] + y + dy
                if not (0 <= new_x < board_width and 0 <= new_y < board_height) or board[new_y][new_x]:
                    return False
    return True

# Función para rotar la pieza
def rotate_piece(piece, board):
    rotated_piece = [list(row) for row in zip(*reversed(piece["piece"]))]
    if is_valid_move({"piece": rotated_piece, "x": piece["x"], "y": piece["y"]}, board):
        piece["piece"] = rotated_piece

# Función para colocar la pieza en el tablero
def place_piece(piece, board):
    for y, row in enumerate(piece["piece"]):
        for x, value in enumerate(row):
            if value:
                board[piece["y"] + y][piece["x"] + x] = colors.index(piece["color"])

# Función para dibujar la pieza en la pantalla
def draw_piece(piece):
    for y, row in enumerate(piece["piece"]):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(screen, piece["color"], ((piece["x"] + x) * block_size, (piece["y"] + y) * block_size, block_size, block_size), 0)

# Función para verificar si hay líneas completas
def check_lines():
    global board
    lines_to_remove = [i for i, row in enumerate(board) if all(row)]
    for line in lines_to_remove:
        del board[line]
        board = [[0] * board_width] + board

# Función para verificar si el juego ha terminado
def is_game_over(piece, board):
    return not is_valid_move(piece, board, dy=1)

# Ejecutar el juego
run_game()

# Salir del programa
pygame.quit()
