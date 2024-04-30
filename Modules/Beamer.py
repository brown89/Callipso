import numpy as np

if __name__ == '__main__':
    from ShapeShadow import Move, Ellipse

else:
    from Modules.ShapeShadow import Move, Ellipse


class Spot(Ellipse):
    @staticmethod
    def angle_check(angle_incident:float) -> float:
        """
        Function for checking incident angle. Angle equal to 90 or above will be modulated by 90, i.e. 105 deg -> 15 deg
        """
        if angle_incident >= 90:
            angle_incident = angle_incident % 90

            print(f"WARNING: Grazing angle have been modulated to {angle_incident}")
        return angle_incident


    @staticmethod
    def _major_(angle_incident:float, minor:float) -> float:
        """
        Calculates the major in an ellipse
        """
        return minor / np.cos(np.deg2rad(angle_incident))


    def __init__(self, beam_diameter:float, angle_incident:float) -> None:
        """
        diameter: diameter of the spot at 0 deg incident
        angle_incident: angle of incident in degrees
        """
        
        angle_incident = Spot.angle_check(angle_incident)
        minor = beam_diameter
        major = self._major_(angle_incident, beam_diameter)
        
        self.diameter = beam_diameter
        self.angle_incident = angle_incident

        super(Spot, self).__init__(major, minor)
        
        return None
    
    
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

        self.x_inst: np.ndarray
        self.y_inst: np.ndarray

        self._gen_instrument_xy_()
        
        return None
    

    def _gen_instrument_xy_(self):
        x, y = Move.rotate(self.theta_offset, self.x, self.y)
        self.x_inst, self.y_inst = Move.translate(self.x_offset, self.y_offset, x, y)

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
        
        return self.x_inst, self.y_inst



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
    print("This is a test")
