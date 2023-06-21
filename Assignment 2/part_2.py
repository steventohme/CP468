# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

from random import randint, random
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
            queenPlacement (list[int]): A list of the row index of each queen
            leftDiagonals (list[list[int]]): A list of all the diagonals on the board, going from top left to bottom right
            rightDiagonals (list[list[int]]): A list of all the diagonals on the board, going from top right to bottom left
        """
        self.N = N
        self.queenPlacement = [0 for _ in range(N)]
        if chromosome:
            # this will ensure that there are no collisions vetically, 
            # therefore no need to check for vertical collisions
            self.queenPlacement = [randint(0, N - 1) for _ in range(N)]
        self.board = self.createBoard()
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

    def __gt__(self, other: 'Board') -> bool:
        """
        Returns whether or not the current board is better than the other board

        Parameters:
        ----------
            other (Board): The other board to compare with
        
        Returns:
        ----------
            (bool): Whether or not the current board is better than the other board
        """
        return self.fitness() > other.fitness()
    
    def createBoard(self) -> list[list[int]]:
        """
        Creates a board based off of the queenPlacement list

        Returns:
        ----------
            board (list[list[int]]): The board itself, a 2D array of integers
        """
        board = [[0 for _ in range(self.N)] for _ in range(self.N)]
        for i in range(self.N):
            board[self.queenPlacement[i]][i] = 1
        return board
    
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
        return int(maxFitness - (horizontalCollisions + diagonalCollisions))



    def crossover(self, other: 'Board', crossoverRate: float) -> 'Board':
        """
        Performs a cross over between two boards

        Parameters:
        ----------
            other (Board): The other board to cross over with
            crossoverRate (float): The crossover rate

        Returns:
        ----------
            child1 (Board): First child board
            child2 (Board): Second child board

        """
        child1, child2 = self, other
        if random() < crossoverRate:
            crossoverPoint = randint(1, self.N - 1)
            child1.queenPlacement = self.queenPlacement[:crossoverPoint] + other.queenPlacement[crossoverPoint:]
            child2.queenPlacement = other.queenPlacement[:crossoverPoint] + self.queenPlacement[crossoverPoint:]
            child1.board = child1.createBoard()
            child2.board = child2.createBoard()
            child1.leftDiagonals, child1.rightDiagonals = child1.createDiagonals()
            child2.leftDiagonals, child2.rightDiagonals = child2.createDiagonals()
        
        return child1, child2
    
    def mutate(self, mutationRate: float) -> None:
        """
        Mutates the board

        Parameters:
        ----------
            mutationRate (float): The mutation rate
        """
        if random() < mutationRate:
            self.queenPlacement[randint(0, self.N - 1)] = randint(0, self.N - 1)
            self.board = self.createBoard()
            self.leftDiagonals, self.rightDiagonals = self.createDiagonals()

def pickRandomParent(population: list[Board], topPercent: float) -> Board:
    """
    Picks a random parent from the population

    Parameters:
    ----------
        population (list[Board]): The population of boards, sorted by fitness
        topPercent (float): The percentage of the population that is considered the best
    
    Returns:
    ----------
        parent (Board): The parent board
    """
    selectionPopulation = population[:int(len(population) * topPercent)]
    index = randint(0, len(selectionPopulation) - 1)
    return selectionPopulation[index]


def genetic(population: list[Board], topPercent: float, crossoverRate: float, mutationRate: float) -> list[Board]:
    """
    Performs the genetic algorithm on the population

    Parameters:
    ----------
        population (list[Board]): The population of boards
        topPercent (float): The percentage of the population that is considered the best
        crossoverRate (float): The crossover rate
        mutationRate (float): The mutation rate
    
    Returns:
    ----------
        newPopulation (list[Board]): The population of boards after the genetic algorithm is performed
    """ 
    sortedProbabilities = []
    newPopulation = []
    for board in population:
        sortedProbabilities.append(board)
    
    sortedProbabilities.sort(reverse=True)

    for i in range(len(sortedProbabilities)):
        parent1 = pickRandomParent(sortedProbabilities, topPercent)
        parent2 = pickRandomParent(sortedProbabilities, topPercent)

        child1, child2 = parent1.crossover(parent2)

        child1.mutate(mutationRate)
        child2.mutate(mutationRate)

        newPopulation.append(child1)
        newPopulation.append(child2)
        if child1.fitness() == child1.N * (child1.N - 1)/2 or child2.fitness()  == child2.N * (child2.N - 1)/2:
            break
    
    return newPopulation
    
    


if __name__ == "__main__":
    POPULATION_SIZE = 100
    N = int(input("Enter the size of the board: "))
    while N < 4:
        print("The size of the board must be greater than 3")
        N = int(input("Enter the size of the board (must be greater than 3): "))
    population = [Board(N, True) for _ in range(POPULATION_SIZE)]
    population.sort(reverse=True)