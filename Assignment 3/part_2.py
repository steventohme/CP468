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

class kMeans:
    def __init__(self, k, data):
        self.k = k
        self.data = data
    