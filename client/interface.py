"""!
Handles the user interface. Using tkinter to create a user interface. Contains functionality related to the user
interface.
"""
from tkinter import *
from typing import Any, List
from config import write_config
from customTypes import Config, Data
from graphData import GraphData


class Interface:
    """!
    Class for handling the user interface. Containing all visual objects in the user interface.
    """

    def __init__(self, config: Config) -> None:
        """!
        Initializing the user interface. Creating a window with all GUI elements.

        @param self Pointer to self.
        @param config Configuration from the configuration file (config.yaml).
        """

        ## Tkinter window context
        self.window = Tk()

        # Setting the title of the window
        self.window.title("Tremolometer")

        ## Pointing to a method
        self.start_method = None

        ## Pointing to a method
        self.update_method = None

        ## Pointing to a method
        self.restart_method = None

        ## Configuration from the configuration file (config.yaml)
        self.config = config

        ## Tkinter menu context
        self.menu = Menu(self.window)

        # Creating the settings menu from with the already existing window context
        self.settings_menu = Menu(self.menu, tearoff=False)

        # Adding innstillinger to dropdown menu
        self.settings_menu.add_command(label="Innstillinger", command=self.menu_options)

        # Adding the innstillinger to fil cascade
        self.menu.add_cascade(label="Fil", menu=self.settings_menu)

        # Setting the window background white
        self.window.configure(bg="white", menu=self.menu)

        graph_len = int(config['maaletid'])

        ## GraphData for plotting data over time
        self.data = GraphData(2, 1, 11, 1920, 325, self.window, graph_len, y_label="Bevegelse (mm)")

        ## Graph for plotting the frequency over time
        self.frequency = GraphData(4, 1, 11, 1920, 325, self.window, graph_len)

        ## Graph for plotting the frequency over time for only x-axis data
        self.frequency_x = GraphData(6, 1, 4, 640, 250, self.window, graph_len)

        ## Graph for plotting the frequency over time for only y-axis data
        self.frequency_y = GraphData(6, 5, 4, 640, 250, self.window, graph_len)

        ## Graph for plotting the frequency over time for only z-axis data
        self.frequency_z = GraphData(6, 9, 4, 640, 250, self.window, graph_len)

        ## Label as header for frequency graph
        self.frequency_label = Label(text="Spektrogram for alle aksene", background="white", foreground="black",
                                     anchor="center")
        self.frequency_label.grid(row=3, column=1, columnspan=11, sticky="news")

        ## Label as header for x-axis frequency graph
        self.frequency_label_x = Label(text="Spektrogram for x-aksen", background="white", foreground="red",
                                       anchor="center")
        self.frequency_label_x.grid(row=5, column=1, columnspan=4)

        ## Label as header for y-axis frequency graph
        self.frequency_label_y = Label(text="Spektrogram for y-aksen", background="white", foreground="blue",
                                       anchor="center")
        self.frequency_label_y.grid(row=5, column=5, columnspan=4)

        ## Label as header for z-axis frequency graph
        self.frequency_label_z = Label(text="Spektrogram for z-aksen", background="white", foreground="green",
                                       anchor="center")
        self.frequency_label_z.grid(row=5, column=9, columnspan=4)

        # Label explaining data graph
        Label(text="Data", background="white", foreground="black", anchor="center") \
            .grid(row=1, column=1, columnspan=11, sticky="news")

        ## Label for displaying connected/disconnected status
        self.connection_label = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
        self.connection_label.grid(row=1, column=11, sticky="news")

        ## Start / restart button in the upper right corner of the user interface
        self.start_button = Button(text="Start", padx=10, pady=10, background="white", foreground="black")
        self.start_button.grid(row=1, column=1, sticky="news", padx=20, pady=20)

        # Drawing all graphs with empty data to update axis labels and numbers
        self.data.draw([])
        self.frequency.draw([])
        self.frequency_x.draw([])
        self.frequency_y.draw([])
        self.frequency_z.draw([])

    def menu_options(self) -> None:
        """!
        Function opens new window (options menu window)

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

        # Running when the save button in the options menu is clicked
        def menu_save_button() -> None:
            entry_input = entry.get()
            if entry_input.isdigit():
                entry_input = int(entry_input)

                # Updates the new input in both the settings file and elsewhere in the application
                self.config["maaletid"] = entry_input
                write_config(self.config, "client/config.yaml")

                self.data.set_x_axis_max(self.config["maaletid"])
                self.frequency.set_x_axis_max(self.config["maaletid"])
                self.frequency_x.set_x_axis_max(self.config["maaletid"])
                self.frequency_y.set_x_axis_max(self.config["maaletid"])
                self.frequency_z.set_x_axis_max(self.config["maaletid"])

            # Closes the settings window
            settings_window.destroy()

        Button(master=settings_window, text="Lagre", command=menu_save_button).grid(row=2)

    def set_methods(self, start_method: Any, update_method: Any, restart_method: Any) -> None:
        """!
        Attaching a start method to the start button and update loop method to the update loop.

        @param self Pointer to self.
        @param start_method Method called when start button is pressed.
        @param update_method Method called each update iteration.
        @param restart_method Method called when restart button is pressed.
        """

        self.start_method = start_method
        self.update_method = update_method
        self.restart_method = restart_method

        # Binding the start method to the start button
        self.start_button.configure(command=self.start_method)

    def change_status_text(self, text: str, foreground: str) -> None:
        """!
        Changing the status label text and foreground color. Status label located in the upper right corner.
        Generate the start button.

        @param self Pointer to self.
        @param text Label text.
        @param foreground Foreground-color of the label.
        """
        self.connection_label.configure(text=text, foreground=foreground)

    def finished_ui(self, frequency_all, frequency_x, frequency_y, frequency_z) -> None:
        """!
        Changing the state of the user interface to finished state. This is displaying restart button and changing labels to contain measured frequencies.

        @param self Pointer to self.
        @param frequency_all The most significant frequency in the spectrogram for all axis.
        @param frequency_x The most significant frequency in the spectrogram for the x-axis.
        @param frequency_y The most significant frequency in the spectrogram for the y-axis.
        @param frequency_z The most significant frequency in the spectrogram for the z-axis.
        """

        # Changing text and functionality of start button to restart text and functionality
        self.start_button.configure(text="Start ny måling")
        self.start_button.configure(command=self.restart_method)
        self.start_button.grid(column=1, row=1, sticky="news", padx=20, pady=20)

        # Updating frequency labels
        self.frequency_label.configure(text=f'Spektrogram for alle aksene ({frequency_all:.2f}Hz)')
        self.frequency_label_x.configure(text=f'Spektrogram for x-aksen ({frequency_x:.2f}Hz)')
        self.frequency_label_y.configure(text=f'Spektrogram for y-aksen ({frequency_y:.2f}Hz)')
        self.frequency_label_z.configure(text=f'Spektrogram for z-aksen ({frequency_z:.2f}Hz)')
        self.draw_labels()

    def draw_data(self, data: List[Data]) -> None:
        """!
        Drawing the data to the data plot

        @param self Pointer to self.
        @param data List of data to draw
        """
        self.data.draw(data)

    def draw_all(self) -> None:
        """!
        Drawing canvas for every canvas containing a spectrogram.

        @param self Pointer to self.
        """
        self.frequency.canvas.draw()
        self.frequency_x.canvas.draw()
        self.frequency_y.canvas.draw()
        self.frequency_z.canvas.draw()

    def clear_all(self) -> None:
        """!
        Clear all canvases containing a spectrogram.

        @param self Pointer to self.
        """
        self.frequency.clear()
        self.frequency_x.clear()
        self.frequency_y.clear()
        self.frequency_z.clear()

    def draw_labels(self):
        """!
        Drawing all labels in the user interface

        @param self Pointer to self.
        """
        self.frequency_label.grid(row=3, column=1, columnspan=11, sticky="news")
        self.frequency_label_x.grid(row=5, column=1, columnspan=4)
        self.frequency_label_y.grid(row=5, column=5, columnspan=4)
        self.frequency_label_z.grid(row=5, column=9, columnspan=4)

    def update(self) -> None:
        """!
        Updating the window and running the tkinter mainloop.

        @param self Pointer to self.
        """
        self.update_method()
        self.window.mainloop()
