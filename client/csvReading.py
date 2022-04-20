"""!
Convert Data to csv
"""
from usbCommunication import Data


def data_to_csv_string(data: Data) -> str:
    """!
    Convert data object to a csv string.

    @param data What data to write.

    @return Data converted to a string.
    """
    csvString = "\"Tid(s)\",\"Bevegelse (mm)\""
    for element in data:
        csvString += f'\n{element[0]},{element[1]}'

    return csvString
