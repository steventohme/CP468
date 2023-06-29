class point:
    """
    A class to represent a point in 2D space
    """
    def __init__(self, x, y):
        """
        Constructor for point class

        Parameters:
        ----------
            x (int): The x coordinate of the point
            y (int): The y coordinate of the point
        
        Attributes:
        ----------
            x (int): The x coordinate of the point
            y (int): The y coordinate of the point
        """
        self.x = x
        self.y = y

class kMeans:
    def __init__(self, k, data):
        self.k = k
        self.data = data
    