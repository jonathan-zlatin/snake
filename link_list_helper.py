class Node:
    """
    represent a snake cell
    """
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """
    the system yo form the snake
    """
    def __init__(self):
        self.__head = self.__tail = None
        self.__length = 0

    def get_head(self) -> Node:
        return self.__head

    def get_tail(self) -> Node:
        return self.__tail

    def add_last(self, node: Node):
        if self.__tail is None:
            # list was empty
            self.__head = node
        else:  # connect old tail to new node
            self.__tail.next = node
            node.prev = self.__tail
        # update head
        self.__tail = node
        self.__length += 1

    def add_first(self, node):
        if self.__head is None:
            # list was empty
            self.__tail = node
        else:  # connect old head to new node
            self.__head.prev = node
            node.next = self.__head
        # update head
        self.__head = node
        self.__length += 1

    def remove_last(self):
        data = self.__tail.data

        self.__tail = self.__tail.prev
        if self.__tail is None:  # list is now empty
            self.__head = None
        else:  # disconnect old tail
            self.__tail.next.prev = None  # disconnect the next node from the tail
            self.__tail.next = None  # disconnect the tail from the next
        self.__length -= 1
        return data

    def __str__(self):
        """
        return all the linked list data as list
        :return:
        """
        cur = self.__head
        value_as_lst = []
        while cur is not None:
            value = cur.data
            value_as_lst.append(value)
            cur = cur.next
        return value_as_lst
