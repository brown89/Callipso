import os
import re
import pandas as pd


# Ellipsometer specific constants
BEAM_SIZE_WITH_FOCUS_PROBES = 0.03
BEAM_SIZE_WITHOUT_FOCUS_PROBES = 0.3

SUPPORTED_FILE_EXTENSIONS = ['*.txt']

DATA_HEAD_NAMES = {
    'Point #': 'n_points',
    'Z Align': 'z_align',
    'SigInt': 'sig_int',
    'Tilt X': 'tilt_x',
    'Tilt Y': 'tilt_y',
    'Hardware OK': 'hardware_ok',
    'MSE': 'mse',
    'Thickness # 1 (nm)': 'thickness_nm',
    'A': 'a',
    'B': 'b',
    'C': 'c',
    'Fit OK': 'fit_ok', 
}


def is_valid(filename:str) -> bool:
    """
    Function for validating file. Can raise one of two errors:
    
    FileNotFoundError if file does not exist
    -or-
    ValueError if file type not supported
    """
    
    # Check if 'filename' is valid
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Could not find file:\n{filename}")
    
    # Check for correct file extension
    _, file_extension = os.path.splitext(filename)
    if file_extension not in ', '.join(SUPPORTED_FILE_EXTENSIONS):
        raise ValueError(f"Unsupported file type, supported files are; {SUPPORTED_FILE_EXTENSIONS}, were given; {file_extension}.")
    
    return True


def first_line_of_data(filename:str, match_pattern:str) -> int:
    """
    Finds the line where data begins."""
    # Read file line by line
    with open(filename, 'r') as f:
        file = f.readlines()
    
    # Loops through lines in file
    start_of_data: int
    for i, line in enumerate(file):

        # Stops if first character is a match for 'match_pattern'
        if line[0] == match_pattern:
            start_of_data = i
            break
    
    return start_of_data
    


def read_text_file(filename:str) -> pd.DataFrame:
    """
    Read file and extracts x and y coordinates

    Returns a DataFrame
    """

    # Find where data starts
    start_of_data = first_line_of_data(filename, '(')

    # Read file into DataFrame
    data = pd.read_csv(filename, sep="\t", header=0, skiprows=range(1, start_of_data))
    
    # Add x and y column
    x_list, y_list = [], []
    for xy in data.iloc[:, 0].values.tolist():
        x, y = re.findall(r"[-+]?(?:\d*\.*\d+)", xy)
        
        x_list.append(float(x))
        y_list.append(float(y))

    # Setting new columns with x and y values
    data['x'] = x_list
    data['y'] = y_list

    # Drops 1st column with old (x, y) coordinates
    data.drop(columns=data.columns[0], axis=1,  inplace=True)

    return data



class JAW:
    def __init__(self, filename: str):

        is_valid(filename)  # Validate file

        self.filename = filename
        self.name = os.path.basename(filename)

        data = read_text_file(filename)
        self.data = data.rename(DATA_HEAD_NAMES)
