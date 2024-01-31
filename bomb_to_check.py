import game_parameters

class Bomb:

    def __init__(self, color, size):
        self.__color = color
        self.__size = size
        self.location = [game_parameters.get_random_bomb_data()[0:2]]
        self.__radius = game_parameters.get_random_bomb_data()[2]
        self.__time = game_parameters.get_random_bomb_data()[3]

    def extend_bomb(self):
        """
        todo: think of changing the color
        :return:
        """
        self.__color = "orange"
        self.location = self.bomb_cells()
        return

    def get_bomb_radius(self):
        return self.__radius

    def get_bomb_time(self):
        return self.__time

    def get_bomb_location(self):
        """
        A list of the bomb cells
        :return: A list
        """
        return self.__location


    def bomb_cells(self):
        """

        :return:
        """
        r = 0
        x = self.location[0][0]
        y = self.location[0][1]
        u = x
        v = y
        lst = []
        lst_wrong = []
        for radius in range(self.__radius + 1):
            lst = self.bomb_cells_helper(r,x,y,u,v,lst,lst_wrong)
            self.location = lst
            lst = []
            lst_wrong = []
            r += 1
        return



    def bomb_cells_helper(self, r,x,y, u, v,lst,lst_wrong):
        if abs(x-u) + abs(y-v) == r:
            if (u, v) not in lst:
                return lst + [(u, v)]
            else:
                return lst
        else:
            if (u,v) in lst_wrong:
                return lst
            else:
                lst = self.bomb_cells_helper(r, x, y, u, v + 1, lst, lst_wrong + [(u,v)])
                lst = self.bomb_cells_helper(r, x, y, u + 1, v, lst, lst_wrong + [(u,v)])
                lst = self.bomb_cells_helper(r, x, y, u - 1, v, lst, lst_wrong + [(u,v)])
                lst = self.bomb_cells_helper(r, x, y, u, v - 1, lst, lst_wrong + [(u,v)])
                return lst



bomb = Bomb("red",1)
print(bomb.bomb_cells())