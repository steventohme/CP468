# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

from collections import defaultdict

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
    def __init__(self, name: str, description: str, latitude: float, longitude: float):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
    

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
    """
    def __init__(self):
        self.graph = defaultdict(list)
    
    def addEdge(self, city: City, neighbour: City):
        self.graph[city].append(neighbour)
    



    
