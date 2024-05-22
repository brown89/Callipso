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
        self.center: np.ndarray = np.array([[0], [0]])
        self.angle: float = 0
        
        return None
    

    @abstractmethod
    def get_patch(self) -> patches.Patch:
        pass


    def plot(self, axes:Axes) -> None:
        axes.add_patch(self.get_patch())

        return None
    

    def translate(self, offset:np.ndarray):
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

    

    def get_patch(self, c=None) -> patches.Patch:
        return patches.Ellipse(
            xy=self.center,
            width=self.width,
            height=self.height,
            angle=self.angle,
            edgecolor='k',
            facecolor=None,
            **self.kwargs
        )
    

    def plot(self, axes:Axes, c=None) -> None:
        axes.add_patch(self.get_patch(c))

        return None
    

class Sector(Shape):
    def __init__(self, radius:float, sweep_angle:float, **kwargs):
        self.x = 0
        self.y = 0
        self.start_angle = 0

        self.radius = radius
        self.end_angle = sweep_angle
        self.kwargs = kwargs

        super().__init__()

    
    def rotate(self, angle:float):
        self.start_angle += angle
        self.end_angle += angle

        return self
    

    def translate(self, x_offset:float, y_offset:float):
        self.x += x_offset
        self.y += y_offset

        return self
    

    def get_patch(self) -> patches.Patch:
        return patches.Wedge(
            center=[self.x, self.y],
            r=self.radius,
            theta1=self.start_angle,
            theta2=self.end_angle,
            **self.kwargs
        )
    

    def plot(self, axes:Axes) -> None:
        axes.add_patch(self.get_patch())

        return None


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    kwargs = {'fill': False}
    circle = Circle(0.1, 0.25, 0.5, **kwargs)
    ellipse = Ellipse(-0.2, -0.125, 0.3, 0.45, 30)

    fig, ax = plt.subplots()
    circle.plot(ax)
    ellipse.plot(ax)

    ax.set_aspect("equal")
    plt.show()
