from apple import Apple
from bomb import Bomb
from snake import Snake
from board import Board
from typing import Tuple

######### CONSTANS  ###########

APPLE = "A"
BOMB = "B"
WAVE = "W"

# set the variables:
bomb = Bomb("blue", 1)

apple1 = Apple("red", 1)
apple2 = Apple("red", 1)

snake = Snake((1, 1), "up", 3)
board1 = Board(2, 2, snake, bomb)
board2 = Board(3, 3, snake, bomb)
board3 = Board(100, 100, snake, bomb)

# board1.add_apple(apple1)
# board1.add_apple(apple2)
board3.add_apple(apple1)
board3.add_apple(apple2)

board3.set_init_board()


def test_get_cell_list_show():
    assert board1.get_cell_list_show() == [["_", "_"], ["_", "_"]]
    assert board2.get_cell_list_show() == [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]


def test_get_cell_list():
    assert board1.get_cell_list() == [(1, 0), (1, 1), (0, 0), (0, 1)]
    assert board2.get_cell_list() == [(2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 1), (0, 2)]


def test_get_cell_content():
    assert board1.get_cell_content((1, 1)) is None
    assert board1.get_cell_content((1, 1)) != "_"
    assert board3.get_cell_content(apple1.get_apple_loc()) == APPLE
    assert board3.get_cell_content(apple1.get_apple_loc()) == APPLE
    assert board3.get_cell_content(bomb.get_bomb_location()) == BOMB


def test_dont_hit_list():
    assert type(board3.get_dont_hit_list()) == list
    assert len(board3.get_dont_hit_list()) == 2


def move_an_apple():
    pass
