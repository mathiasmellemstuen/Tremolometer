import pandas as pd

def update():
    global device_was_connected

    if check_if_device_is_connected():
        device_was_connected = True
        connected_ui()
        readFromSerialConnection()
    else:
        disconnected_ui()

        if device_was_connected:
            device_was_connected = False
            messagebox.showwarning("Frakoblet", "Tremolometer ble frakoblet")

    canvas.draw()
    window.after(1, update)

update()

window.mainloop()