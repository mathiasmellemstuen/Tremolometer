import serial.tools.list_ports
import serial
import base64

class USBCommunication:
    def __init__(self):
        self.connection = None

    def search_for_comport(self):

        for port in serial.tools.list_ports.comports():
            if "Pico" in str(port.description):
                if self.connection is None:
                    self.connection = serial.Serial(port= "/dev/" + port.name, parity=serial.PARITY_NONE)
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
            return None

        if self.connection.inWaiting() > 0:
            input = self.connection.read(1336)
            bytes = base64.b64decode(input)
            data = []

            for i in range(100):
                time = int.from_bytes(bytes[10 * i + 0: 10 * i + 4], byteorder="big", signed=False)
                x = int.from_bytes(bytes[10 * i + 4 : 10 * i + 6], byteorder="big", signed=True)
                y = int.from_bytes(bytes[10 * i + 6 : 10 * i + 8], byteorder="big", signed=True)
                z = int.from_bytes(bytes[10 * i + 8 : 10 * i + 10], byteorder="big", signed=True)
                data.append((time, x, y, z))
            return data
        return None