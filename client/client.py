"""!
Handle the client.
"""
from tkinter.messagebox import showwarning, askquestion
from interface import Interface
from timer import get_current_time_ms
from usbCommunication import USBCommunication
from config import Config

import threading
import filter
import spectrogram
import numpy as np

## Measurement data.
data = []

## Config data.
config = Config("client/config.yaml")

## Communication connection to the microcontroller.
usb_communication: USBCommunication = USBCommunication(config)

## GUI.
interface = Interface(config)

## Microcontroller has been connected.
device_was_connected = False

## Microcontroller and Client are communicating measurements.
measuring = False

## The USB thread is currently running.
run_usb_thread = True

## Last packet time
last_packet_time = 0


def start_button() -> None:
    """!
    Start communication with microcontroller if it is connected.
    """
    global measuring

    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
        measuring = True
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")


def restart_button() -> None:
    """!
    Start measuring a new sett of data from the microcontroller.
    """
    global data, measuring
    answer = askquestion("Starte på nytt", "Dette vil fjerne all synlig data og starte på nytt")

    if answer == "yes":
        data = []

        interface.clear_all()
        interface.draw_all()

        interface.frequency_label.configure(text=f'Spektrogram for alle aksene')
        interface.frequency_label_x.configure(text=f'Spektrogram for x-aksen')
        interface.frequency_label_y.configure(text=f'Spektrogram for y-aksen')
        interface.frequency_label_z.configure(text=f'Spektrogram for z-aksen')
        interface.draw_labels()

        start_button()


def usb_thread() -> None:
    """!
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
        elif usb_communication.check_if_device_is_connected():
            status, in_data = usb_communication.ping()

            if not status and len(in_data) > 10:
                new_data = usb_communication.read_from_data(in_data)

                for d in new_data:
                    if d[1] == 0 and d[2] == 0 and d[3] == 0:
                        del d

                data.extend(new_data)
                last_packet_time = get_current_time_ms()

        elif not usb_communication.check_if_device_is_connected():
            usb_communication.search_for_comport()


def update() -> None:
    """!
    Update GUI.
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
        measuring = False

        # Normalize all axis
        x_min = min(d[1] for d in data)
        y_min = min(d[2] for d in data)
        z_min = min(d[3] for d in data)

        for i in range(len(data) - 1):
            temp_data = list(data[i])
            temp_data[1] = temp_data[1] - x_min
            temp_data[2] = temp_data[2] - y_min
            temp_data[3] = temp_data[3] - z_min
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

        strongest_frequency = spectrogram.create_spectrogram_from_data(three_axial_length_data,
                                                                       interface.frequency.plot, config)
        strongest_frequency_x = spectrogram.create_spectrogram_from_data([d[1] for d in data],
                                                                         interface.frequency_x.plot, config)
        strongest_frequency_y = spectrogram.create_spectrogram_from_data([d[2] for d in data],
                                                                         interface.frequency_y.plot, config)
        strongest_frequency_z = spectrogram.create_spectrogram_from_data([d[3] for d in data],
                                                                         interface.frequency_z.plot, config)

        interface.draw_all()

        interface.finished_ui(strongest_frequency, strongest_frequency_x, strongest_frequency_y, strongest_frequency_z)
        interface.update()

    interface.window.after(1, update)


def on_exit() -> None:
    """!
    Handle when the program exits.
    """
    global run_usb_thread

    run_usb_thread = False

    if usb_communication.connection is not None:
        usb_communication.send_exit_signal()
        usb_communication.connection.close()

    interface.window.destroy()


if __name__ == '__main__':
    data_handler = threading.Thread(target=usb_thread)
    data_handler.start()

    interface.window.protocol("WM_DELETE_WINDOW", on_exit)
    interface.set_methods(start_button, update, restart_button)
    interface.update()
