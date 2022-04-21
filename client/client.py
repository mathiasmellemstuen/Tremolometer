"""!
Handle the client.
"""
from typing import List
from costumeTyping import Data, Config
from interface import Interface
from config import read_config
from usbCommunication import USBCommunication
from tkinter.messagebox import showwarning
from timer import get_current_time_ms
import threading
import spectrogram

data = []

"""!Store data"""
config: Config = read_config("client/config.yaml")
usb_communication: USBCommunication = USBCommunication()
# Creating test data
#for i in range(0, 20000):
#    if i < 5000:
#        data.append((i, 1000 * math.sin(i * 0.006), 0, 0))
#    elif i > 10000:
#        data.append((i, 1000 * math.sin(i * 0.1), 0, 0))
#    else:
#        data.append((i, 1000 * math.sin(i * 0.02), 0, 0))
interface = Interface(config)
device_was_connected = False
measuring = False
run_usb_thread = True
last_packet_time = 0


def start_button() -> None:
    """
    Start communication with microcontroller if it is connected.

    """
    global measuring

    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
        measuring = True
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")


def usb_thread() -> None:
    """
    Draws data sent form the accelerometer to the plot on the GUI.

    """
    global last_packet_time

    while run_usb_thread:
        if usb_communication.check_if_device_is_connected() and measuring:
            new_data = usb_communication.read()
            if new_data is not None:
                data.extend(new_data)
                last_packet_time = get_current_time_ms()
                print(data[len(data) - 1])

            interface.draw_data(data)
        else:
            usb_communication.search_for_comport()


def update() -> None:
    """
    Update GUI
    """
    global device_was_connected
    global data
    global start_time
    global config
    global measuring

    if usb_communication.check_if_device_is_connected():
        device_was_connected = True
        interface.gen_start_button("Tilkoblet", "green")
    else:
        interface.gen_start_button("Ikke tilkoblet", "red")

        if device_was_connected:
            device_was_connected = False
            showwarning("Frakoblet", "Tremolometer ble frakoblet")

    if measuring and not len(data) == 0 and data[len(data) - 1][0] > config["maaletid"]:
        interface.finished_ui()
        measuring = False

        # Calculating and drawing spectrogram when the measuring is finished
        spectrogram.create_spectrogram_from_data(data, interface.frequency.plot, config)
        interface.frequency.canvas.draw()
        interface.update()

    interface.window.after(1, update)


usb_thread = threading.Thread(target=usb_thread)
usb_thread.start()


def on_exit() -> None:
    """
    Handle when the program exits.

    """
    global run_usb_thread

    run_usb_thread = False

    if usb_communication.connection is not None:
        usb_communication.connection.close()

    interface.window.destroy()


interface.window.protocol("WM_DELETE_WINDOW", on_exit)
spectrogram.create_spectrogram_from_data(data, interface.frequency.plot, config)
interface.frequency.canvas.draw()
interface.set_methods(start_button, update)
interface.update()
