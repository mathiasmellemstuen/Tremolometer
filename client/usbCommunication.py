import serial.tools.list_ports
import serial

class USBCommunication:
    def __init__(self):
        self.connection = None

    def search_for_comport(self):

        for port in serial.tools.list_ports.comports():
            if "Pico" in str(port.description):
                self.connection = serial.Serial(port=port.name, parity=serial.PARITY_NONE)
                return port

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
            bytes = self.connection.read(10)

            i = 0
            time = int.from_bytes(bytes[12 * i: 12 * i + 4], byteorder="little", signed=False)
            x = int.from_bytes(bytes[12 * i + 4: 12 * i + 6], byteorder="little", signed=True)
            y = int.from_bytes(bytes[12 * i + 6: 12 * i + 8], byteorder="little", signed=True)
            z = int.from_bytes(bytes[12 * i + 8: 12 * i + 10], byteorder="little", signed=True)
            print(f'Time: {time} x: {x} y: {y} z: {z}')
            return time, x, y, z

        return None, None, None, None