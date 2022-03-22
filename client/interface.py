from tkinter import *
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class Interface:
    def __init__(self, config):
        self.window = Tk()
        self.window.title("Tremolometer")
        self.window.configure(bg="white")
        self.start_button = None
        self.save_button = None
        self.update_method = None
        self.frequency_label = Label(text="Frequency: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
        self.measure_label = Label(text="Måling: 0 / 20 s", background="white", foreground="black", anchor="center")
        self.connection_label = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
        self.config = config

        # For graph plotting data over time
        self.data_figure, self.data_plot, self.data_canvas, self.data_widget = self.create_graph(2, "Tid (s)", "Bevegelse (mm)")

        # For graph plotting frequency over time
        self.frequency_figure, self.frequency_plot, self.frequency_canvas, self.frequency_widget = self.create_graph(3, "Tid (s)", "Frekvens (Hz)")

    def graph_mouse_move(self, event):
        if event.inaxes:
            event.inaxes.plot(event.xdata, 0, event.xdata, 10000)
            event.inaxes.plot(0, event.inaxes.get_y_lim(), event.xdata, event.inaxes.get_y_lim())

    def set_methods(self, start_method, save_as_method, update_method):
        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black", command=start_method)
        self.save_button = Button(text="Lagre som", padx=10, pady=10, background="white", foreground="black", command=save_as_method)
        self.update_method = update_method

    def disconnected_ui(self):
        self.connection_label.configure(text="Ikke tilkoblet")
        self.connection_label.configure(foreground="red")

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_label.grid(column=1, row=4, sticky="news", padx=20, pady=20)
        self.measure_label.grid(column=6, row=1, sticky="news")
        self.connection_label.grid(column=11, row=1, sticky="news")

    def connected_ui(self):
        self.connection_label.configure(text="Tilkoblet")
        self.connection_label.configure(foreground="green")

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_label.grid(column=1, row=3, sticky="news", padx=20, pady=20)
        self.measure_label.grid(column=6, row=1, sticky="news")
        self.connection_label.grid(column=11, row=1, sticky="news")

    def finished_ui(self):
        self.save_button.grid(column=11, row=3, sticky="news", padx=20, pady=20)

    def draw_data(self, data):

        if data is None:
            self.data_canvas.draw()
            return

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
        canvas.mpl_connect('motion_notify_event', self.graph_mouse_move)
        widget = canvas.get_tk_widget()
        widget.grid(column=1, row=row, columnspan=11, sticky=W + E)

        return figure, plot, canvas, widget