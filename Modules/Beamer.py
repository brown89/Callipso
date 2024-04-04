import numpy as np


def _angle_check_(angle_incident) -> float:
    if angle_incident >= 90:
        angle_incident = angle_incident % 90
        
        print(f"WARNING: Grazing angle have been modulated to {angle_incident}")
    return angle_incident


def area(spot_diameter:float, angle_incident:float) -> float:
    """
    Return: area of the spot
    """
    angle_incident = _angle_check_(angle_incident)
    return np.pi * (spot_diameter/2)**2 / np.cos(np.deg2rad(angle_incident))


def elongation(spot_diameter:float, angle_incident:float) -> float:
    """
    Return: elongation of the spot
    """
    angle_incident = _angle_check_(angle_incident)
    return spot_diameter / np.cos(np.deg2rad(angle_incident))


    
class SpotCollection:
    def __init__(self, x_coordinates:np.ndarray, y_coordinates:np.ndarray, spot_diameter:float, angle_incident:float) -> None:
        self.x: np.ndarray = x_coordinates
        self.y: np.ndarray = y_coordinates

        self.angle_incident: float = angle_incident
        self.diameter: float = spot_diameter



if __name__ == '__main__':
    print("Yellow world")
