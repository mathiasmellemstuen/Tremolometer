import serial.tools.list_ports
import serial

device_was_connected = False
comport = None
serialConnection = None

def search_for_comport():

    for port in serial.tools.list_ports.comports():
        if "Pico" in str(port.description):
            return port
    return None

def check_if_device_is_connected():
    return search_for_comport() is not None

def sendStartSignal():
    global serialConnection
    serialConnection.flush()

    serialConnection.write(b"1")

def readFromSerialConnection():

    global serialConnection
    global data

    if serialConnection is None:
        return

    if serialConnection.inWaiting() > 0:
        bytes = serialConnection.read(10)

        time = int.from_bytes(bytes[:4], byteorder="big", signed=False)
        x = int.from_bytes(bytes[4:6], byteorder="big", signed=True)
        y = int.from_bytes(bytes[6:8], byteorder="big", signed=True)
        z = int.from_bytes(bytes[8:10], byteorder="big", signed=True)

        print(f'Time: {time} x: {x} y: {y} z: {z}')