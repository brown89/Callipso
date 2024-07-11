from abc import ABC, abstractmethod
import numpy as np
from matplotlib.axes import Axes
from matplotlib import patches


if __name__ == '__main__':
    from Transform import rotate, translate

else:
    from Modules.Transform import rotate, translate


class Shape(ABC):
    """
    Base class for shapes
    """
    def __init__(self) -> None:
        self.center: np.ndarray = np.array([0, 0]).T
        self.angle: float = 0
        
        return None
    
    @abstractmethod
    def area(self) -> float:
        """
        Returns the area of the shape
        """
        pass

    @abstractmethod
    def get_patch(self, **kwargs:dict) -> patches.Patch:
        """
        Returns a Matplotlib patch object
        """
        pass


    @abstractmethod
    def get_x(self) -> list[float]:
        """
        Returns a list of x coordinates of the shape
        """
        pass


    @abstractmethod
    def get_y(self) -> list[float]:
        """
        Returns a list of y coordinates of the shape
        """
        pass


    def _plot_as_scatter_(self, axes, **kwargs:dict) -> None:
        """
        Plot shape object as a scatter or line plot
        """
        axes.plot(self.get_x(), self.get_y(), **kwargs)
        return None


    def plot(self, axes:Axes, as_patch:bool=False, **kwargs:dict) -> None:
        """
        Plot shape as a patch or line/scatter plot

        axes: axes handle to plot in/on
        as_patch: boolean whether to plot as patch or scatter
        """

        if as_patch:
            axes.add_patch(self.get_patch(**kwargs))
        
        else:
            self._plot_as_scatter_(axes, **kwargs)

        return None
    

    def translate(self, x:float, y:float):
        """
        Translates the shape with offset (x,y)
        """
        offset = np.array([x, y]).T
        self.center = translate(self.center, offset)

        return self
    

    def rotate(self, angle:float):
        """
        Rotates the shape 'angle' degrees around (0,0)
        """
        self.angle += angle

        return self
    


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        """
        Circle implementation of 'Shape', centered in (0,0).

        - radius: radius of the circle
        """
        self.radius = radius
        
        super().__init__()


    def area(self) -> float:
        return np.pi * self.radius**2

    def get_x(self) -> list[float]:
        angle = np.linspace(0, 2*np.pi, int(360/15), endpoint=True)

        return [np.cos(a) * self.radius + self.center[0] for a in angle]
    
    
    def get_y(self) -> list[float]:
        angle = np.linspace(0, 2*np.pi, int(360/15), endpoint=True)

        return [np.sin(a) * self.radius + self.center[1] for a in angle]
    

    def get_patch(self, **kwargs) -> patches.Patch:
        return patches.Circle(
            xy=self.center,
            radius=self.radius,
            **kwargs
        )
    


class Ellipse(Shape):
    def __init__(self, width:float, height:float):
        """
        Ellipse implementation of 'Shape'.
        Centered on (0,0).

        - width: length along x axis
        - height: length along y axis
        """
        self.width = width
        self.height = height

        super().__init__()

    
    def get_patch(self, **kwargs) -> patches.Patch:
        return patches.Ellipse(
            xy=self.center,
            width=self.width,
            height=self.height,
            angle=self.angle,
            **kwargs
        )
    
    
    def _xy_(self):
        angle = np.linspace(0, 2*np.pi, int(360/15), endpoint=True)

        x = [0.5 * self.width * np.cos(a) for a in angle]
        y = [0.5 * self.height * np.sin(a) for a in angle]
        
        return x, y
    

    def area(self) -> float:
        return np.pi * self.width * self.height
    

    def get_x(self) -> list[float]:
        
        x_coor, y_coor = self._xy_()
        rad = np.deg2rad(self.angle)

        return [x * np.cos(rad) - y * np.sin(rad) + self.center[0] for x, y in zip(x_coor, y_coor)]
        

    def get_y(self) -> list[float]:
        
        x_coor, y_coor = self._xy_()
        rad = np.deg2rad(self.angle)

        return [y * np.cos(rad) + x * np.sin(rad) + self.center[1] for x, y in zip(x_coor, y_coor)]



class Rectangle(Shape):
    def __init__(self, width:float, height:float, centered:bool=False):
        """
        Rectangle implementation of 'Shape'.
        Lower left corner in (0,0), with option to center around (0,0).
        """
        self.width = width
        self.height = height

        self.centered = centered
        
        super().__init__()

    
    def _xy_(self):
        x = [0, self.width, self.width, 0, 0]
        y = [0, 0, self.height, self.height, 0]

        coor = np.array([x, y])

        if self.centered:
            coor = translate(
                coor, 
                np.array([
                    -.5*self.width, 
                    -.5*self.height
                ])
            )

        coor = rotate(coor, self.angle)
        coor = translate(coor, self.center)

        return coor
    

    def area(self) -> float:
        return self.width * self.height
    
    def get_x(self) -> list[float]:
        coor = self._xy_()

        return coor[0, :]
    

    def get_y(self) -> list[float]:
        coor = self._xy_()

        return coor[1, :]
    
    
    def get_patch(self, **kwargs) -> patches.Patch:

        if self.centered:
            center = rotate(
                np.array([
                    -.5 * self.width,
                    -.5 * self.height
                ]),
                self.angle
            )

            center = translate(center, self.center)
        
        else:
            center = self.center
        

        return patches.Rectangle(
            xy=center,
            width=self.width,
            height=self.height,
            angle=self.angle,
            **kwargs
        )



class Sector(Shape):
    def __init__(self, radius:float, sweep_angle:float):
        """
        Sector implementation of 'Shape'.
        Centered in (0,0).
        
        - radius: radius of the sector
        - sweep_angle: sweep angle of the sector arc
        """
        self.radius = radius
        self.sweep_angle = sweep_angle
        
        super().__init__()

    
    def area(self) -> float:
        return self.sweep_angle/360 * np.pi * self.radius**2
    
    
    
    def get_patch(self, **kwargs) -> patches.Patch:
        return patches.Wedge(
            center=self.center,
            r=self.radius,
            theta1=self.angle,
            theta2=self.angle + self.sweep_angle,
            **kwargs
        )
    

    def _get_angle_(self, n_points) -> list[float]:
        a_start = np.deg2rad(self.angle)
        a_stop = np.deg2rad(self.angle + self.sweep_angle)

        return np.linspace(a_start, a_stop, n_points)
    

    def get_x(self) -> list[float]:
        x = [self.center[0]]        
        angle = self._get_angle_(9)
        
        x.extend([np.cos(a) * self.radius + self.center[0] for a in angle])
        
        return x + [self.center[0]]
        
    
    def get_y(self) -> list[float]:
        y = [self.center[1]]
        angle = self._get_angle_(9)
        
        y.extend([np.sin(a) * self.radius + self.center[1] for a in angle])

        return y + [self.center[1]]
    


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    circle = Circle(
        radius=0.5
    )

    # Ellipse
    ellipse = Ellipse(
        width=2, 
        height=1
    )
    ellipse.angle = 16
    ellipse.translate(0, -0.5)

    # Rectangle
    rectangle = Rectangle(
        width=1,
        height=2,
        centered=True
    )
    rectangle.angle = 30
    rectangle.translate(-.73, -.85)
    
    # Sector
    sector = Sector(0.75, 90)
    sector.angle = -20
    sector.translate(.5, -.42)
    


    # Plotting
    fig, ax = plt.subplots()
    circle.plot(ax)
    circle.plot(ax, as_patch=True)
    
    keywords = {
        'edgecolor': 'g',
        'facecolor': 'wheat',
        'alpha': 0.3,
    }
    ellipse.plot(ax, color='r')
    ellipse.plot(ax, as_patch=True, **keywords)

    rectangle.plot(ax, color='k', alpha=0.5)
    rectangle.plot(ax, as_patch=True)

    sector.plot(ax)
    sector.plot(ax, as_patch=True)

    """
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    """
    ax.set_aspect("equal")

    plt.show()
