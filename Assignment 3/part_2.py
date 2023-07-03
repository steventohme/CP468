# Author: Steven Tohme
# Class: CP468 - Artificial Intelligence

import pandas as pd
from random import randint

class Point:
    """
    A class to represent a point in 2D space

    """
    def __init__(self, x: float, y: float) -> None:
        """
        Constructor for point class

        Parameters:
        ----------
            x (int): The x coordinate of the point
            y (int): The y coordinate of the point
        
        """
        self.x = x
        self.y = y
    
    def calcDistance(self, other: 'Point') -> float:
        """
        Calculates the Euclidian distance between the current point and the point passed as a parameter

        Parameters:
        ----------
            other (Point): The point to compare to
        
        Returns:
        ----------
            float: The Euclidian distance between the two points
        """
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __str__(self) -> str:
        """
        Returns string representation of point object

        Returns:
        ---------
            str: string representation of point object
        """
        return f"[X: {self.x}, Y: {self.y}]"

class kMeans:
    """
    A class to represent a k-means clustering algorithm

    """
    def __init__(self, k: int, X_data: pd.Series, Y_data: pd.Series) -> None:
        self.k = k
        self.data = self.createData(X_data, Y_data)
        self.centroids = []
        self.assignedData = {}
    
    def createData(self, X_data: pd.Series, Y_data: pd.Series) -> list[Point]:
        """
        Creates a list of points from the data passed to the class

        Parameters:
        ----------
            data (pandas Dataframe): The data to be converted to a list of points

        Returns:
        ----------
            list[point]: A list of points
        """
        points = []
        for i in range(len(X_data)):
            points.append(Point(X_data[i], Y_data[i]))
        return points
    
    def initializeCentroids(self) -> None:
        """
        Initializes the centroids of the k-means algorithm
        """
        centroids = []
        for _ in range(self.k):
            centroids.append(self.data[randint(0, len(self.data) - 1)])
        
        self.centroids = centroids
    
    def assignCentroids(self) -> None:
        """
        Assigns current data points to the closest centroid according to euclidian distance
        """
        assignedData = {}
        for centroid in self.centroids:
            assignedData[centroid] = []
        
        for point in self.data:
            distanceMin = point.calcDistance(self.centroids[0])
            centroidMin = self.centroids[0]
            for centroid in self.centroids[1:]:
                distance = point.calcDistance(centroid)
                if distance < distanceMin:
                    distanceMin = distance
                    centroidMin = centroid
            
            assignedData[centroidMin].append(point)

        self.assignedData = assignedData




if __name__ == "__main__":
    data = pd.read_csv("Assignment 3/kmeans.csv")
    k = 3
    kmeans = kMeans(k, data['f1'], data['f2'])
    kmeans.initializeCentroids()
    kmeans.assignCentroids()
    for point in kmeans.assignedData:
        print(point)