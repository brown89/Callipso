import numpy as np
import matplotlib.pyplot as plt

from Modules.ShapeShadow import Ellipse, Sector



if __name__ == '__main__':
    ellipse = Ellipse(major=1.2, minor=0.3)
    sector = Sector(radius=0.15, angle_sweep=90)

    fig, ax = plt.subplots()
    ax.plot(ellipse.x , ellipse.y, '.k')
    ax.plot(sector.x , sector.y, '.r')

    ax.set_aspect('equal')  # Set the aspect 1:1
    plt.show()
