from abc import ABC, abstractmethod
from matplotlib.axes import Axes
from matplotlib import patches


class Shape(ABC):
    def __init__(self) -> None:
        return None
    

    @abstractmethod
    def get_patch(self) -> patches.Patch:
        pass


    def plot(self, axes:Axes) -> None:
        axes.add_patch(self.get_patch())

        return None


class Circle(Shape):
    def __init__(self, x:float, y:float, radius: float, **kwargs) -> None:
        self.center = [x, y]
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
    def __init__(self, x:float, y:float, width:float, height:float, angle:float, **kwargs):
        self.center = [x, y]
        self.width = width
        self.height = height
        self.angle = angle
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


class Sector(Shape):
    def __init__(self, x:float, y:float, radius:float, start_angle:float, end_angle:float, **kwargs):
        self.center = [x, y]
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.kwargs = kwargs

        super().__init__()

    

    def get_patch(self) -> patches.Patch:
        return patches.Wedge(
            center=self.center,
            r=self.radius,
            theta1=self.start_angle,
            theta2=self.end_angle,
            **self.kwargs
        )



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
