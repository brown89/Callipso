import numpy as np
import matplotlib.pyplot as plt

from Modules.ShapeShadow import Ellipse, Shape


class Mask(Shape):
    def __init__(self, x_coor:list, y_coor:list):
        self.x_coor = x_coor
        self.y_coor = y_coor

        super(Mask, self).__init__()


        return None
    

    def _generate_(self) -> None:
        self.x = np.asarray(self.x_coor)
        self.y = np.asarray(self.y_coor)

        return None
    

    def area(self) -> None:
        return None
    


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


if __name__ == '__main__':
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
