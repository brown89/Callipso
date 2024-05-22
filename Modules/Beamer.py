import numpy as np
from matplotlib.axes import Axes


if __name__ == '__main__':
    from ShapeShadow import Ellipse

else:
    from Modules.ShapeShadow import Ellipse


class Transform:

    @staticmethod
    def check_dim(array:np.ndarray) -> bool:
        if not isinstance(array, np.ndarray):
            raise ValueError(f"Expeced numpy.array, was given: {type(array)}")
        
        if array.shape[0] != 2:
            return False
        else:
            return True
        

    @staticmethod
    def rotate(center:np.ndarray, angle:float) -> list[float, float]:
        Transform.check_dim(center)

        def rotator(array2d:np.ndarray) -> np.ndarray:
            rad = np.deg2rad(angle)
            A = np.array([
                [np.cos(rad), -np.sin(rad)],
                [np.sin(rad), np.cos(rad)]
            ])

            return A.dot(array2d)
        
        return np.apply_along_axis(rotator, axis=0, arr=center)
    
    
    @staticmethod
    def translate(center:np.ndarray, offset:list[float, float]) -> np.ndarray:
        Transform.check_dim(center)

        def translator(array2d:np.ndarray) -> np.ndarray:
            return offset + array2d
        
        return np.apply_along_axis(translator, axis=0, arr=center)
    

    


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


    @staticmethod
    def major(angle_incident:float, minor:float) -> float:
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
        
        self.diameter = beam_diameter
        self.angle_incident = angle_incident
        
        return None
    
    
    def elongation(self) -> float:
        """
        Return: elongation of the spot
        """
        
        return Spot.major(self.angle_incident, self.diameter)
    

    def get_patch(self, x:float, y:float, **kwargs) -> Ellipse:
        kwargs = {
            'fill': False,
            'edgecolor': 'k',
            'linewidth': 1,
            'zorder': 1,
        }
        ellipse = Ellipse(x, y, self.elongation(), self.diameter, 0, **kwargs)
        
        return ellipse
    

    def plot(self, axes:Axes, x:float, y:float, **kwargs) -> None:
        axes.add_patch(self.get_patch(x, y, **kwargs))

        return None
    

    def area(self) -> float:
        """
        Return the area of the spot
        """
        return np.pi * self.diameter * self.elongation()

    

class MapPattern:
    def __init__(self, xy:np.ndarray, xy_offset:np.ndarray, theta_offset:float) -> None:
        """
        x: x coordinates of the map pattern 
        y: y coordinates of the map pattern
        x_offset: x offset
        y_offset: y offset
        theta_offset: theta angle offset in degrees
        """
        
        self.xy = xy
        self.xy_offset = xy_offset
        self.t_offset = theta_offset

        return None
    

    def count(self) -> int:
        """
        Returns the number of measurements
        """
        
        return len(self.x)
    

    def xy_instrument(self):
        xy = self.xy

        xy = Transform.rotate(xy, self.t_offset)
        xy = Transform.translate(xy, self.xy_offset)

        return xy


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
                ellipse = Ellipse(width=major, height=minor, **kwargs)  # Creating object
                ellipse.translate(row)  # Centering ellipse on map pattern

                ellipse.plot(axes)
        
        else:
            axes.scatter(xy[0,:], xy[1,:])

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
    xy = np.array([
        [0, 0, 1, 1],
        [0, 1, 1, 0]
        ])
    
    sector = Sector(radius=2*2.54, sweep_angle=90, **Temp.SAMPLE)
    
    spot = Spot(beam_diameter=0.3, angle_incident=65)
    mp = MapPattern(xy, np.array([0.5, 2.5]), theta_offset=41)

    sc = SpotCollection(mp, spot)

    fig, ax = plt.subplots()
    
    DXF.plot(stage_file, ax, **Temp.STAGE)

    sector.plot(ax)

    sc.plot(ax, as_ellipse=True, **Temp.SPOT)

    ax.scatter(xy[0, :], xy[1, :])

    ax.set_aspect("equal")
    plt.show()
