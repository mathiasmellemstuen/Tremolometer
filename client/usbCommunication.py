"""!
Handles the USB communication between the application and microcontroller. Code in this module is running inside it's
own thread.
"""
from typing import Optional, List, Any
from customTypes import Data
from serial.tools.list_ports_common import ListPortInfo
import time
import serial.tools.list_ports
import serial
import base64
import os
import math


class USBCommunication:
    """!
    Handle USB communication with microcontroller.
    """

    def __init__(self, config) -> None:
        """!
        Constructor of the USBCommunication class.

        @param self Pointer to self.
        """

        ## Holds a serial connection object that represents the serial connection over USB to the microcontroller.
        self.connection = None

        ## Configuration from the configuration file (config.yaml)
        self.config = config

        ## Comport prefix (nt if the os is windows and /dev/ if the os is linux or macOS)
        self.connection_port_prefix = "" if os.name == "nt" else "/dev/"

    def search_for_comport(self) -> Optional[ListPortInfo]:
        """!
        Find the COM port the device is connected to.
        Test all COM ports to find the port the microcontroller is connected to.
        This is determined by sending a byte (b'!'), then checking if the received byte is the same (b'!').

        @param self Pointer to self.
        """
        for port in serial.tools.list_ports.comports():
            try:
                full_port = self.connection_port_prefix + port.name
                temp_connection = serial.Serial(port=full_port, parity=serial.PARITY_ODD, timeout=4, writeTimeout=4,
                                                baudrate=115200)
                time.sleep(0.1)
                temp_connection.flush()
                temp_connection.write("!".encode())
                time.sleep(0.1)
                input = temp_connection.read(temp_connection.inWaiting())

                if input == b'':
                    temp_connection.close()
                    continue

                if input == b'!':
                    self.connection = temp_connection
                    self.connection.flush()
                    return port

                temp_connection.close()

            except Exception as e:
                print(e)
                continue

        return None

    def check_if_device_is_connected(self) -> bool:
        """!
        Check if the microcontroller is connected.

        @param self Pointer to self.

        @return True if we have a serial connection
        """
        return self.connection is not None

    def ping(self) -> tuple[bool, bytes]:
        try:
            time.sleep(1)
            self.connection.write("!".encode())
            time.sleep(1)
            input_data = self.connection.read(self.connection.inWaiting())
            if input_data == b'!':
                return True, b'0'
            else:
                return False, input_data
        except Exception as e:
            print(e)
            self.connection = None
            return False, b'0'

    def send_start_signal(self) -> None:
        """!
        Send start signal to the microcontroller.

        @param self Pointer to self.
        """
        self.connection.flush()
        t = self.config["maaletid"]
        self.connection.write(f'{chr(self.config["maaletid"] + 34)}'.encode())

    def send_exit_signal(self) -> None:
        """!
        Send an exit signal to the microcontroller.

        @param self Pointer to self.
        """
        try:
            self.connection.flush()
            self.connection.write(" ".encode())
        except Exception as e:
            print(e)
            print("Could not send stopping signal. Exiting")

    def read(self) -> Optional[List[Data]]:
        """!
        Read data sent from the microcontroller.

        @param self Pointer to self.

        @return List of the data measurement or None.
        """
        if self.connection is None:
            return None

        if self.connection.inWaiting() > 0:
            return self.read_from_data(self.connection.read(self.calc_buffer_size(self.config['antallPakker'], 10)))
        return None

    def read_from_data(self, buffer: bytes) -> Optional[List[Data]]:
        """!
        Convert raw data form microcontroller to array of data points.

        @param self Pointer to self.
        @param buffer Raw data form microcontroller, formatted in base-64.

        @return List of the data measurement.
        """
        num_packages = int(self.config['antallPakker'])
        input = buffer
        bytes = base64.b64decode(input)
        data = []
        for i in range(num_packages):
            t = int.from_bytes(bytes[10 * i + 0: 10 * i + 4], byteorder="big", signed=False)
            x = int.from_bytes(bytes[10 * i + 4: 10 * i + 6], byteorder="big", signed=True)
            y = int.from_bytes(bytes[10 * i + 6: 10 * i + 8], byteorder="big", signed=True)
            z = int.from_bytes(bytes[10 * i + 8: 10 * i + 10], byteorder="big", signed=True)

            data.append((t, x, y, z))
        return data

    @staticmethod
    def calc_buffer_size(input_len: int, package_size: int) -> int:
        return math.ceil(4 * (((input_len * package_size) + 2) / 3))
