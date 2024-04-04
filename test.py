import numpy as np
import matplotlib.pyplot as plt

from Modules.ShapeShadow import Ellipse, Mask



def sector_mask(x:list, y:list, radius:float) -> list:
    """
    a**2 + b**2 = c**2
    """

    r2 = radius**2

    idx = []
    for i, (xi, yi) in enumerate(zip(x, y)):
        if r2 < (xi**2 + yi**2):
            idx.append(i)
    
    for i in sorted(idx, reverse=True):
        x.pop(i)
        y.pop(i)

    return x, y


def plot_lots_of_ellipse():
    x_range = np.linspace(0, 5, 25)
    y_range = np.linspace(0, 5, 25)

    x_coor = []
    y_coor = []
    for x in x_range:
        for y in y_range:
            x_coor.append(x)
            y_coor.append(y)

    x, y = sector_mask(x_coor, y_coor, 5)
    mask = Mask(x, y)
    mask.rotate(225)

    fig, ax = plt.subplots()

    for x, y in zip(mask.x, mask.y):
        ellipse = Ellipse(0.12, 0.03)
        ellipse.translate(x, y)
        ax.plot(ellipse.x, ellipse.y, '-k')

    ax.set_aspect('equal')  # Set the aspect 1:1
    plt.show()


if __name__ == '__main__':
    print("Yellow")
