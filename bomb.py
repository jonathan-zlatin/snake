import game_parameters
from typing import Tuple, List
import copy

"""
changes:
1. separate between bomb cell and its "wave"
2. get bomb cell -> get "wave" cells
"""


class Bomb:
    """
    represent the Bomb in the game
    """

    def __init__(self):
        col, row, self.__radius, self.__time_left = game_parameters.get_random_bomb_data()
        self.__location = (col, row)
        self.__radius_temp = 0
        self.__wave = []

    def move_the_bomb(self) -> List[Tuple[int, int]]:
        """
        moves the bomb and return its location
        :return: the last recorded wave
        """
        col, row, self.__radius, self.__time_left = game_parameters.get_random_bomb_data()
        self.__location = (col, row)
        self.__radius_temp = 0
        last_wave = copy.copy(self.__wave)
        self.__wave = []
        return last_wave  # the last recorded wave

    def get_the_wave(self) -> List[Tuple[int, int]]:
        return self.__wave

    def get_bomb_location(self) -> Tuple[int, int]:
        """
        A list of the bomb cells
        :return: A list
        """
        return self.__location

    def ready_to_expload(self):
        """
        the function check the time to expload, and the radius initiate the bomb, or moves it if it finished
        :return: a list of all thr cells the current wave is on
        """
        if self.__time_left == 0:
            wave_lst = self.bombs_wave(self.__location, self.__radius_temp)  # a list with the current wave
            self.__radius_temp += 1
            if self.__radius_temp > self.__radius:
                self.move_the_bomb()
                return
            return wave_lst
        else:
            self.__time_left -= 1
            return None

    def bombs_wave(self, cord: Tuple[int, int], radius: int) -> List[Tuple[int, int]]:
        """
        :param cord: the center ow the wave - the bomb location
        :param radius: a given radius
        :return:
        """
        wave_lst = []
        x_cord, y_cord = cord
        # find the for corners of the wave:
        cell_1 = (x_cord, y_cord + radius)
        cell_2 = (x_cord, y_cord - radius)
        cell_3 = (x_cord + radius, y_cord)
        cell_4 = (x_cord - radius, y_cord)
        wave_lst.append(cell_1)
        wave_lst.append(cell_2)
        wave_lst.append(cell_3)
        wave_lst.append(cell_4)

        # now we will add all the cord that on the square lines:
        for i in range(1, radius):
            new_cord = (x_cord + i, y_cord + radius - i)
            if new_cord not in wave_lst:
                wave_lst.append(new_cord)

        for i in range(1, radius):
            new_cord = (x_cord + i, y_cord - radius + i)
            if new_cord not in wave_lst:
                wave_lst.append(new_cord)

        for i in range(1, radius):
            new_cord = (x_cord - radius + i, y_cord - i)
            if new_cord not in wave_lst:
                wave_lst.append(new_cord)

        for i in range(1, radius):
            new_cord = (x_cord - radius + i, y_cord + i)
            if new_cord not in wave_lst:
                wave_lst.append(new_cord)

        self.__wave = wave_lst
        return wave_lst
