from typing import Tuple, List, Optional
from link_list_helper import Node
from link_list_helper import DoublyLinkedList

######### CONSTANS  ###########

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"


class Snake:
    """
    represent the snake in the game
    the snake is build as a double linked list.
    when every node has: (data:(coordinate, direction), prev, next)
    """

    def __init__(self, start_location: Tuple[int, int], direction: str, size: int):
        self.__location = start_location
        self.__direction = direction
        self.__len = size
        self.__snake_cells = DoublyLinkedList()  # we first make double link list
        self.__grow_left = 0  # cells left to add

    def set_snake_cells(self) -> None:
        """
        initial the snake as linked list
        """
        # set the cells initial data:
        x_cord = self.__location[0]
        y_cord = self.__location[1]

        cell_1_loc: Tuple[int, int] = (x_cord, y_cord)
        cell_2_loc: Tuple[int, int] = (x_cord, y_cord - 1)
        cell_3_loc: Tuple[int, int] = (x_cord, y_cord - 2)

        cell_1_data: Tuple[Tuple[int, int], str] = (cell_1_loc, self.__direction)
        cell_2_data: Tuple[Tuple[int, int], str] = (cell_2_loc, self.__direction)
        cell_3_data: Tuple[Tuple[int, int], str] = (cell_3_loc, self.__direction)

        # creation:

        cell_1 = Node(cell_1_data)
        cell_2 = Node(cell_2_data)
        cell_3 = Node(cell_3_data)

        # initial the linked list:

        self.__snake_cells.add_first(cell_3)
        self.__snake_cells.add_first(cell_2)
        self.__snake_cells.add_first(cell_1)

    def get_snake_cells(self) -> List[Tuple[int, int]]:
        """
        :return all the cells the snake is on as regular list
        """
        cur: Node = self.__snake_cells.get_head()
        value_as_lst: List[Tuple[int, int]] = []
        while cur is not None:
            value: Tuple[int, int] = cur.data[0]  # we wants only the location from the data
            value_as_lst.append(value)
            cur = cur.next
        return value_as_lst

    def get_snake_location(self) -> Tuple[int, int]:
        """
        :return: the snake head location
        """
        return self.__location

    def get_snake_dir(self):
        return self.__direction

    def move_to(self, move_to: Tuple[int, int], movekey, grow_size=0) -> Optional[Tuple[int, int]]:
        """
        it will be the head location + one to movekey
        :param move_to: The next cell the snake is going to go to
        :param movekey: The direction of the next cell
        :param grow_size: the size the snake gets to grow
        :return: None if the snake ate apple, the tail location if not.
        """
        if grow_size > 0:
            self.__grow_left += int(grow_size)

        # make a new head and link it

        new_head_data: Tuple[Tuple[int, int], str] = (move_to, movekey)
        new_head_node = Node(new_head_data)

        # make changes in the snake cells -> move the snake
        self.__snake_cells.add_first(new_head_node)  # add a new head
        self.__location = move_to
        self.__direction = movekey

        if self.__grow_left == 0:
            tail_loc = self.__snake_cells.remove_last()[0]  # get rid of the tail
            return tail_loc
        else:
            self.__grow_left -= 1
            return None
