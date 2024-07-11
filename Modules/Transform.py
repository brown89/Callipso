import numpy as np



def check_dim(array:np.ndarray) -> bool:
    """
    Pre-check for type and dimensionality
    Checks:
    - is Numpy nparray
    - dimensions [2, N]
    """
    if not isinstance(array, np.ndarray):
        raise ValueError(f"Expeced numpy.array, was given: {type(array)}")
    
    if array.shape[0] != 2:
        return False
    else:
        return True
        


def rotate(xy:np.ndarray, angle:float) -> np.ndarray:
    """
    Rotates a Numpy array [2, N] 'angle' degree around (0, 0)
    xy: np.ndarray dimension [2, N] containing x and y coordinates
    angle: float rotational angle in degrees
    return: rotated version of xy
    """
    check_dim(xy)

    def rotator(array2d:np.ndarray) -> np.ndarray:
        rad = np.deg2rad(angle)
        A = np.array([
            [np.cos(rad), -np.sin(rad)],
            [np.sin(rad), np.cos(rad)]
        ])
        return A.dot(array2d)
    
    return np.apply_along_axis(rotator, axis=0, arr=xy)
    
    

def translate(xy:np.ndarray, offset:np.ndarray) -> np.ndarray:
    """
    Translates Numpy array [2, N] 'offset' amount
    xy: np.ndarray dimension [2, N] containing x and y coordinates
    offset: np.ndarray dimension [2, 1] containing offset
    return: translated version of xy
    """
    check_dim(xy)
    
    def translator(array2d:np.ndarray) -> np.ndarray:
        return offset + array2d
        
    return np.apply_along_axis(translator, axis=0, arr=xy)

