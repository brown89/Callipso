import os
import re
import pandas as pd

SUPPORTED_FILE_EXTENSIONS = ['*.txt']

BEAM_SIZE_WITH_FOCUS_PROBES = 0.03
BEAM_SIZE_WITHOUT_FOCUS_PROBES = 0.3


def is_valid(filename):
    """
    Function for validating file. Can raise one of two errors:
    
    FileNotFoundError if file does not exist
    -or-
    ValueError if file type not supported
    """
    
    # Check if 'file_path' is valid
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Could not find file:\n{filename}")
    
    # Check for correct file extension
    _, file_extension = os.path.splitext(filename)
    if file_extension not in '\t'.join(SUPPORTED_FILE_EXTENSIONS):
        raise ValueError(f"Unsupported file type, supported files are; {SUPPORTED_FILE_EXTENSIONS}, were given; {file_extension}.")
    
    return True


def read_text_file(filename):
    # Read in file to DataFrame
    data = pd.read_csv(filename, sep="\t", header=0, skiprows=range(1, 7))
    
    # Add x and y column
    x_list, y_list = [], []
    for xy in data.iloc[:, 0].values.tolist():
        x, y = re.findall(r"[-+]?(?:\d*\.*\d+)", xy)
        
        x_list.append(float(x))
        y_list.append(float(y))

    data['x'] = x_list
    data['y'] = y_list

    # Drops 1st column
    data.drop(columns=data.columns[0], axis=1,  inplace=True)

    # Rename all columns
    new_names = {name: name.strip() for name in data.columns}
    data.rename(columns=new_names, inplace=True)

    print("Column names:")
    for col_name in new_names:
        print(f"- {col_name}")
    
    return data

class JAW:
    def __init__(self, file_path: str):

        is_valid(file_path)  # Validate file

        self.file_path = file_path
        self.name = os.path.basename(file_path)
        self.data = read_text_file(file_path)



