import os
import pandas as pd

from Readers._text_reader import text_reader
from Readers._scan_reader import ScanFile, scan_reader


# Ellipsometer specific constants
BEAM_SIZE_WITH_FOCUS_PROBES = 0.03
BEAM_SIZE_WITHOUT_FOCUS_PROBES = 0.3


def is_valid(filename:str) -> bool:
    """
    Function for validating file and extension is supported.
    
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


#----------------------------------------------------------------
# *.txt file reader
#----------------------------------------------------------------

# Types of supported file formats
SUPPORTED_FILE_EXTENSIONS = [
    '*.txt',
]


def read_text_file(filename:str) -> pd.DataFrame:
    """
    Function for reading the text version of the J.A.Woollam *.SE files

    Headers are renamed according with the HEAD_NAMES

    NOTE: The x and y coordinates are extracted from the 1st column and saved in an x and y column.
    """

    # Check if filename is valid
    is_valid(filename)

    dataframe = text_reader(filename)

    return dataframe


#----------------------------------------------------------------
# *.SCAN file_reader
#----------------------------------------------------------------


def read_scan_file(filename:str) -> ScanFile:

    # Check validity of file
    is_valid(filename)

    scan_file = scan_reader(filename)

    return scan_file
