"""!
Handle the client.
"""
from typing import List
from costumeTyping import Data, Config
from interface import Interface
from config import read_config
from usbCommunication import USBCommunication
from tkinter.messagebox import showwarning, askquestion
from timer import get_current_time_ms
from statistics import mean
import threading
import numpy as np
import spectrogram
import filter

data = []
"""!Store data"""
config: Config = read_config("client/config.yaml")
usb_communication: USBCommunication = USBCommunication()
# Creating test data
# for i in range(0, 20000):
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


def restart_button() -> None:
    global data
    answer = askquestion("Starte på nytt", "Dette vil fjerne all synlig data og starte på nytt")

    if answer == "yes":
        data = []

        interface.frequency.clear()
        interface.frequency_x.clear()
        interface.frequency_y.clear()
        interface.frequency_z.clear()

        interface.frequency.canvas.draw()
        interface.frequency_x.canvas.draw()
        interface.frequency_y.canvas.draw()
        interface.frequency_z.canvas.draw()

        start_button()


def usb_thread() -> None:
    """
    Draws data sent form the accelerometer to the plot on the GUI.

    """
    global last_packet_time
    global data

    while run_usb_thread:
        if usb_communication.check_if_device_is_connected() and measuring:
            new_data = usb_communication.read()

            if new_data is not None:
                for d in new_data:
                    if d[1] == 0 and d[2] == 0 and d[3] == 0:
                        del d

                data.extend(new_data)
                last_packet_time = get_current_time_ms()

            interface.draw_data(data)
        elif not usb_communication.check_if_device_is_connected():
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
        interface.change_status_text("Tilkoblet", "green")
    else:
        interface.change_status_text("Ikke tilkoblet", "red")

        if device_was_connected:
            device_was_connected = False
            showwarning("Frakoblet", "Tremolometer ble frakoblet")

    # Run after the measuring is done
    if measuring and not len(data) == 0 and data[len(data) - 1][0] / 1000 > config["maaletid"]:
        interface.finished_ui()
        measuring = False

        # Normalize all axis
        x_mean = min(d[1] for d in data)
        y_mean = min(d[2] for d in data)
        z_mean = min(d[3] for d in data)

        for i in range(len(data) - 1):
            temp_data = list(data[i])
            temp_data[1] = temp_data[1] - x_mean
            temp_data[2] = temp_data[2] - y_mean
            temp_data[3] = temp_data[3] - z_mean
            data[i] = tuple(temp_data)

        data_x = filter.low_pass_filter(np.array([d[1] for d in data]), 19.9, 40)
        data_y = filter.low_pass_filter(np.array([d[2] for d in data]), 19.9, 40)
        data_z = filter.low_pass_filter(np.array([d[3] for d in data]), 19.9, 40)

        for i in range(len(data) - 1):
            temp_data = list(data[i])
            temp_data[1] = data_x[i]
            temp_data[2] = data_y[i]
            temp_data[3] = data_z[i]
            data[i] = tuple(temp_data)

        interface.draw_data(data)

        # Calculating and drawing spectrogram when the measuring is finished
        three_axial_length_data = [np.sqrt(pow(d[1], 2) + pow(d[2], 2) + pow(d[3], 2)) for d in data]
        three_axial_length_data_mean = min(d for d in three_axial_length_data)
        for i in range(len(three_axial_length_data) - 1):
            three_axial_length_data[i] = three_axial_length_data[i] - three_axial_length_data_mean

        strongest_frequency = spectrogram.create_spectrogram_from_data(three_axial_length_data, interface.frequency.plot, config, "hot")
        strongest_frequency_x = spectrogram.create_spectrogram_from_data([d[1] for d in data], interface.frequency_x.plot, config, "hot")
        strongest_frequency_y = spectrogram.create_spectrogram_from_data([d[2] for d in data], interface.frequency_y.plot, config, "hot")
        strongest_frequency_z = spectrogram.create_spectrogram_from_data([d[3] for d in data], interface.frequency_z.plot, config, "hot")

        interface.frequency.canvas.draw()
        interface.frequency_x.canvas.draw()
        interface.frequency_y.canvas.draw()
        interface.frequency_z.canvas.draw()

        interface.finished_ui(frequency_all=strongest_frequency, frequency_x=strongest_frequency_x, frequency_y=strongest_frequency_y, frequency_z=strongest_frequency_z)
        interface.update()

    interface.window.after(1, update)


def on_exit() -> None:
    """
    Handle when the program exits.

    """
    global run_usb_thread

    run_usb_thread = False

    if usb_communication.connection is not None:
        usb_communication.send_exit_signal()
        usb_communication.connection.close()

    interface.window.destroy()


if __name__ == '__main__':
    usb_thread = threading.Thread(target=usb_thread)
    usb_thread.start()

    interface.window.protocol("WM_DELETE_WINDOW", on_exit)
    interface.set_methods(start_button, update, restart_button)
    interface.update()
