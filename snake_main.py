import game_parameters
from game_display import GameDisplay
from board import Board
from bomb import Bomb
from snake import Snake
from apple import Apple

######### CONSTANS  ###########

WIDTH = game_parameters.WIDTH
HEIGHT = game_parameters.HEIGHT
SNAKE_LEN = 3
STARTING_POINT = (10, 10)

######### COLORS  ###########

RED = "Red"
YELLOW = "Yellow"
GREEN = "Green"
BLACK = "Black"
ORANGE = "Orange"

######### DIRECTIONS  ###########

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

######### BOARD_SIGNS  ###########

APPLE = "A"
BOMB = "B"
WAVE = "W"
SNAKE = "S"


def set_bomb_and_snake_and_apple():
    """
    initial the board
    :return:
    """
    bomb = Bomb()
    snake = Snake(STARTING_POINT, UP, SNAKE_LEN)
    lst_apple = [Apple() for app in range(3)]
    return bomb, snake, lst_apple


def main_loop(gd: GameDisplay) -> None:
    """
    :param gd: the game enviorment
    :return:
    """
    # set initial board
    gd.show_score(0)
    bomb, snake, apple_lis = set_bomb_and_snake_and_apple()
    main_board = Board(WIDTH, HEIGHT, snake, bomb, apple_lis)
    cord_board = main_board.get_cell_list()
    main_board.set_init_board()
    # color initial board
    for cell in cord_board:
        cell_content = main_board.get_cell_content(cell)

        row_cord = cell[1]
        col_cord = cell[0]

        # checks the cell sign and draw it.
        if cell_content == APPLE:
            gd.draw_cell(col_cord, row_cord, GREEN)
        elif cell_content == SNAKE:
            gd.draw_cell(col_cord, row_cord, BLACK)
        elif cell_content == BOMB:
            gd.draw_cell(col_cord, row_cord, RED)
        elif cell_content == WAVE:
            gd.draw_cell(col_cord, row_cord, ORANGE)
    gd.end_round()  # that was the first round

    while True:  # do one round
        # show current score status

        current_score = main_board.get_score_status()
        gd.show_score(current_score)

        key_clicked = gd.get_key_clicked()
        wave_lst = main_board.check_bomb_status()

        problem_show = False
        if wave_lst:  # checks if the snake hits the bomb
            for cell in snake.get_snake_cells():
                if cell in wave_lst:
                    problem_show = True
        if problem_show:
            break

        legal_move = main_board.move_snake(key_clicked)
        if legal_move:
            for cell in cord_board:
                cell_content = main_board.get_cell_content(cell)
                row_cord = cell[1]
                col_cord = cell[0]
                # checks the cell sign and draw it.
                if cell_content == APPLE:
                    gd.draw_cell(col_cord, row_cord, GREEN)
                elif cell_content == SNAKE:
                    gd.draw_cell(col_cord, row_cord, BLACK)
                elif cell_content == BOMB:
                    gd.draw_cell(col_cord, row_cord, RED)
                elif cell_content == WAVE:
                    gd.draw_cell(col_cord, row_cord, ORANGE)
        # that was the first round
        else:
            break
        gd.end_round()
