# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

import random
from math import comb

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
            leftDiagonals (list[list[int]]): A list of all the diagonals on the board, going from top left to bottom right
            rightDiagonals (list[list[int]]): A list of all the diagonals on the board, going from top right to bottom left
        """
        self.N = N
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        if chromosome:
            # this will ensure that there are no collisions vetically, 
            # therefore no need to check for vertical collisions
            queenPlacement = [random.randint(0, N - 1) for _ in range(N)]
            for i in range(N):
                self.board[queenPlacement[i]][i] = 1
        
        self.leftDiagonals, self.rightDiagonals = self.createDiagonals()
            

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
    
    def createDiagonals(self) -> list[list[int]]:
        """
        Creates a list of all the diagonals on the board

        Returns:
        ----------
            diagonals (list[list[int]]): A list of all the diagonals on the board
        """
        # every diagonal has a unique sum of row + col, so we can use that as an index
        
        leftDiagonals = [[] for _ in range(N * 2 - 1)]
        rightDiagonals = [[] for _ in range(N * 2 - 1)]

        for i in range(N):
            for j in range(N):
                leftDiagonals[i + j].append(self.board[i][N - 1 - j])


        for i in range(N):
            for j in range(N):
                rightDiagonals[i + j].append(self.board[i][j])
    
        return leftDiagonals, rightDiagonals
    
    def fitness(self) -> int:
        """
        Returns the fitness of the board
        fitness = (N * (N-1)/2) - collisions
    
        Returns:
        ----------
            fitness (int): The fitness of the board
        """
        maxFitness = (self.N * (self.N - 1)/2)

        # we must use the comb function to figure out how many pairs of queens are colliding
        horizontalCollisions = sum(comb(row.count(1),2) for row in self.board)
        diagonalCollisions = sum(comb(diagonal.count(1),2) for diagonal in self.rightDiagonals) + sum(comb(diagonal.count(1),2) for diagonal in self.leftDiagonals)
        return int(maxFitness - (horizontalCollisions + diagonalCollisions)), horizontalCollisions, diagonalCollisions


if __name__ == "__main__":
    POPULATION_SIZE = 100
    N = int(input("Enter the size of the board: "))
    while N < 4:
        print("The size of the board must be greater than 3")
        N = int(input("Enter the size of the board (must be greater than 3): "))
    population = [Board(N, True) for _ in range(POPULATION_SIZE)]
    print(population[0])
    print(population[0].fitness())