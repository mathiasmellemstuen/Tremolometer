import pandas as pd
from interface import Interface, create_figure
from config import read_config
from usbCommunication import USBCommunication
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfile

#data = [(1, 1, 2, 3), (2, 4, 5, 6), (3, 7, 8, 9), (4, 10, 11, 12), (5, 13, 14, 15)]
data = []
config = read_config("client/config.yaml")
usb_communication = USBCommunication()
interface = Interface(config)
device_was_connected = False

def start_button():
    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")

def save_as_button():
    f = asksaveasfile(title="Lagre som", defaultextension=".csv", filetypes=[("CSV fil", "*.csv"), ("Excel fil", "*.xlsx")])

    if f is None:
        return

    dataFrame = pd.DataFrame(data, columns=['Tid(s)', 'Bevegelse (mm)'])

    extension = f.name.split(".")[-1]

    if extension == "csv":
        dataFrame.to_csv(f.name)
    else:
        dataFrame.to_excel(f.name, index=False)

    f.close()

def update():
    global device_was_connected

    if usb_communication.check_if_device_is_connected():
        device_was_connected = True
        interface.connected_ui()
        time, x, y, z = usb_communication.read()

        if time is not None:
            data.append((time, x, y, z))
            interface.draw_plot(create_figure(data, config))

    else:
        interface.disconnected_ui()

        if device_was_connected:
            device_was_connected = False
            showwarning("Frakoblet", "Tremolometer ble frakoblet")

    interface.window.after(1, update)

interface.draw_plot(create_figure(data, config))
interface.set_methods(start_button, save_as_button, update)
interface.update()