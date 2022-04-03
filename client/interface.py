from tkinter import *
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from config import write_config

class Interface:
    def __init__(self, config):
        self.window = Tk()
        self.window.title("Tremolometer")
        self.window.configure(bg="white")
        self.menu = Menu(self.window)
        self.settings_menu = Menu(self.menu, tearoff=False)
        self.settings_menu.add_command(label="Innstillinger", command=self.menu_options)
        self.menu.add_cascade(label="Fil", menu=self.settings_menu)
        self.window.configure(menu=self.menu)
        self.start_button = None
        self.update_method = None
        self.frequency_graph_header = Label(text="Frekvens over tid", background="white", foreground="black", anchor="center")
        self.frequency_label = Label(text="Gjennomsnittlig frekvens: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
        self.measure_label = Label(text="Måling: 0 / 20 s", background="white", foreground="black", anchor="center")
        self.connection_label = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
        self.config = config

        # For graph plotting data over time
        self.data_figure, self.data_plot, self.data_canvas, self.data_widget = self.create_graph(2, "Tid (s)", "Bevegelse (mm)")

        # For graph plotting frequency over time
        self.frequency_figure, self.frequency_plot, self.frequency_canvas, self.frequency_widget = self.create_graph(4, "Tid (s)", "Frekvens (Hz)")

    def menu_options(self):
        settings_window = Toplevel(self.window)
        settings_window.title("Innstillinger")
        settings_window.geometry("200x200")

        Label(settings_window, text="Innstillinger").grid(row=0)
        Label(settings_window, text="Måletid (ms)").grid(row=1, column=0)

        entry = Entry(settings_window)
        entry.grid(row=1, column=1)
        entry.insert(0,self.config["maaletid"])
        def menu_save_button():
            entry_input = entry.get()
            if entry_input.isdigit():
                entry_input = int(entry_input)
                self.config["maaletid"] = entry_input
                write_config(self.config, "client/config.yaml")

            settings_window.destroy()

        Button(master=settings_window, text="Lagre", command=menu_save_button).grid(row=2)


    def set_methods(self, start_method, update_method):
        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black", command=start_method)
        self.update_method = update_method

    def disconnected_ui(self):
        self.connection_label.configure(text="Ikke tilkoblet")
        self.connection_label.configure(foreground="red")

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_graph_header.grid(column=6, row=3, sticky="news")
        self.frequency_label.grid(column=1, row=5, sticky="news", padx=20, pady=20)
        self.measure_label.grid(column=6, row=1, sticky="news")
        self.connection_label.grid(column=11, row=1, sticky="news")

    def connected_ui(self):
        self.connection_label.configure(text="Tilkoblet")
        self.connection_label.configure(foreground="green")

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_graph_header.grid(column=6, row=3, sticky="news")
        self.frequency_label.grid(column=1, row=5, sticky="news", padx=20, pady=20)
        self.measure_label.grid(column=6, row=1, sticky="news")
        self.connection_label.grid(column=11, row=1, sticky="news")

    def finished_ui(self):
        self.start_button.configure(text="Start ny måling")
        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)

    def draw_data(self, data):

        if data is None:
            self.data_canvas.draw()
            return

        if not len(data) == 0:
            padding_value = 1.10
            max_value = max([max(element[1:]) for element in data]) * padding_value
            min_value = min([min(element[1:]) for element in data]) * padding_value

            self.data_plot.set_ylim(min_value, max_value)

        self.data_plot.plot([element[0] for element in data], [element[1] for element in data], color=(1.0, 0.0, 0.0))
        self.data_plot.plot([element[0] for element in data], [element[2] for element in data], color=(0.0, 1.0, 0.0))
        self.data_plot.plot([element[0] for element in data], [element[3] for element in data], color=(0.0, 0.0, 1.0))

        self.data_canvas.draw()

    def update(self):
        self.update_method()
        self.window.mainloop()

    def create_graph(self, row, x_label, y_label):
        figure = Figure(figsize=(19, 5))
        plot = figure.add_subplot(111)
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        plot.grid(color='gray', linestyle='dashed')

        plot.set_xticks(list(range(0, self.config["maaletid"] + 1))[0::1000])
        plot.set_xlim([0, self.config["maaletid"]])
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.window)
        widget = canvas.get_tk_widget()
        widget.grid(column=1, row=row, columnspan=11, sticky=W + E)

        return figure, plot, canvas, widget