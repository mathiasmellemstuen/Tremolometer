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
    csv_string = "\"Tid(s)\",\"Bevegelse (mm)\""
    for element in data:
        csv_string += f'\n{element[0]},{element[1]}'

    return csv_string
