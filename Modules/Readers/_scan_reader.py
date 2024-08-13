from abc import ABC
import re


class XY(ABC):
    def __init__(self, x:float|list[float], y:float|list[float]):
        """
        Base class for holding x and y coordinates
        """
        
        self.x = x
        self.y = y


class SubstrateDimensions(XY):
    OPTIONS = {
        0: 'Circle',
        1: 'Rectangle',
        2: 'Rectangle, (0,0) at corner'
    }

    def __init__(self, x:float, y:float, shape:int, diameter:float, draw_wafer_notch:bool=False):
        """
        Data structure for 'Substrate Dimensions'

        x: width of the sample (applicable only to rectangular samples)
        y: height of the sample (applicable only to rectangular samples)
        shape: selected shape (0:Circle, 1:Rectangle, 2:Rectangle, (0,0) at corner)
        diameter: diameter of the sample (applicable only to circular samples)
        draw_wafer_notch: option to draw the wafer notch
        """

        self.shape = shape
        self.diameter = diameter
        self.draw_wafer_notch = draw_wafer_notch

        super().__init__(x, y)


class Alignment(XY):
    OPTIONS = {
        0: 'Align at this position only',
    }

    def __init__(self, x:float, y:float, option:int):
        """
        Data structure for 'Alignment'

        x: x alignment
        y: y alignment
        option: option where to align (0:Align at this position only, 1:Align in all points???)
        """
        self.option = option
        
        super().__init__(x, y)


class Offsets(XY):
    def __init__(self, x:float, y:float, theta:float, use_initial_position:bool=False):
        """
        Data structure for 'Offsets'

        x: x offset
        y: y offset
        theta: theta offset
        use_initial_position: 
        """
        self.theta = theta
        self.use_initial_position = use_initial_position

        super().__init__(x, y)


class ScanPoints(XY):
    def __init__(self, x:list[float], y:list[float], z:list[float]):
        self.z = z
        
        super().__init__(x, y)


class TransmissionBaseline(XY):
    def __init__(self, x:float, y:float, use_point_for_transmission_baseline:bool=False):
        self.use_point_for_transmission_baseline = use_point_for_transmission_baseline
    
        super().__init__(x, y)


class ScanFile:
    def __init__(
        self,
        substrate_dimensions:SubstrateDimensions,
        alignment:Alignment,
        offsets:Offsets,
        scan_points:ScanPoints,
        transmission_baseline:TransmissionBaseline,
        ):

        self.substrate_dimensions = substrate_dimensions
        self.alignment = alignment
        self.offsets = offsets
        self.scan_points = scan_points
        self.transmission_baseline = transmission_baseline


def _scanfile_to_dict(file:list[str]) -> dict:
    """
    Reads file into dictionary with properties as keys 
    and settings as values.
    """
    key = False
    data = {}

    # Looping lines of file
    for line in file:

        # Check if start entry, by matching 'start_' to line if
        # no 'key' is active
        if not key and "start_" in line:
            key = line.replace("start_", "").strip()
            data[key] = []
        
        # Check if end of entry, by matching 'end_' to line if
        # 'key' is active
        elif key and "end_" in line:
            if key in line:
                key = False
            
            else:
                data[key].append(line)
        
        # Appending data if key is active
        elif key:
            data[key].append(line)
    

    return data


def _text_to_bool(text:str) -> bool:
    """
    Converts a charater 'F' or 'T' to False or True respectively
    """
    if text.lower() == 'f':
        return False
    
    elif text.lower() == 't':
        return True
    
    else:
        return None
    

def scan_reader(filename:str) -> ScanFile:

    # Read file into memory
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    f.close()

    # Pull the file into dictionary with 'properties' as keys and
    # data as 'values'
    data = _scanfile_to_dict(lines)

    # Extract Substrate Dimensions
    sd = data["Substrate Dimensions"][0].strip().split("\t")
    substrate_dimensions = SubstrateDimensions(
        shape=int(sd[0]),
        diameter=float(sd[1]),
        draw_wafer_notch=_text_to_bool(sd[2]),
        x=float(sd[3]),
        y=float(sd[4]),
    )

    # Extract Alignment
    a = data["Alignment"][0].strip().split("\t")
    alignment = Alignment(
        option=int(a[0]),
        x=float(a[1]),
        y=float(a[2]),
    )

    # Extract Offsets
    off = data["Offsets"][0].strip().split("\t")
    offsets = Offsets(
        x=float(off[0]),
        y=float(off[1]),
        theta=float(off[2]),
        use_initial_position=_text_to_bool(off[3]),
    )

    # Extract x,y,z coordinates
    xyz = data["Scan Points"]
    """
    Explanation of the regex pattern:

        [+-]?   -> Matches an optional sign (+ or -) at the beginning of the number.
        \d*     -> Matches zero or more digits before the decimal point.
        \.?     -> Matches an optional decimal point.
        \d+     -> Matches one or more digits after the decimal point.
        (?:[eE][+-]?\d+)?   -> Matches the optional scientific notation part:
            (?: ... )   -> This is a non-capturing group. It groups part of the regex without 
                            creating a backreference (i.e., it doesn't store the match for later use).
            [eE]        -> Matches the letter e or E for scientific notation.
            [+-]?       -> Matches an optional sign (+ or -) for the exponent.
            \d+         -> Matches one or more digits for the exponent.
    """

    x_list = []
    y_list = []
    z_list = []
    for line in xyz[1:]:

        # Regular expression pattern
        pattern = r'[+-]?\d*\.?\d+(?:[eE][+-]?\d+)?'
        decimals = re.findall(pattern, line.strip())

        if len(decimals) == 3:
            x, y, z = decimals
            x_list.append(float(x))
            y_list.append(float(y))
            z_list.append(float(z))
        else:
            print(f'Error in interpreting: {line}')


    scan_points = ScanPoints(
        x=x_list, 
        y=y_list, 
        z=z_list,
    )


    # Extract transmission baseline
    tb = data["Transmission Baseline"][0]
    upft, x, y = tb.strip().split("\t")

    transmission_baseline = TransmissionBaseline(
        use_point_for_transmission_baseline=_text_to_bool(upft),
        x=float(x),
        y=float(y),
    )

    scan_file = ScanFile(
        substrate_dimensions=substrate_dimensions,
        alignment=alignment,
        offsets=offsets,
        scan_points=scan_points,
        transmission_baseline=transmission_baseline,
    )

    
    return scan_file
