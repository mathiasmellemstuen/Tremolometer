from interface import Interface
from config import read_config
from usbCommunication import USBCommunication
from tkinter.messagebox import showwarning
from timer import get_current_time_ms
import threading

data = []
config = read_config("client/config.yaml")
usb_communication = USBCommunication()
interface = Interface(config)
device_was_connected = False
measuring = False
start_time = None
run_usb_thread = True

def start_button():
    global start_time
    global measuring

    if usb_communication.check_if_device_is_connected():
        usb_communication.send_start_signal()
        start_time = get_current_time_ms()
        measuring = True
    else:
        showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")


def usb_thread():
    while run_usb_thread:
        if usb_communication.check_if_device_is_connected():

            if measuring:
                new_data = usb_communication.read()

                if new_data is not None:
                    data.extend(new_data)
                    print(len(data))

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

def on_exit():
    global run_usb_thread

    run_usb_thread = False

    if usb_communication.connection is not None:
        usb_communication.connection.close()

    interface.window.destroy()

interface.window.protocol("WM_DELETE_WINDOW", on_exit)
interface.draw_data(data)
interface.set_methods(start_button, update)
interface.update()