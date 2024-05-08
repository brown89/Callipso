import ezdxf
import ezdxf.entities
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Arc, Circle, Patch, Polygon


def add_arc(arc:ezdxf.entities.Arc) -> Patch:
    """
    Returns a matplotlib.patches.Arc object
    """
    center = (arc.dxf.center.x, arc.dxf.center.y)
    radius = arc.dxf.radius
    start_angle = arc.dxf.start_angle
    end_angle = arc.dxf.end_angle

    return Arc(
        center, 
        width=2*radius, 
        height=2*radius, 
        angle=0, 
        theta1=start_angle, 
        theta2=end_angle, 
        ec=(0, 0, 0, 0.5),
        fill=False,
        linewidth=0.5,
    )


def add_circle(circle:ezdxf.entities.Circle) -> Patch:
    center = (circle.dxf.center.x, circle.dxf.center.y)
    radius = circle.dxf.radius

    return Circle(
        xy=center,
        radius=radius,
        ec=(0, 0, 0, 0.5),
        fill=False,
        linewidth=0.5,
    )


def add_line(line:ezdxf.entities.Line) -> Patch:
    x_start, y_start = line.dxf.start.x, line.dxf.start.y
    x_end, y_end = line.dxf.end.x, line.dxf.end.y

    return Polygon(
        xy=[[x_start, y_start], [x_end, y_end]],
        closed=False,
        ec=(0, 0, 0, 0.5),
        fill=False,
        linewidth=0.5,
    )


def plot(dxf_filename:str, ax_handle:Axes) -> None:
    doc = ezdxf.readfile(dxf_filename)
    msp = doc.modelspace()

    for entity in msp:
        if entity.dxftype() == "ARC":
            arc = add_arc(entity)
            ax_handle.add_patch(arc)
        
        elif entity.dxftype() == "CIRCLE":
            circle = add_circle(entity)
            ax_handle.add_patch(circle)
        
        elif entity.dxftype() == "LINE":
            line = add_line(entity)
            ax_handle.add_patch(line)

    return None        