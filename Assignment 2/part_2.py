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
        self.board = [[0 for _ in range(N)] for _ in range(N)]

    def __str__(self) -> str:
        """
        Returns a string representation of the board

        Returns:
        ----------
            string (str): The string representation of the board
        """
        
        string = ""
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 1:
                    string += "♛ "
                elif (i + j) % 2 == 0:
                    string += "⬛"
                else:
                    string += "⬜"
            string += "\n"
        return string
