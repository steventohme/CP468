# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence


class Board:
    def __init__(self, N: int) -> None:
        """
        Constructs an empty board object

        Parameters:
        ----------
            N (int): The size of the board
        """
        self.N = N
        self.board = [[0 for i in range(N)] for j in range(N)]
