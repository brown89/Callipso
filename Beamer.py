import numpy as np

def area_ellise(radius:float, grazing_angle:float) -> float:
    """
    Method for calculating the cross-sectional area of a cylinder at an angle i.e. ellipse
    
    radius: radius of the incident beam
    angle: angle between beam and plane normal
    """

    if grazing_angle >= 90:
        raise ValueError("Grazing angle must be less than 90")

    return np.pi * radius**2 / np.cos(np.deg2rad(grazing_angle))


if __name__ == '__main__':
    angles = [0, 25, 35, 45, 55, 65, 75, 80, 85, 89]

    for angle in angles:
        area = area_ellise(1, angle)

        print(f"Angle: {angle:.1f}, area: {area:.1f}")
