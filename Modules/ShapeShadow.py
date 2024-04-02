from abc import ABC, abstractmethod
import numpy as np


class Shape(ABC):
    def __init__(self) -> None:
        self.x: np.ndarray
        self.y: np.ndarray

        self._generate_()

        return None
    
    
    @abstractmethod
    def _generate_(self) -> None:
        """
        Method for generating initial base shape
        
        NOTE: abstract methods MUST be implemented in child class
        """
        
        pass
    
    
    @abstractmethod
    def area(self) -> float:
        """
        Method for calculating area of the shape
        
        NOTE: abstract methods MUST be implemented in child class
        """
        
        pass


    def rotate(self, angle: float):
        """
        Method for making rotational offset
        
        angle: degrees of rotation counter clockwise
        """
        
        xy = np.asarray([self.x, self.y])
        rad = np.deg2rad(angle)

        A = np.asarray(
            [[np.cos(rad), -np.sin(rad)],
            [np.sin(rad), np.cos(rad)]]
        )

        xy_rotated = np.dot(A, xy)

        self.x = xy_rotated[0,:]
        self.y = xy_rotated[1,:]

        return self
    
    
    def translate(self, x_offset: float, y_offset: float):
        """
        Method for making translational offset
        """
        
        self.x = self.x + x_offset
        self.y = self.y + y_offset

        return self
    


class Sector(Shape):
    def __init__(self, radius:float, angle_sweep:float) -> None:
        self.radius = radius
        self.angle_sweep = np.deg2rad(angle_sweep)

        super(Sector, self).__init__()

        return None
    
    
    def _generate_(self):
        n = np.linspace(
            start=0, 
            stop=self.angle_sweep, 
            num=int(self.angle_sweep * 12 / np.pi), 
            endpoint=True
        )

        x = np.cos(n) * self.radius
        y = np.sin(n) * self.radius

        x = np.insert(x, 0, 0)
        y = np.insert(y, 0, 0)

        self.x = np.append(x, 0)
        self.y = np.append(y, 0)

        return None
    

    def area(self) -> float:
        return (self.angle_sweep / 2) * self.radius ** 2
    
        

class Ellipse(Shape):
    def __init__(self, major: float, minor: float) -> None:
        self.major = major
        self.minor = minor

        super(Ellipse, self).__init__()

        return None
    

    def _generate_(self) -> None:
        a = np.linspace(0, 2*np.pi, 32+1, endpoint=True)

        self.x = np.cos(a) * self.major/2
        self.y = np.sin(a) * self.minor/2

        return None
    

    def area(self) -> float:
        return np.pi * self.major * self.minor



class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

        super(Circle, self).__init__()

        return None
    

    def _generate_(self) -> None:
        a = np.arange(0, 361, 15)

        self.x = np.cos(a) * self.radius
        self.y = np.sin(a) * self.radius

        return None
    

    def area(self) -> float:
        return np.pi * self.radius ** 2



class Rectangle(Shape):
    def __init__(self, width: float, height: float, centered: bool=True) -> None:
        self.width = width
        self.height = height
        self.centered = centered

        super(Rectangle, self).__init__()
    
    def _generate_(self) -> None:
        self.x = np.array([0, self.width, self.width, 0, 0])
        self.y = np.array([0, 0, self.height, self.height, 0])

        if self.centered:
            self.translate(-self.width/2, -self.height/2)
        
        return None
    

    def area(self) -> float:
        return self.width * self.height
    


class Square(Rectangle):
    def __init__(self, width: float, centered: bool=True) -> None:
        super(Square, self).__init__(width, width, centered)

        return None



def demo():
    import matplotlib.pyplot as plt
    
    n = 5

    angle = np.random.rand(n) * 90
    x_disp = np.random.rand(n) * 20 - 10
    y_disp = np.random.rand(n) * 20 - 10

    sector = Sector(radius=5, angle_sweep=45)
    sector.rotate(angle[0]).translate(x_disp[0], y_disp[0])

    rectangle = Rectangle(width=2, height=5)
    rectangle.rotate(angle[1]).translate(x_disp[1], y_disp[1])

    square = Square(width=3)
    square.rotate(angle[2]).translate(x_disp[2], y_disp[2])

    circle = Circle(radius=3)
    circle.translate(x_disp[3], y_disp[3])

    ellipse = Ellipse(major=3, minor=1)
    ellipse.rotate(angle[4]).translate(x_disp[4], y_disp[4])

    # Plotting figure
    fig, ax = plt.subplots()
    ax.plot(sector.x, sector.y, '-g', 
            alpha=0.5, 
            label=f"A: {angle[0]:.1f}, Tx: {x_disp[0]:.1f}, Ty: {y_disp[0]:.1f}"
        )
    ax.plot(rectangle.x, rectangle.y, '-r', 
            alpha=0.5, 
            label=f"A: {angle[1]:.1f}, Tx: {x_disp[1]:.1f}, Ty: {y_disp[1]:.1f}"
        )
    ax.plot(square.x, square.y, '-b', 
            alpha=0.5, 
            label=f"A: {angle[2]:.1f}, Tx: {x_disp[2]:.1f}, Ty: {y_disp[2]:.1f}"
        )
    ax.plot(circle.x, circle.y, '-k', 
            alpha=0.5, 
            label=f"A: {angle[3]:.1f}, Tx: {x_disp[3]:.1f}, Ty: {y_disp[3]:.1f}"
        )    
    ax.plot(ellipse.x, ellipse.y, '-m',
            alpha=0.5,
            label=f"A: {angle[4]:.1f}, Tx: {x_disp[4]:.1f}, Ty: {y_disp[4]:.1f}"
            )

    ax.set_aspect('equal')  # Set the aspect 1:1

    plt.legend()
    plt.show()

if __name__ == '__main__':
    demo()