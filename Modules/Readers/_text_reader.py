import re
import pandas as pd


# Header renaming schema
HEAD_NAMES = {
    'Point #': 'n_points',
    'Z Align': 'z_align',
    'SigInt': 'sig_int',
    'Tilt X': 'tilt_x',
    'Tilt Y': 'tilt_y',
    'Hardware OK': 'hardware_ok',
    'MSE': 'mse',
    'Thickness # 1 (nm)': 'thickness_nm',
    'n of Cauchy @ 632.8 nm': 'n_cauchy_632nm',
    'A': 'a',
    'B': 'b',
    'C': 'c',
    'Fit OK': 'fit_ok', 
}


def first_line_of_data(filename:str, match_pattern:str) -> int:
    """
    Finds the line where data begins.
    """
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
    

def _extract_xy_coordinates_(dataframe:pd.DataFrame) -> pd.DataFrame:
    # Add x and y column
    x_list, y_list = [], []
    for xy in dataframe.iloc[:, 0].values.tolist():
        x, y = re.findall(r"[-+]?(?:\d*\.*\d+)", xy)
        
        x_list.append(float(x))
        y_list.append(float(y))

    # Setting new columns with x and y values
    dataframe['x'] = x_list
    dataframe['y'] = y_list

    return dataframe


def text_reader(filename:str) -> pd.DataFrame:

    # Find where data starts
    start_of_data = first_line_of_data(filename, '(')

    # Read file into DataFrame
    data = pd.read_csv(filename, sep="\t", header=0, skiprows=range(1, start_of_data))
    
    # Extract x and y coordinates
    data = _extract_xy_coordinates_(data)

    # Drops 1st column with old (x, y) coordinates
    data.drop(columns=data.columns[0], axis=1,  inplace=True)

    data.rename(mapper=str.strip, axis='columns')

    return data.rename(mapper=HEAD_NAMES, axis='columns')
