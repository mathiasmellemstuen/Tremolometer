import serial.tools.list_ports
import serial
import base64

class USBCommunication:
    def __init__(self):
        self.connection = None

    def search_for_comport(self):

        for port in serial.tools.list_ports.comports():
            if "COM4" in str(port.description):
                if self.connection is None:
                    self.connection = serial.Serial(port=port.name, parity=serial.PARITY_NONE, baudrate=9600)
                return port

        self.connection = None

        return None

    def check_if_device_is_connected(self):
        return self.search_for_comport() is not None

    def send_start_signal(self):
        self.connection.flush()
        self.connection.write(b"1")

    def read(self):
        if self.connection is None:
            return
        if self.connection.inWaiting() > 0:
            input = self.connection.read(16)
            bytes = base64.b64decode(input)
            print(bytes)

            time = int.from_bytes(bytes[0:4], byteorder="big", signed=False)
            x = int.from_bytes(bytes[4:6], byteorder="big", signed=True)
            y = int.from_bytes(bytes[6:8], byteorder="big", signed=True)
            z = int.from_bytes(bytes[8:10], byteorder="big", signed=True)
            print(f'Time: {time} x: {x} y: {y} z: {z}')
            return time, x, y, z

        return None, None, None, None