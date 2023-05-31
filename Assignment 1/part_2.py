# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

from collections import defaultdict, deque

class City:
    """
    class to represent a city instance

    ----------
    Attributes:
    ----------
        name (string): The name of the state
        description (string): The name of the city
        latitude (float): The latitude of the city
        longitude (float): The longitude of the city

    ----------
    Methods:
    ----------
        calcDistance(city: City) -> float: Calculates the Euclidian distance between the current city and the city passed as a parameter

    """
    def __init__(self, name: str, description: str, latitude: float, longitude: float) -> None:
        """
        Constructs city object

        Parameters:
        ----------
            name (string): The name of the state
            description (string): The name of the city
            latitude (float): The latitude of the city
            longitude (float): The longitude of the city
        """
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
    
    def __hash__(self):
        """
        Hashes the city object

        Returns:
        ----------
            hash (int): The hash of the city object
        """
        return hash((self.name, self.description))

    def __eq__(self, other):
        """
        Checks if two city objects are equal

        Parameters:
        ----------
            other (City): The city to compare to
        
        Returns:
        ----------
            bool: True if the cities are equal, False otherwise
        """
        return (self.name, self.description) == (other.name, other.description)
    

    def calcDistance(self, city: 'City') -> float:
        """
        Calculates the Euclidian distance between the current city and the city passed as a parameter

        Parameters:
        ----------
            city (City): The city to calculate the distance to

        Returns:
        ----------
            distance (float): The distance between the two cities
        """
        return round(((self.latitude - city.latitude)**2 + (self.longitude - city.longitude)**2)**0.5, 2)
 

class Graph:
    """
    class to represent a graph
    ----------
    Attributes:
    ----------
        graph (dict): A dictionary containing the graph in the form {City: [City1, City2, ...]}
    
    ----------
    Methods:
    ----------
        addEdge(city: City, neighbour: City) -> None: Adds an edge between two cities
        createGraph(city_file: str) -> Graph: Creates a graph from a file containing cities
    """
    def __init__(self) -> None:
        self.graph = defaultdict(list)
        self.cityList = []
    
    def createCityList(self, cityFile: str) -> None:
        """
        Creates a list of cities to be referenced by the graph

        Parameters:
        ----------
            cityFile (string): The name of the file containing the cities
        """
        self.cityList = []
        with open(cityFile) as f:
            for line in f:
                line = line.split(',')
                if line[0] == 'name':
                    continue
                city = City(line[0], line[1], float(line[2]), float(line[3]))
                self.cityList.append(city)

    def addEdge(self, city: City, neighbour: City) -> None:
        """
        Adds an edge between two cities

        Parameters:
        ----------
            city (City): The city to add the edge to
            neighbour (City): The city to add as a neighbour
        """
        self.graph[city].append(neighbour)
    
    def createGraph(self, cityFile: str) -> 'Graph':
        """
        Creates a graph from a file containing cities

        Parameters:
        ----------
            city_file (string): The name of the file containing the cities

        Returns:
        ----------
            graph (Graph): The graph created from the file
        """
        self.createCityList(cityFile)
        for city in self.cityList:
            for neighbour in self.cityList:
                if city.calcDistance(neighbour) <= 500:
                    self.addEdge(city, neighbour)
        return self

    def sortNeighbours(self) -> dict:
        """
        Sorts the neighbours of each city in the graph by their distance to the city

        Returns:
        ----------
            graph (dict): The graph with the neighbours sorted
        """
        for city in self.graph:
            self.graph[city].sort(key=lambda x: city.calcDistance(x))
        return self.graph

    def calcPathDistance(self, path: list) -> float:
        """
        Calculates the total distance of a path

        Parameters:
        ----------
            path (list): The path to calculate the distance of

        Returns:
        ----------
            distance (float): The total distance of the path
        """
        distance = 0
        for i in range(len(path) - 1):
            distance += path[i].calcDistance(path[i+1])
        return round(distance, 2)

    def BFS(self, start_node: City, end_node: City) -> tuple[list[City], float]:
        """
        Performs a breadth first search on the graph

        Parameters:
        ----------
            start_node (City): The starting city
            end_node (City): The goal city

        Returns:
        ----------
            path (list): The path from the start city to the goal city
        """

        # initialize FIFO queue and visited set
        queue = deque()
        visited = set()

        # add start node to queue and visited set
        queue.append((start_node,[start_node]))
        visited.add(start_node)

        # while the queue is not empty i.e. there are still nodes to visit
        while queue:
            current_city, current_path = queue.pop()
            if current_city == end_node:
                return current_path, self.calcPathDistance(current_path)
            
            # add all neighbours of the current node to the queue and visited set
            for neighbour in self.graph[current_city]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, current_path + [neighbour]))
        
        return None, None
    
    def DFS(self, start_node: City, end_node:City):
        """
        Performs a depth first search on the graph

        Parameters:
        ----------
            start_node (City): The starting city
            end_node (City): The goal city

        Returns:
        ----------
            path (list): The path from the start city to the goal city
        """
        # initialize stack and visited set
        stack = []
        visited = set()

        # add start node to stack and visited set
        stack.append((start_node,[start_node]))
        visited.add(start_node)

        # while the stack is not empty i.e. there are still nodes to visit
        while stack:
            current_city, current_path = stack.pop()
            if current_city == end_node:
                return current_path, self.calcPathDistance(current_path)
            
            # add all neighbours of the current node to the stack and visited set
            for neighbour in self.graph[current_city]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append((neighbour, current_path + [neighbour]))
        
        return None, None

    def printPath(self, path: list) -> None:
        """
        Prints the path in the form of a list of cities

        Parameters:
        ----------
            path (list): The path to print
        """
        for i,city in enumerate(path):
            if i == len(path) - 1:
                print(f"{city.description}")
            else:
                print(f"{city.description}" + " -> ", end="")


def main():
    graph = Graph().createGraph('Assignment 1/city_data_50.csv')
    start = graph.cityList[0]
    print("Shortest Path using BFS")
    path, distance = graph.BFS(start, graph.cityList[3])
    graph.printPath(path)
    print(f"Distance: {distance}")
    print("Shortest Path using DFS Cycle")
    path, distance = graph.DFS(start, graph.cityList[3])
    graph.printPath(path)
    print(f"Distance: {distance}")

main()