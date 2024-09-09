import numpy as np
from matplotlib.axes import Axes

import os
import sys
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from Utilities.Transform import rotate, translate
from Modules.ShapeShadow import Ellipse



class Spot(Ellipse):
    @staticmethod
    def angle_check(angle_incident:float) -> float:
        """
        Function for checking incident angle. 
        Angle equal to 90 or above will be modulated by 90, i.e. 105 deg -> 15 deg
        """
        if angle_incident >= 90:
            angle_incident = angle_incident % 90

            print(f"WARNING: Grazing angle have been modulated to {angle_incident}")
        return angle_incident


    @staticmethod
    def major(angle_incident:float, minor:float) -> float:
        """
        Calculates the major in an ellipse
        """
        return minor / np.cos(np.deg2rad(angle_incident))


    def __init__(self, beam_diameter:float, angle_incident:float) -> None:
        """
        Spot holdes all information in relation to the beam.
        Inherents from 'Ellipse'

        - beam_diameter: diameter of the spot at 0 deg incident
        - angle_incident: angle of incident in degrees
        """
        
        angle_incident = Spot.angle_check(angle_incident)
                
        self.diameter = beam_diameter
        self.angle_incident = angle_incident
        
        height = beam_diameter
        width = Spot.major(angle_incident, beam_diameter)

        super().__init__(width, height)
        return None
    
    
    def elongation(self) -> float:
        """
        Return: elongation of the spot i.e. major of an ellipse.
        """
        
        return self.width



class MapPattern:
    def __init__(self, x:list[float], y:list[float], x_offset:float, y_offset:float, theta_offset:float) -> None:
        """
        - x: x coordinates of the map pattern 
        - y: y coordinates of the map pattern
        - x_offset: x offset
        - y_offset: y offset
        - theta_offset: theta angle offset in degrees
        """
        
        self.xy = np.array([x, y])
        self.xy_offset = np.array([x_offset, y_offset])
        self.t_offset = theta_offset

        return None
    

    def count(self) -> int:
        """
        Returns the number of measurements

        - returns: int
        """
        
        return self.xy.shape[1]
    

    def xy_instrument(self) -> np.ndarray:
        """
        Returns the x- and y-coordinates of the instrument.
        Dimensions [2, N]

        - returns: np.ndarray
        """
        
        xy_inst = self.xy.copy()

        xy_inst = rotate(xy_inst, self.t_offset)
        xy_inst = translate(xy_inst, self.xy_offset)

        return xy_inst



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
    

    def plot(self, axes:Axes, as_ellipse=False, **kwargs) -> None:
        """
        Returns a list of Ellipse objects centered on the coordiantes specified in the supplied MapPatternf

        NOTE: Offset in the map pattern is applied prior to creating the Ellipse object
        """
        
        # Setting major and minor of Ellipse object
        major = self.spot.elongation()
        minor = self.spot.diameter

        xy = self.map_pattern.xy_instrument()  # Applying offset
        
        if as_ellipse:
            for row in xy.T:
                ellipse = Ellipse(width=major, height=minor)  # Creating object
                ellipse.translate(row[0], row[1])  # Centering ellipse on map pattern

                ellipse.plot(axes, as_patch=True, **kwargs)
        
        else:
            axes.scatter(xy[0,:], xy[1,:], zorder=10)

        return None
    



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import Templates as Temp
    from ShapeShadow import Sector
    from dotenv import load_dotenv
    import DXF
    import os

    load_dotenv()

    stage_file = os.getenv('STAGE_FILE')    
    x = [0, 0, 1, 1]
    y = [0, 1, 1, 0]

    
    sector = Sector(radius=2*2.54, sweep_angle=90)
    
    spot = Spot(
        beam_diameter=0.3, 
        angle_incident=65
    )
    mp = MapPattern(
        x=x, 
        y=y, 
        x_offset=0.5, 
        y_offset=2.5, 
        theta_offset=41
    )

    sc = SpotCollection(mp, spot)

    fig, ax = plt.subplots()
    
    DXF.plot(stage_file, ax, **Temp.STAGE)

    sector.plot(ax, as_patch=True, **Temp.SAMPLE)

    sc.plot(ax, as_ellipse=True, **Temp.SPOT)

    ax.scatter(x, y)

    ax.set_aspect("equal")
    plt.show()
