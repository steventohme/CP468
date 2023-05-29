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
        return ((self.latitude - city.latitude)**2 + (self.longitude - city.longitude)**2)**0.5
 

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

    
    def BFS_TSP(self, start_node: City) -> tuple[float, list[City]]:
        """
        Finds the shortest path that visits all cities using BFS

        Parameters:
        ----------
            start_node (City): The starting city for the search

        Returns:
        ----------
            min_distance (float): The length of the shortest path
            path (List[City]): The order in which the cities were visited
        """
        # initialize variables for BFS
        num_nodes = len(self.cityList)
        queue = deque()
        visited = set()
        min_distance = float('inf')
        shortest_path = []

        # keep track of the current_node as well as the path
        queue.append((start_node, [start_node]))
        visited.add(start_node)


        # sort neighbours by distance from each city
        self.graph = self.sortNeighbours()

        while queue:
            current, current_path = queue.pop()
            if len(current_path) == num_nodes:
                # If all cities except the start city have been visited,
                # calculate the distance and update the minimum distance and shortest path if necessary
                distance = self.calcPathDistance(current_path) + current.calcDistance(start_node)
                if distance < min_distance:
                    min_distance = distance
                    shortest_path = current_path + [start_node]
                continue

            for neighbour in self.graph[current]:
                # Add the neighbours of the current city to the queue if they have not been visited
                if neighbour not in visited:
                    queue.append((neighbour, current_path + [neighbour]))
                    visited.add(neighbour)
                    break

        return min_distance, shortest_path

    def DFS_TSP(self, start_node: City) -> tuple[float, list[City]]:
        """
        Finds the shortest path that visits all cities using DFS

        Parameters:
        ----------
            start_node (City): The starting city for the search
        
        Returns:
        ----------
            min_distance (float): The length of the shortest path
            path (List[City]): The order in which the cities were visited
        """
        num_nodes = len(self.cityList)  # Total number of nodes in the graph
        stack = [(start_node, [start_node])]  # Stack to store nodes to be explored
        visited = set()  # Set to track visited nodes
        min_distance = float('inf')  # Variable to store the minimum distance found
        shortest_path = []  # Variable to store the shortest path found

        stack.append((start_node, [start_node]))
        visited.add(start_node)
        # Sort neighbours by distance from each city
        self.graph = self.sortNeighbours()

        while stack:
            current, current_path = stack.pop()
            if len(current_path) == num_nodes:
                # If all cities have been visited,
                # calculate the distance and update the minimum distance and shortest path if necessary
                distance = self.calcPathDistance(current_path) + current.calcDistance(start_node)
                if distance < min_distance:
                    min_distance = distance
                    shortest_path = current_path + [start_node]
                continue

            for neighbour in self.graph[current]:
                # Add the neighbours of the current city to the stack if they have not been visited
                if neighbour not in visited:
                    stack.append((neighbour, current_path + [neighbour]))
                    visited.add(neighbour)
                    break

        return min_distance, shortest_path
        

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
    distance, path = graph.BFS_TSP(start)
    graph.printPath(path)
    print(f"Distance: {distance}")
    print("Shortest Path using DFS Cycle")
    distance, path = graph.DFS_TSP(start)
    graph.printPath(path)
    print(f"Distance: {distance}")

main()