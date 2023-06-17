# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

import random
class Board:
    def __init__(self, N: int, chromosome: bool) -> None:
        """
        Constructs an empty board object

        Parameters:
        ----------
            N (int): The size of the board
            chromosome (bool): Whether or not to generate a random board (chromosome) vs. an empty board
        
        Attributes:
        ----------
            N (int): The size of the board
            board (list[list[int]]): The board itself, a 2D array of integers
            diagonals (list[list[int]]): A list of all the diagonals on the board, precomputed instead of created every fitness function call
        """
        self.N = N
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        if chromosome:
            # this will ensure that there are no collisions vetically, 
            # therefore no need to check for vertical collisions
            queenPlacement = [random.randint(0, N - 1) for _ in range(N)]
            for i in range(N):
                self.board[queenPlacement[i]][i] = 1
        
        self.diagonals = self.createDiagonals()
            

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
    
    # TODO: implement -> def createDiagonals(self) -> list[list[int]]:

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
        diagonalCollisions = len([diagonal for diagonal in self.diagonals if diagonal.count(1) > 1])
        return int(maxFitness - (horizontalCollisions + diagonalCollisions))