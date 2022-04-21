"""!
Handle GUI.
"""

from tkinter import *
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from config import write_config
from spectrogram import create_spectrogram_from_data
from typing import Any, List
from costumeTyping import Config, Data


class Graph_data:
    """!
    Container class for graph data. Used to display the raw data and the frequency.
    """
    def __init__(self, time_full_time : bool, x_label : str, y_label : str, config: Config, *data: tuple[Figure, Any, FigureCanvasTkAgg, Any] or Any) -> None:
        """!
        Constructor.

        @params self Pointer to self.
        @params *data all data in as a tuple.
        """
        self.padding_value = 1.10
        self.color = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        self.figure, self.plot, self.canvas, self.widget = data
        self.config = config
        self.x_label = x_label
        self.y_label = y_label
        self.time_full_time = time_full_time

    def clear(self):

        self.plot.cla()
        self.plot.set_xlabel(self.x_label)
        self.plot.set_ylabel(self.y_label)

        if self.time_full_time:
            self.plot.set_xticks(list(range(0, self.config["maaletid"] + 1))[0::1000])
            self.plot.set_xlim([0, self.config["maaletid"]])

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
            padding_value = 1.10
            max_value = max([max(element[1:]) for element in data]) * self.padding_value
            min_value = min([min(element[1:]) for element in data]) * self.padding_value

            self.plot.set_ylim(min_value, max_value)

            for i in range(0, len(data[0]) - 1):
                self.plot.plot([element[0] for element in data], [element[i + 1] for element in data],
                               color=self.color[i])

        self.canvas.draw()


class Interface:
    """!
    Interface class.

    More details.
    """

    def __init__(self, config: Config) -> None:
        """!
        Init all the window things.

        @param self Pointer to self.
        @param config Pointer to configuration.
        """
        self.window = Tk()
        self.window.title("Tremolometer")
        self.menu = Menu(self.window)
        self.settings_menu = Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Innstillinger", command=self.menu_options)
        self.menu.add_cascade(label="Fil", menu=self.settings_menu)
        self.window.configure(bg="white", menu=self.menu)
        self.start_button = None
        self.update_method = None
        self.restart_method = None
        self.frequency_graph_header = Label(text="Spektrogram", background="white", foreground="black", anchor="center")
        self.frequency_label = Label(text="Gjennomsnittlig frekvens: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
        self.measure_label = Label(text="Måling: 0 / 20 s", background="white", foreground="black", anchor="center")
        self.connection_label = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
        self.config = config

        # For graph plotting data over time
        self.data = self.create_graph(2, "Tid (s)", "Bevegelse (mm)", True)


        # For graph plotting frequency over time
        self.frequency = self.create_graph(4, "Tid (s)", "Frekvens (Hz)", False)

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
        Attach a method to a button.

        Attach a start method to the start button and a method to the update variable.

        @param self Pointer to self.
        @param start_method Pointer to the start method.
        @param update_method Pointer to the method called each update.
        """
        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black",
                                   command=start_method)
        self.update_method = update_method
        self.restart_method = restart_method

    def gen_start_button(self, text: str, foreground: str) -> None:
        """!
        Generate the start button.

        @param self Pointer to self.
        @param text The start button text.
        @param foreground What color the text.
        """
        self.connection_label.configure(text=text, foreground=foreground)

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_graph_header.grid(column=1, row=3, columnspan=11, sticky="news")
        self.frequency_label.grid(column=1, row=5, sticky="news", padx=20, pady=20)
        self.measure_label.grid(column=6, row=1, sticky="news")
        self.connection_label.grid(column=11, row=1, sticky="news")

    def finished_ui(self) -> None:
        """!
        Change the text to start a new measurement.

        @param self Pointer to self.
        """
        self.start_button.configure(text="Start ny måling")
        self.start_button.configure(command=self.restart_method)
        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)

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

    def create_graph(self, row: int, x_label: str, y_label: str, time_full_time : bool) -> Graph_data:
        """!
        Create a graph window.

        @param self Pointer to self.
        @param row The number of rows
        @param x_label Label for x-axis
        @param y_label Label for y-axis

        @return figure, plot, canvas, widget
        """
        figure = Figure(figsize=(19, 5))
        plot = figure.add_subplot(111)
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        plot.grid(color='gray', linestyle='dashed')

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.window)
        widget = canvas.get_tk_widget()
        widget.grid(column=1, row=row, columnspan=11, sticky=W + E)

        return Graph_data(time_full_time, x_label, y_label, self.config, figure, plot, canvas, widget)
