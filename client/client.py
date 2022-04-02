from interface import Interface
from config import read_config
from usbCommunication import USBCommunication
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfile
import pandas as pd
from timer import get_current_time_ms
import threading

data = []
config = read_config("client/config.yaml")
usb_communication = USBCommunication()
interface = Interface(config)
device_was_connected = False
measuring = False
start_time = None


def start_button():
    global start_time
    global measuring

    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
        start_time = get_current_time_ms()
        measuring = True
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")


def save_as_button():
    f = asksaveasfile(title="Lagre som", defaultextension=".csv",
                      filetypes=[("CSV fil", "*.csv"), ("Excel fil", "*.xlsx")])

    if f is None:
        return

    dataFrame = pd.DataFrame(data, columns=['Tid(s)', 'Bevegelse (mm)'])

    extension = f.name.split(".")[-1]

    if extension == "csv":
        dataFrame.to_csv(f.name)
    else:
        dataFrame.to_excel(f.name, index=False)

    f.close()


def usb_thread():
    while True:
        if usb_communication.check_if_device_is_connected():

            if measuring:
                new_data = usb_communication.read()

                if new_data is not None:
                    data.extend(new_data)

                interface.draw_data(data)
        else:
            usb_communication.search_for_comport()


def update():
    global device_was_connected
    global data
    global start_time
    global config
    global measuring

    if usb_communication.check_if_device_is_connected():
        device_was_connected = True
        interface.connected_ui()

    else:

        interface.disconnected_ui()

        if device_was_connected:
            device_was_connected = False
            showwarning("Frakoblet", "Tremolometer ble frakoblet")

    if not start_time is None and get_current_time_ms() - start_time + 1000 > config['maaletid']:
        interface.finished_ui()
        measuring = False

    interface.window.after(1, update)


usb_thread = threading.Thread(target=usb_thread)
usb_thread.start()

interface.draw_data(data)
interface.set_methods(start_button, save_as_button, update)
interface.update()
