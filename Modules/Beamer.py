import numpy as np

from ShapeShadow import Move, Ellipse


class Spot:
    @staticmethod
    def angle_check(angle_incident:float) -> float:
        if angle_incident >= 90:
            angle_incident = angle_incident % 90

            print(f"WARNING: Grazing angle have been modulated to {angle_incident}")
        return angle_incident


    def __init__(self, diameter:float, angle_incident:float) -> None:

        angle_incident = Spot.angle_check(angle_incident)

        self.diameter = diameter
        self.angle_incident = angle_incident

        return None
    
    
    def area(self) -> float:
        """
        Return: area of the spot
        """
        
        return np.pi * (self.diameter/2)**2 / np.cos(np.deg2rad(self.angle_incident))


    def elongation(self) -> float:
        """
        Return: elongation of the spot
        """
        
        return self.diameter / np.cos(np.deg2rad(self.angle_incident))


    
class MapPattern:
    def __init__(self, x_coordinates:np.ndarray, y_coordinates:np.ndarray, x_offset:float, y_offset:float, theta_offset:float) -> None:
        self.x = x_coordinates
        self.y = y_coordinates
        
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.theta_offset = theta_offset

        return None
    

    def count(self):
        """
        Returns the number of measurements
        """
        
        return len(self.x)
    

    def offset(self) -> list[np.ndarray, np.ndarray]:
        x, y = Move.rotate(self.theta_offset, self.x, self.y)
        x, y = Move.translate(self.x_offset, self.y_offset, x, y)
        
        return x, y



class SpotCollection:
    def __init__(self, map_pattern:MapPattern, spot:Spot) -> None:
        self.map_pattern = map_pattern
        self.spot = spot

        return None
    

    def coverate(self) -> float:
        """
        Returns the area covered by the spots
        """

        return self.map_pattern.count() * self.spot.area()
    

    def outlines(self) -> list[Ellipse]:
        minor = self.spot.diameter
        major = self.spot.elongation()

        xs, ys = self.map_pattern.offset()
        ellipse_obj = []

        for x, y in zip(xs, ys):
            ellipse = Ellipse(major=major, minor=minor)
            ellipse.translate(x, y)

            ellipse_obj.append(ellipse)

        return ellipse_obj
    


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    map_pattern = MapPattern(np.array([0, 1, 1, 0]), np.array([0, 0, 1, 1]), -.5, -.5, 30)
    spot = Spot(.3, 65)
    spot_collection = SpotCollection(map_pattern=map_pattern, spot=spot)
    
    fig, ax = plt.subplots()
    for spot in spot_collection.outlines():
        ax.plot(spot.x, spot.y, '-k')

    ax.set_aspect('equal')  # Set the aspect 1:1
    plt.show()