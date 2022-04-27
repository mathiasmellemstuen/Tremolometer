"""!
Handle GUI.
"""

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from config import write_config
from typing import Any, List, Tuple
from costumeTyping import Config, Data, Plot, Widget
import numpy as np


class GraphData:
    """!
    Container class for graph data. Used to display the raw data and the frequency.
    """

    def __init__(self, row: int, column: int, column_span: int,
                 fig_size_x: int, fig_size_y: int, x_axis_min: int, x_axis_max: int, x_axis_step: int,
                 window, x_label='Tid (s)', y_label='Frekvens (Hz)') -> None:
        """!
        Constructor.

        @params self Pointer to self.
        @params *data all data in as a tuple.
        """
        self.figure = Figure(figsize=(fig_size_x / 96, fig_size_y / 96), dpi=96)
        self.plot = self.figure.add_subplot(111, xlabel=x_label, ylabel=y_label)
        self.plot.grid(color='gray', linestyle='dashed')

        self.figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figure, master=window)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=column, row=row, columnspan=column_span, sticky=W + E)

        self.padding_value = 1.10
        self.axis_color_and_direction = (((1.0, 0.0, 0.0), "x"), ((0.0, 0.0, 1.0), "y"), ((0.0, 1.0, 0.0), "z"))
        self.x_label = x_label
        self.y_label = y_label
        self.x_axis_min = x_axis_min
        self.x_axis_max = x_axis_max
        self.x_axis_step = x_axis_step

    def clear(self):
        self.plot.cla()
        self.plot.set_xlabel(self.x_label)
        self.plot.set_ylabel(self.y_label)

        self.plot.set_xlim([self.x_axis_min, self.x_axis_max])
        self.plot.set_xticks(list(range(0, self.x_axis_max + 1))[0::self.x_axis_step])

        self.plot.grid(color='gray', linestyle='dashed')

    def draw(self, data: List[Data] or List[tuple[int, int]]) -> None:
        """!
        Draws the data to the figure.

        @param self Pointer to self
        @param data List containing data to plot
        """
        self.clear()

        if data is None:
            self.canvas.draw()
            return

        if not len(data) == 0:
            max_value = max([max(element[1:]) for element in data]) * self.padding_value
            min_value = min([min(element[1:]) for element in data]) * self.padding_value

            self.plot.set_ylim(min_value, max_value)

            for i in range(0, len(data[0]) - 1):
                self.plot.plot([element[0] / 1000 for element in data], [element[i + 1] for element in data],
                               color=self.axis_color_and_direction[i][0], label=self.axis_color_and_direction[i][1])

            self.plot.legend()  # Adding a legend to the plot

        self.canvas.draw()


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
        self.data = GraphData(2, 1, 11, 1920, 325, 0, graph_len, 1, self.window, "Bevegelse (mm)")

        # For graph plotting frequency over time
        self.frequency = GraphData(4, 1, 11, 1920, 325, 0, graph_len, 1, self.window)
        self.frequency_x = GraphData(6, 1, 4, 640, 250, 0, graph_len, 1, self.window)
        self.frequency_y = GraphData(6, 5, 4, 640, 250, 0, graph_len, 1, self.window)
        self.frequency_z = GraphData(6, 9, 4, 640, 250, 0, graph_len, 1, self.window)

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
        Label(settings_window, text="Måletid (ms)").grid(row=1, column=0)

        entry = Entry(settings_window)
        entry.grid(row=1, column=1)
        entry.insert(0, self.config["maaletid"])

        def menu_save_button() -> None:
            entry_input = entry.get()
            if entry_input.isdigit():
                entry_input = int(entry_input)
                self.config["maaletid"] = entry_input
                write_config(self.config, "client/config.yaml")

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

        # self.frequency_label.grid(column=12, row=2, sticky="n", padx=20, pady=20)

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
        self.frequency_label.grid(row=3, column=1, columnspan=11, sticky="news")
        self.frequency_label_x.grid(row=5, column=1, columnspan=4)
        self.frequency_label_y.grid(row=5, column=5, columnspan=4)
        self.frequency_label_z.grid(row=5, column=9, columnspan=4)

    def draw_data(self, data: List[Data]) -> None:
        """!
        Plot the data.

        @param self Pointer to self.
        @param data: What data to draw
        """
        self.data.draw(data)

    def update(self) -> None:
        """!
        Update the window

        @param self Pointer to self.
        """
        self.update_method()
        self.window.mainloop()
