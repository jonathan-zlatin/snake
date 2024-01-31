from typing import Tuple
import game_parameters


class Apple:
    """
    represent the apple in the game
    """

    def __init__(self):
        col, row, self.__score = game_parameters.get_random_apple_data()
        self.__location = (col, row)

    def move_apple(self):
        """
        change the apples data
        :return: None
        """
        col, row, self.__score = game_parameters.get_random_apple_data()
        self.__location: Tuple[int, int] = (col, row)

    def get_apple_loc(self) -> Tuple[int, int]:
        return self.__location

    def get_apple_score(self) -> int:
        return self.__score
