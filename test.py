import numpy as np
import matplotlib.pyplot as plt

from Modules.ShapeShadow import Ellipse, Mask, Sector
from Modules.Beamer import MapPattern, SpotCollection, Spot
from Modules.JAW import JAW


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
    import pandas as pd


    DATA_PATH = r"C:\Users\BjoernSchytzBruun\OneDrive - RadiSurf ApS\Dokumenter - Shared Drive\Working folders\Bjoern_WorkingFolder\Programming\Python\Ellipsometry\data\MPI003-1_fp_1143pt.txt"
    jaw = JAW(DATA_PATH)  # loads data
    jaw.data = jaw.data.dropna()

    # Setting up 'spot collection'
    map_pattern = MapPattern(jaw.data.x, jaw.data.y, x_offset=0, y_offset=0, theta_offset=0)
    spot = Spot(0.03, 75)
    spot_collection = SpotCollection(map_pattern, spot)

    # Pulling thickness from 'jaw' data
    thickness = jaw.data['Thickness # 1 (nm)']
    
    # Samples outline
    sector = Sector(2*2.54, 90)
    sector.rotate(225+5.1).translate(-0.0673, 0.4477)


    # Initiating figure
    fig, ax = plt.subplots()
    
    # Plotting sample outline
    ax.plot(sector.x, sector.y, '-b')

    # Applying offset to measurements
    x_mp, y_mp = spot_collection.map_pattern.offset()
    tric = ax.tricontourf(x_mp, y_mp, thickness, levels=10, cmap='jet')

    # Plotting spot outlines
    for spot in spot_collection.outlines():
        ax.plot(spot.x, spot.y, '-k', linewidth=1)
    

    ax.set_aspect('equal')
    ax.set_xlabel('cm')
    ax.set_ylabel('cm')

    fig.colorbar(tric)    
    plt.show()
"""
"""    