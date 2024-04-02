import numpy as np

def area_ellipse(radius:float, grazing_angle:float) -> float:
    """
    Method for calculating the cross-sectional area of a cylinder at an angle i.e. ellipse
    
    radius: radius of the incident beam
    angle: angle between beam and plane normal

    return: area of ellipse
    """

    if grazing_angle >= 90:
        raise ValueError("Grazing angle must be less than 90")

    return np.pi * radius**2 / np.cos(np.deg2rad(grazing_angle))


def ellipse_ratio(minor:float, theta:float) -> float:
    """
    Function for calculating the ratio between minor axis in a ellipse to the angle of incedense
    
    minor: minor axis of ellipse
    theta: angle of incedense

    return: major axis of ellipse
    """
    return minor / np.cos(np.deg2rad(theta))


def test_area_ellipse():
    angles = [0, 25, 35, 45, 55, 65, 75, 80, 85, 89]

    for angle in angles:
        area = area_ellipse(1, angle)

        print(f"Angle: {angle:.1f}, area: {area:.1f}")


def test_ab_ratio():
    angles = [0, 10, 30, 65, 75]

    for angle in angles:
        b = ellipse_ratio(minor=300, theta=angle)

        print(f"300:{b:.2f}, angle: {angle:.2f}")

if __name__ == '__main__':
    test_ab_ratio()