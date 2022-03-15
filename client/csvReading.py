def data_to_csv_string(data):
    csvString = "\"Tid(s)\",\"Bevegelse (mm)\""
    for element in data:
        csvString += f'\n{element[0]},{element[1]}'

    return csvString
