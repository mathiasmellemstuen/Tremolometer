"""!
Handle GUI.
"""
from tkinter import *
from typing import Any, List
from config import write_config
from customTypes import Config, Data
from graphData import GraphData


class Interface:
    """!
    Handle the user interface
    """
    def __init__(self, config: Config) -> None:
        """!
        Init all the window things.

        @param self Pointer to self.
        @param config Pointer to configuration.
        """
        self.window = Tk()
        self.window.title("Tremolometer")

        self.start_method = None
        self.update_method = None
        self.restart_method = None
        self.config = config
        self.menu = Menu(self.window)
        self.settings_menu = Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Innstillinger", command=self.menu_options)
        self.menu.add_cascade(label="Fil", menu=self.settings_menu)
        self.window.configure(bg="white", menu=self.menu)

        graph_len = int(config['maaletid'])
        # For graph plotting data over time
        self.data = GraphData(2, 1, 11, 1920, 325, self.window, graph_len, y_label="Bevegelse (mm)")

        # For graph plotting frequency over time
        self.frequency = GraphData(4, 1, 11, 1920, 325, self.window, graph_len)
        self.frequency_x = GraphData(6, 1, 4, 640, 250, self.window, graph_len)
        self.frequency_y = GraphData(6, 5, 4, 640, 250, self.window, graph_len)
        self.frequency_z = GraphData(6, 9, 4, 640, 250, self.window, graph_len)

        self.frequency_label = Label(text="Spektrogram for alle aksene", background="white", foreground="black", anchor="center")
        self.frequency_label.grid(row=3, column=1, columnspan=11, sticky="news")
        self.frequency_label_x = Label(text="Spektrogram for x-aksen", background="white", foreground="red", anchor="center")
        self.frequency_label_x.grid(row=5, column=1, columnspan=4)
        self.frequency_label_y = Label(text="Spektrogram for y-aksen", background="white", foreground="blue", anchor="center")
        self.frequency_label_y.grid(row=5, column=5, columnspan=4)
        self.frequency_label_z = Label(text="Spektrogram for z-aksen", background="white", foreground="green", anchor="center")
        self.frequency_label_z.grid(row=5, column=9, columnspan=4)

        Label(text="Data", background="white", foreground="black", anchor="center") \
            .grid(row=1, column=1, columnspan=11, sticky="news")

        self.connection_label = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
        self.connection_label.grid(row=1, column=11, sticky="news")

        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black")
        self.start_button.grid(row=1, column=1, sticky="news", padx=20, pady=20)

        self.data.draw([])
        self.frequency.draw([])
        self.frequency_x.draw([])
        self.frequency_y.draw([])
        self.frequency_z.draw([])

    def menu_options(self) -> None:
        """!
        Titlebar menu option.

        @param self Pointer to self.
        """
        settings_window = Toplevel(self.window)
        settings_window.title("Innstillinger")
        settings_window.geometry("200x200")

        Label(settings_window, text="Innstillinger").grid(row=0)
        Label(settings_window, text="Måletid (s)").grid(row=1, column=0)

        entry = Entry(settings_window)
        entry.grid(row=1, column=1)
        entry.insert(0, self.config["maaletid"])

        def menu_save_button() -> None:
            entry_input = entry.get()
            if entry_input.isdigit():
                entry_input = int(entry_input)
                self.config["maaletid"] = entry_input
                write_config(self.config, "client/config.yaml")

                self.data.set_x_axis_max(self.config["maaletid"])
                self.frequency.set_x_axis_max(self.config["maaletid"])
                self.frequency_x.set_x_axis_max(self.config["maaletid"])
                self.frequency_y.set_x_axis_max(self.config["maaletid"])
                self.frequency_z.set_x_axis_max(self.config["maaletid"])

            settings_window.destroy()

        Button(master=settings_window, text="Lagre", command=menu_save_button).grid(row=2)

    def set_methods(self, start_method: Any, update_method: Any, restart_method: Any) -> None:
        """!
        Attach a start method to the start button and a method to the update variable.

        @param self Pointer to self.
        @param start_method Pointer to the start method.
        @param update_method Pointer to the method called each update.
        @param restart_method Pointer to the method called to restart taking measurement.
        """
        self.start_method = start_method
        self.update_method = update_method
        self.restart_method = restart_method

        self.start_button.configure(command=self.start_method)

    def change_status_text(self, text: str, foreground: str) -> None:
        """!
        Generate the start button.

        @param self Pointer to self.
        @param text The start button text.
        @param foreground What color the text.
        """
        self.connection_label.configure(text=text, foreground=foreground)

    def finished_ui(self, frequency_all, frequency_x, frequency_y, frequency_z) -> None:
        """!
        Change the text to start a new measurement.

        @param self Pointer to self.
        """
        self.start_button.configure(text="Start ny måling")
        self.start_button.configure(command=self.restart_method)
        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)

        self.frequency_label.configure(text=f'Spektrogram for alle aksene ({frequency_all:.2f}Hz)')
        self.frequency_label_x.configure(text=f'Spektrogram for x-aksen ({frequency_x:.2f}Hz)')
        self.frequency_label_y.configure(text=f'Spektrogram for y-aksen ({frequency_y:.2f}Hz)')
        self.frequency_label_z.configure(text=f'Spektrogram for z-aksen ({frequency_z:.2f}Hz)')
        self.draw_labels()

    def draw_data(self, data: List[Data]) -> None:
        """!
        Plot the data.

        @param self Pointer to self.
        @param data: What data to draw
        """
        self.data.draw(data)

    def draw_all(self) -> None:
        self.frequency.canvas.draw()
        self.frequency_x.canvas.draw()
        self.frequency_y.canvas.draw()
        self.frequency_z.canvas.draw()

    def clear_all(self) -> None:
        self.frequency.clear()
        self.frequency_x.clear()
        self.frequency_y.clear()
        self.frequency_z.clear()

    def draw_labels(self):
        self.frequency_label.grid(row=3, column=1, columnspan=11, sticky="news")
        self.frequency_label_x.grid(row=5, column=1, columnspan=4)
        self.frequency_label_y.grid(row=5, column=5, columnspan=4)
        self.frequency_label_z.grid(row=5, column=9, columnspan=4)

    def update(self) -> None:
        """!
        Update the window

        @param self Pointer to self.
        """
        self.update_method()
        self.window.mainloop()
