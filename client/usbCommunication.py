import time

import serial.tools.list_ports
import serial
import base64
import config

class USBCommunication:
    def __init__(self):
        self.connection = None
        self.config = config.read_config("client/config.yaml")

    def search_for_comport(self):
        for port in serial.tools.list_ports.comports():
            try:
                temp_connection = serial.Serial(port="/dev/" + port.name, parity=serial.PARITY_NONE, timeout=1)
                time.sleep(0.1)
                temp_connection.flush()
                temp_connection.write("1".encode())
                time.sleep(0.1)
                input = temp_connection.read(temp_connection.inWaiting())

                if input == b'':
                    temp_connection.close()
                    continue

                if input == b'2':
                    self.connection = temp_connection
                    return port

                temp_connection.close()

            except Exception as e:
                print(e)
                continue

        return None

    def check_if_device_is_connected(self):
        return self.connection is not None

    def send_start_signal(self):
        self.connection.flush()
        self.connection.write(str(self.config["maaletid"]).encode())

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