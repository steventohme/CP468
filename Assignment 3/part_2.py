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
    
    def __eq__(self, __value: object) -> bool:
        """
        Returns whether a point is equal to another point

        Returns:
        ---------
            bool: equal or not equal
        """
        return self.x == __value.x and self.y == __value.y
    
    def __hash__(self):
        """
        Computes the hash value for the point object based on its coordinates.

        Returns:
        ---------
            int: Hash value for the point object
        """
        return hash(str(self.x) + str(self.y))
    

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
        Assigns current data points to the closest centroid according to Euclidian distance
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
    
    def adjustCentroids(self) -> None:
        """
        Change centroids to be average of values of points contained within it
        """
        newCentroids = []
        for centroid in self.assignedData:
            count = 0
            xSum = 0
            ySum = 0
            for point in self.assignedData[centroid]:
                count += 1
                xSum += point.x
                ySum += point.y
            
            newCentroid = Point(xSum/count, ySum/count)
            newCentroids.append(newCentroid)
        
        self.centroids = newCentroids

def kMeansAlgorithm(k: int, X_data: pd.Series, Y_data: pd.Series) -> dict:
    """
    Runs K Means Clustering Algorithm

    Parameters:
    ----------
        k (int): K-value, amount of centroids in our algorithm
        X_data (pd.Series): Horizontal values of data points
        Y_data (pd.Series): Vertical values of data points
    
    Returns:
    ---------
        assignedData (dict): 
    """
    worker = kMeans(k, X_data, Y_data)
    worker.initializeCentroids()
    iterationCount = 0
    while True:
        iterationCount += 1
        prev = worker.centroids
        worker.assignCentroids()
        worker.adjustCentroids()
        if prev == worker.centroids:
            worker.assignCentroids()
            break
        prev = worker.centroids
    
    return worker.assignedData
