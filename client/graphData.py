"""!
Contains data for one graph in the application.
"""
from tkinter import W, E, Tk
from typing import List
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from customTypes import Data


class GraphData:
    """!
    Container class for graph data. Used to display the raw data and the frequency.
    """
    def __init__(self, row: int, column: int, column_span: int,
                 fig_size_x: int, fig_size_y: int, window: Tk, x_axis_max: int,
                 x_axis_min=0, x_axis_step=1,
                  x_label='Tid (s)', y_label='Frekvens (Hz)') -> None:
        """!
        Constructor for a single graph in the GUI.

        @param self Pointer to self.
        @param row GUI row position in the tkinter grid.
        @param column GUI column position in the tkinter grid.
        @param column_span GUI column span in the tkinter grid.
        @param fig_size_x GUI size x in pixels.
        @param fig_size_y GUI size y in pixels.
        @param window Reference to tkinter window.
        @param x_axis_max Graph x-axis max value.
        @param x_axis_min Graph y-axis min value.
        @param x_axis_step Graph x-axis number of steps.
        @param x_label Graph x-axis label.
        @param y_label Graph y-axis label.
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

    def set_x_axis_max(self, new_x_axis_max) -> None:
        """!
        Set a new max x-axis value.

        @param self Pointer to self.
        @param new_x_axis_max The new x-axis value.
        """
        self.x_axis_max = new_x_axis_max
        self.draw([])

    def clear(self) -> None:
        """!
        Clear the plot.

        @params self Pinter to self.
        """
        self.plot.cla()
        self.plot.set_xlabel(self.x_label)
        self.plot.set_ylabel(self.y_label)

        self.plot.set_xlim([self.x_axis_min, self.x_axis_max])
        self.plot.set_xticks(list(range(0, self.x_axis_max + 1))[0::self.x_axis_step])

        self.plot.grid(color='gray', linestyle='dashed')

    def draw(self, data: List[Data] or List[tuple[int, int]]) -> None:
        """!
        Draws the data on the figure.

        @param self Pointer to self
        @param data The data that will be drawn on the figure.
        """
        self.clear()

        if data is None:
            self.canvas.draw()
            return

        if not len(data) == 0:

            # Calculating the maximum and minimum value
            max_value = max([max(element[1:]) for element in data]) * self.padding_value
            min_value = min([min(element[1:]) for element in data]) * self.padding_value

            # Setting the y-axis to be zoomed in on the range between min_value and max_value
            self.plot.set_ylim(min_value, max_value)

            # Looping through all the axes and plotting one line for each one.
            for i in range(0, len(data[0]) - 1):
                self.plot.plot([element[0] / 1000 for element in data], [element[i + 1] for element in data],
                               color=self.axis_color_and_direction[i][0], label=self.axis_color_and_direction[i][1])
            # Adding a legend to the plot
            self.plot.legend()

        # Drawing the canvas on the user interface.
        self.canvas.draw()
