from apple import Apple
from bomb import Bomb
from snake import Snake
from typing import List, Tuple, Any

######### CONSTANS  ###########

APPLE = "A"
BOMB = "B"
WAVE = "W"
SNAKE = "S"

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

GROW_SIZE = 3


class Board:
    """
    represent the board in the game
    """

    def __init__(self, WIDTH: int, HEIGHT: int, snake: Snake, bomb: Bomb, apples_lis: List[Apple]):

        self.__snake = snake
        self.__width = WIDTH
        self.__height = HEIGHT
        self.__apples_lis: List[Apple] = apples_lis
        self.__bomb = bomb
        self.__score = 0
        self.__cells_content_lst: List = [["_"] * self.__width for rows in range(self.__height)]
        cord_lis = []
        for row in range(self.__height - 1, -1, -1):  # the cells are a bit different. (0,0) is on left, down corner
            for col in range(self.__width):
                cord_lis.append((col, row))
        self.__cells_cord_lst = cord_lis

    def set_init_board(self):
        """
        set the first bomb, snake and apples on the show board
        :return:
        """

        self.add_snake()
        while not self.add_bomb():  # as long as the initial place is taken, try again to put it
            pass
        for app in self.__apples_lis:
            while not self.add_apple(app):  # as long as the initial place is taken, try again to put it
                pass

    def get_cell_list_show(self) -> List[Any]:
        return self.__cells_content_lst

    def get_cell_list(self) -> List[tuple]:
        """
        :return: A list of all the cells in the board as tuples
        """
        return self.__cells_cord_lst

    def get_cell_content(self, coordinate):
        """
        Check whats inside a given cell
        :return: The name of whats in the cell, None if nothing
        """
        col: int = coordinate[0]
        row: int = coordinate[1]
        if self.__cells_content_lst[row][col] == "_":
            return None
        else:
            return self.__cells_content_lst[row][col]

    def get_dont_hit_list(self) -> List[Tuple[int, int]]:
        """
        :return: A list of all cells might finish the game
        """
        dont_hit_lis = []
        bomb_cell: Tuple = self.__bomb.get_bomb_location()
        snake_cells = self.__snake.get_snake_cells()
        dont_hit_lis += bomb_cell
        dont_hit_lis += snake_cells
        return dont_hit_lis

    def get_score_status(self) -> int:
        """
        :return: the current score, its increase when an apple is eaten
        """
        return self.__score

    def move_an_apple(self, apple: Apple) -> None:
        """
        moves the apple on the screen
        :param apple:
        :return: None
        """
        col, row = apple.get_apple_loc()
        self.__cells_content_lst[row][col] = "_"  # replace the apple with nothing
        apple.move_apple()  # move the apple
        new_loc = apple.get_apple_loc()

        while new_loc not in self.__cells_cord_lst or self.get_cell_content(new_loc) is not None:
            apple.move_apple()
            new_loc = apple.get_apple_loc()
        col, row = new_loc
        self.__cells_content_lst[row][col] = APPLE

    def check_bomb_status(self) -> List[Tuple[int, int]]:
        """
        check the bomb time, and current "wave". if thw wave
        ended the function moves the bomb location, and change the screen
        :return: A list with the wave cells
        """
        last_wave = self.__bomb.get_the_wave()
        if last_wave:
            for cell in last_wave:  # clean the last wave
                x_cord, y_cord = cell
                self.__cells_content_lst[y_cord][x_cord] = "_"

        wave_lst = self.__bomb.ready_to_expload()
        if wave_lst is not None:
            for cell in wave_lst:  # make new one, if possible
                x_cord, y_cord = cell
                # if its out of range:
                if x_cord <= 0 or x_cord > self.__width - 1 or y_cord <= 0 or y_cord > self.__height - 1:
                    self.move_the_bomb()
                    break
                else:
                    self.__cells_content_lst[y_cord][x_cord] = WAVE

            # check if targeted an apple:

            for app in self.__apples_lis:  # if the wave is on an apple
                if app.get_apple_loc() in wave_lst:
                    self.move_an_apple(app)
        else:
            col, row = self.__bomb.get_bomb_location()
            self.__cells_content_lst[row][col] = BOMB
        return wave_lst

    def move_the_bomb(self) -> None:
        """
        moves the bomb
        :return:
        """
        d_col, d_row = self.__bomb.get_bomb_location()
        last_wave = self.__bomb.move_the_bomb()
        n_loc = self.__bomb.get_bomb_location()
        if last_wave:  # its not empty -> erase the last wave
            for cell in last_wave:
                x_cord, y_cord = cell
                # do it only for cells on the board
                if 0 <= x_cord < self.__width and y_cord < self.__height and y_cord >= 0:
                    self.__cells_content_lst[y_cord][x_cord] = "_"

        # keep trying to find an empty place to put the bomb

        while n_loc not in self.__cells_cord_lst or self.get_cell_content(n_loc) is not None:
            self.__bomb.move_the_bomb()
            n_loc = self.__bomb.get_bomb_location()
            if n_loc in self.__cells_cord_lst and self.get_cell_content(n_loc) is None:
                break

        # now change the bomb location on the board

        n_col, n_row = n_loc
        self.__cells_content_lst[d_row][d_col] = "_"  # replace the bomb with nothing
        self.__cells_content_lst[n_row][n_col] = BOMB

    def add_apple(self, apple: Apple) -> bool:
        """
        adds an apple to the board, probbly only at the beginning
        :param apple: an apple object
        :return: True if it was able to add the apple, false if it couldn't
        """
        col, row = apple.get_apple_loc()
        if self.get_cell_content((col, row)) is None:
            self.__cells_content_lst[row][col] = APPLE  # sign the apple on the board
            return True
        else:
            return False

    def add_snake(self) -> None:
        """
        put the initial snake on the screen
        """
        self.__snake.set_snake_cells()
        snake_cells: List[Tuple[int, int]] = self.__snake.get_snake_cells()
        for cell in snake_cells:
            col, row = cell
            self.__cells_content_lst[row][col] = SNAKE

    def add_bomb(self) -> bool:
        """
        adds a bomb to the board
        :return: True if it was able to add the bomb, false if it couldn't
        """
        bomb_cord = self.__bomb.get_bomb_location()
        col, row = bomb_cord
        if self.get_cell_content(bomb_cord) is None:
            self.__cells_content_lst[row][col] = BOMB
            return True
        else:
            return False

    def move_snake(self, movekey: str) -> bool:
        """
        :param movekey: given direction
        :return: if its possible to do this move
        """
        snake_loc: Tuple[int, int] = self.__snake.get_snake_location()
        next_loc_row: int = snake_loc[1]
        next_loc_col: int = snake_loc[0]
        snake_next_loc: Tuple[int, int] = snake_loc

        # first check if the next step is in legal location
        # if not, change the movekey for the last given direction

        snake_dir = self.__snake.get_snake_dir()
        if movekey is None:  # if nothing been clicked keep as you were
            movekey = snake_dir
        elif snake_dir == movekey:
            movekey = snake_dir
        elif movekey == RIGHT and snake_dir == LEFT:
            movekey = snake_dir
        elif movekey == UP and snake_dir == DOWN:
            movekey = snake_dir
        elif movekey == LEFT and snake_dir == RIGHT:
            movekey = snake_dir
        elif movekey == DOWN and snake_dir == UP:
            movekey = snake_dir

        # if the function return None, the order wasn't legal, so keep going the same direction
        # first check whats going to be the snake next cell

        if movekey == UP:
            snake_next_loc: Tuple[int, int] = (next_loc_col, next_loc_row + 1)
        elif movekey == DOWN:
            snake_next_loc: Tuple[int, int] = (next_loc_col, next_loc_row - 1)
        elif movekey == RIGHT:
            snake_next_loc: Tuple[int, int] = (next_loc_col + 1, next_loc_row)
        elif movekey == LEFT:
            snake_next_loc: Tuple[int, int] = (next_loc_col - 1, next_loc_row)

        if next_loc_col < 0 or next_loc_col >= self.__width - 1 or next_loc_row < 0 or next_loc_row >= self.__height - 1 or snake_next_loc in self.get_dont_hit_list():

            return False  # the next cell isn't on the board

        elif self.get_cell_content(snake_next_loc) == APPLE:
            # get the apple the snake is going to step on
            moving_apple = self.__apples_lis[0]
            for app in self.__apples_lis:
                if app.get_apple_loc() == snake_next_loc:
                    moving_apple = app

            # move the apple
            score = moving_apple.get_apple_score()
            self.__score += score

            self.move_an_apple(moving_apple)
            # self.__snake.eat_apple(moving_apple)

            n_col, n_row = snake_next_loc
            self.__cells_content_lst[n_row][n_col] = SNAKE  # change the head to "S" on the screen
            removing_cell = self.__snake.move_to(snake_next_loc, movekey, GROW_SIZE)
            if removing_cell is not None:  # if its a cord:
                col, row = removing_cell
                self.__cells_content_lst[row][col] = "_"  # change the tail to nothing on the screen
            return True
        elif self.get_cell_content(snake_next_loc) == BOMB:
            return False
        elif self.get_cell_content(snake_next_loc) == WAVE:
            return False
        else:
            # nothing special happen
            # move the snake on screen

            n_col, n_row = snake_next_loc
            self.__cells_content_lst[n_row][n_col] = SNAKE  # change the head to "S" on the screen
            removing_cell: Tuple[int, int] = self.__snake.move_to(snake_next_loc, movekey)
            if removing_cell is not None:  # if its a cord:
                col, row = removing_cell
                self.__cells_content_lst[row][col] = "_"  # change the tail to nothing on the screen
            return True
