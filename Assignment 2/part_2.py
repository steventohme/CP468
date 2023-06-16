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
        self.board = [[1 for i in range(N)] for j in range(N)]

    def __str__(self) -> str:
        """
        Returns a string representation of the board

        Returns:
        ----------
            string (str): The string representation of the board
        """
        string = ""
        for row in self.board:
            for cell in row:
                if cell == 1:
                    string += "♛ "
                else:
                    string += str(cell) + " "
            string += "\n"
        return string


if __name__ == "__main__":
    board = Board(8)
    print(board)