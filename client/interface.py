from tkinter import *
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

        self.figure = None
        self.plot = None
        self.figure, self.plot = create_figure_and_plot(self.config)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=1, row=2, columnspan=11, sticky=W + E)

    def set_methods(self, start_method, save_as_method, update_method):
        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black", command=start_method)
        self.save_button = Button(text="Lagre som", padx=10, pady=10, background="white", foreground="black", command=save_as_method)
        self.update_method = update_method

    def disconnected_ui(self):
        self.connection_label.configure(text="Ikke tilkoblet")
        self.connection_label.configure(foreground="red")

        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)
        self.frequency_label.grid(column=1, row=3, sticky="news", padx=20, pady=20)
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
            self.canvas.draw()
            return

        self.plot.plot([element[0] for element in data], [element[1] for element in data], color=(1.0, 0.0, 0.0))
        self.plot.plot([element[0] for element in data], [element[2] for element in data], color=(0.0, 1.0, 0.0))
        self.plot.plot([element[0] for element in data], [element[3] for element in data], color=(0.0, 0.0, 1.0))
        self.canvas.draw()

    def update(self):
        self.update_method()
        self.window.mainloop()

def create_figure_and_plot(config):
    figure = Figure(figsize=(19, 5))
    plot = figure.add_subplot(111)
    plot.set_xlabel("Tid (s)")
    plot.set_ylabel("Bevegelse (mm)")
    plot.grid(color='gray', linestyle='dashed')


    plot.set_xticks(list(range(0, config["maaletid"] + 1))[0::1000])
    plot.set_xlim([0, config["maaletid"]])
    figure.tight_layout()
    return figure, plot