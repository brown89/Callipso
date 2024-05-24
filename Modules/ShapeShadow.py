from abc import ABC, abstractmethod
import numpy as np
from matplotlib.axes import Axes
from matplotlib import patches



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
    


class Shape(ABC):
    def __init__(self) -> None:
        self.center: np.ndarray = np.array([0, 0]).T
        self.angle: float = 0
        
        return None
    

    @abstractmethod
    def get_patch(self) -> patches.Patch:
        pass


    def plot(self, axes:Axes) -> None:
        axes.add_patch(self.get_patch())

        return None
    

    def translate(self, x:float, y:float):
        offset = np.array([x, y]).T
        self.center = Transform.translate(self.center, offset)

        return self
    

    def rotate(self, angle:float):
        self.angle += angle

        return self
    


class Circle(Shape):
    def __init__(self, radius: float, **kwargs) -> None:
        self.radius = radius
        self.kwargs = kwargs

        super().__init__()
    

    def get_patch(self) -> patches.Patch:
        return patches.Circle(
            xy=self.center,
            radius=self.radius,
            **self.kwargs
        )
    


class Ellipse(Shape):
    def __init__(self, width:float, height:float, **kwargs):
        self.width = width
        self.height = height
        self.kwargs = kwargs

        super().__init__()

    

    def get_patch(self) -> patches.Patch:
        return patches.Ellipse(
            xy=self.center,
            width=self.width,
            height=self.height,
            angle=self.angle,
            **self.kwargs
        )
        


class Rectangle(Shape):
    def __init__(self, width:float, height:float, centered:bool=False, **kwargs):
        self.width = width
        self.height = height
        self.kwargs = kwargs
        
        super().__init__()

        if centered:
            self.center = self.center - np.array([self.width/2, self.height/2]).T

    

    def get_patch(self) -> patches.Patch:
        return patches.Rectangle(
            xy=self.center,
            width=self.width,
            height=self.height,
            angle=self.angle,
            **self.kwargs,
        )

class Sector(Shape):
    def __init__(self, radius:float, sweep_angle:float, **kwargs):
        self.radius = radius
        self.sweep_angle = sweep_angle
        self.kwargs = kwargs

        super().__init__()

    
    def get_patch(self) -> patches.Patch:
        return patches.Wedge(
            center=self.center,
            r=self.radius,
            theta1=self.angle,
            theta2=self.angle + self.sweep_angle,
            **self.kwargs
        )



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    kwargs = {'fill': False}
    circle = Circle(0.1, **kwargs)
    circle.translate([0.25, 0.5])
    ellipse = Ellipse(0.3, 0.45)
    ellipse.rotate(30).translate([-0.2, -0.125])

    fig, ax = plt.subplots()
    circle.plot(ax)
    ellipse.plot(ax)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_aspect("equal")

    plt.show()
