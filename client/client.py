"""!
Main entrypoint for this application. Handles initialization of the tkinter user interface and starting usb
communication thread.
"""
from tkinter.messagebox import showwarning, askquestion
from config import read_config
from customTypes import Config
from interface import Interface
from usbCommunication import USBCommunication
import threading
import filter
import spectrogram
import numpy as np

## Measurement data received from the microcontroller / sensor.
data = []

## Dict of data from the configuration file (config.yaml).
config: Config = read_config("client/config.yaml")

## Initialization of USB Communication connection to the microcontroller.
usb_communication: USBCommunication = USBCommunication()

## Initialization of the user interface.
interface = Interface(config)

## True if the microcontroller was connected during the last frame.
device_was_connected = False

## True if microcontroller are currently sending measurements to this application.
measuring = False

## True if the USB thread is currently running.
run_usb_thread = True


def start_button() -> None:
    """!
    Function is called then the start button is pressed. Sends start signal to the microcontroller if it's connected.
    """
    global measuring

    # Sends start signal if the device is connected. Displying a warning if the device is disconnected.
    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
        measuring = True
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")


def restart_button() -> None:
    """!
    Function is called when the restart button is pressed. Sends a start signal to the microcontroller if it's
    connected.
    """
    global data

    # Displaying dialogbox with yes / no question
    answer = askquestion("Starte på nytt", "Dette vil fjerne all synlig data og starte på nytt")

    # Clearing user interface and sends start signal
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
    Function is running on separate thread. Handling all USB communication such as reading measurment data, pinging
    microcontroller and searching for comports.
    """
    global data

    while run_usb_thread:
        # Reading the data if we are currently receiving measurement data and the device is connected.
        if usb_communication.check_if_device_is_connected() and measuring:

            # Reading data from microcontroller
            new_data = usb_communication.read()

            if new_data is not None:
                for d in new_data:
                    if d[1] == 0 and d[2] == 0 and d[3] == 0:
                        del d

                data.extend(new_data)

            # Updating the user interface with the received data
            interface.draw_data(data)
        elif usb_communication.check_if_device_is_connected():
            # Pinging the client to keep the connection alive
            usb_communication.ping()
        elif not usb_communication.check_if_device_is_connected():
            # Searching for a USB connection
            usb_communication.search_for_comport()


def update() -> None:
    """!
    Main update loop of the application. Providing user interface with data and updating the user interface accordingly.
    Handles processing of received data with filters and generating spectrogram images.
    """
    global device_was_connected
    global data
    global config
    global measuring

    if usb_communication.check_if_device_is_connected():
        device_was_connected = True
        # Changing the status text in the upper right corner if the device is connected
        interface.change_status_text("Tilkoblet", "green")
    else:
        # Changing the status text in the upper right corner if the device is disconnected
        interface.change_status_text("Ikke tilkoblet", "red")

        # This runs once after the device have been disconnected. Displays a warning dialog box
        if device_was_connected:
            device_was_connected = False
            showwarning("Frakoblet", "Tremolometer ble frakoblet")

    # Running once when application have reaceived every measurment from the microcontroller and the microcontroller is finished sending
    if measuring and not len(data) == 0 and data[len(data) - 1][0] / 1000 > config["maaletid"]:
        measuring = False

        # Getting the minimum value for each axis
        x_min = min(d[1] for d in data)
        y_min = min(d[2] for d in data)
        z_min = min(d[3] for d in data)

        # Pushing each axis in the graph above y = 0
        for i in range(len(data) - 1):
            temp_data = list(data[i])
            temp_data[1] = temp_data[1] - x_min
            temp_data[2] = temp_data[2] - y_min
            temp_data[3] = temp_data[3] - z_min
            data[i] = tuple(temp_data)

        # Applying low pass filter to data in each x,y,z axis
        data_x = filter.low_pass_filter(np.array([d[1] for d in data]), 19.9, 40)
        data_y = filter.low_pass_filter(np.array([d[2] for d in data]), 19.9, 40)
        data_z = filter.low_pass_filter(np.array([d[3] for d in data]), 19.9, 40)

        # Assigning low pass filter data to the data variable
        for i in range(len(data) - 1):
            temp_data = list(data[i])
            temp_data[1] = data_x[i]
            temp_data[2] = data_y[i]
            temp_data[3] = data_z[i]
            data[i] = tuple(temp_data)

        # Drawing processed data
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

        # Sending draw call to all graph in the user interface
        interface.draw_all()

        # Updating the user interface to finished mode. Displaying the strongest frequencies in the labels
        interface.finished_ui(strongest_frequency, strongest_frequency_x, strongest_frequency_y, strongest_frequency_z)

        # Updating interface. Includes running the tkinter update method
        interface.update()

    # Waiting 1 milliseconds before calling itself recursively
    interface.window.after(1, update)


def on_exit() -> None:
    """!
    Callback function that is called when the program exits. Closes usb connection and destroying tkinter window
    properly.
    """
    global run_usb_thread

    run_usb_thread = False

    if usb_communication.connection is not None:
        usb_communication.send_exit_signal()
        usb_communication.connection.close()

    interface.window.destroy()


if __name__ == '__main__':
    # Creating and startin usb thread
    data_handler = threading.Thread(target=usb_thread)
    data_handler.start()

    # Setting up on exit callback
    interface.window.protocol("WM_DELETE_WINDOW", on_exit)

    # Setting methods callbacks for buttons and update loop in the user interface
    interface.set_methods(start_button, update, restart_button)

    # Starting the update loop, calling itself recursively
    interface.update()
