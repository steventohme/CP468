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
    
    def fitness(self) -> int:
        """
        Returns the fitness of the board
        fitness = (N * (N-1)/2) - collisions
    
        Returns:
        ----------
            fitness (int): The fitness of the board
        """
        maxFitness = (self.N * (self.N - 1)/2)
        horizontalCollisions = sum(1 for row in self.board if row.count(1) > 1)
        
        verticalCollisions = 0
        for col in range(self.N):
            onesCount = 0
            for row in range(self.N):
                if self.board[row][col] == 1:
                    onesCount += 1
                    if onesCount > 1:
                        verticalCollisions += 1
                        break
                

        return int(maxFitness - (horizontalCollisions + verticalCollisions))


        


