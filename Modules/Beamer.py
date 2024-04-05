import numpy as np

if __name__ == '__main__':
    from ShapeShadow import Move, Ellipse

else:
    from Modules.ShapeShadow import Move, Ellipse


class Spot:
    @staticmethod
    def angle_check(angle_incident:float) -> float:
        """
        Function for checking incident angle. Angle equal to 90 or above will be modulated by 90, i.e. 105 deg -> 15 deg
        """
        if angle_incident >= 90:
            angle_incident = angle_incident % 90

            print(f"WARNING: Grazing angle have been modulated to {angle_incident}")
        return angle_incident


    def __init__(self, diameter:float, angle_incident:float) -> None:
        """
        diameter: diameter of the spot at 0 deg incident
        angle_incident: angle of incident in degrees
        """
        
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
    def __init__(self, x:np.ndarray, y:np.ndarray, x_offset:float, y_offset:float, theta_offset:float) -> None:
        """
        x: x coordinates of the map pattern 
        y: y coordinates of the map pattern
        x_offset: x offset
        y_offset: y offset
        theta_offset: theta angle offset in degrees
        """
        
        self.x = x
        self.y = y
        
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.theta_offset = theta_offset

        return None
    

    def count(self) -> int:
        """
        Returns the number of measurements
        """
        
        return len(self.x)
    

    def offset(self) -> list[np.ndarray, np.ndarray]:
        """
        Applies the map pattern offset and returns two np.ndarrays with x and y coordinates
        
        NOTE: Data is NOT overwritten
        """
        
        x, y = Move.rotate(self.theta_offset, self.x, self.y)
        x, y = Move.translate(self.x_offset, self.y_offset, x, y)
        
        return x, y



class SpotCollection:
    """
    Class for applying spot information to map patterns.
    """

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
        """
        Returns a list of Ellipse objects centered on the coordiantes specified in the supplied MapPatternf

        NOTE: Offset in the map pattern is applied prior to creating the Ellipse object
        """
        
        # Setting major and minor of Ellipse object
        major = self.spot.elongation()
        minor = self.spot.diameter

        xs, ys = self.map_pattern.offset()  # Applying offset

        ellipse_obj = []
        for x, y in zip(xs, ys):
            ellipse = Ellipse(major=major, minor=minor)  # Creating object
            ellipse.translate(x, y)  # Centering ellipse on map pattern

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