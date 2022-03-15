from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import config
config = config.read_config()

# Window
window = Tk()
window.title("Tremolometer")
window.configure(bg="white")

# Creating GUI objects
frequencyLabel = Label(text="Frequency: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
measureLabel = Label(text="Måling: 0 / 20 s", background="white", foreground="black", anchor="center")
connectionLabel = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
startButton = Button(text="Start", padx=10, pady=10, background="white", foreground="black", command=start)
saveButton = Button(text="Lagre som", padx=10, pady=10, background="white", foreground="black", command=save_as)

#data = [(1, 1, 2, 3), (2, 4, 5, 6), (3, 7, 8, 9), (4, 10, 11, 12), (5, 13, 14, 15)]
def createFigure(data):
    figure = Figure(figsize=(19, 5))
    plot = figure.add_subplot(111)
    plot.set_xlabel("Tid (s)")
    plot.set_ylabel("Bevegelse (mm)")
    plot.grid(color='gray', linestyle='dashed')
    plot.plot([element[0] for element in data], [element[1] for element in data], color=(1.0, 0.0, 0.0))
    plot.plot([element[0] for element in data], [element[2] for element in data], color=(0.0, 1.0, 0.0))
    plot.plot([element[0] for element in data], [element[3] for element in data], color=(0.0, 0.0, 1.0))
    plot.set_xticks(range(0, config["maaletid"] + 1))
    plot.set_xlim([0, config["maaletid"]])
    figure.tight_layout()
    return figure

def drawPlot(figure, window, row = 2):
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(column=1, row=row, columnspan=11, sticky=W + E)

def disconnected_ui():
    connectionLabel.configure(text="Ikke tilkoblet")
    connectionLabel.configure(foreground="red")

    startButton.grid(column=1, row=1, sticky="news", padx=20, pady=20)
    frequencyLabel.grid(column=1, row=3, sticky="news", padx=20, pady=20)
    measureLabel.grid(column=6, row=1, sticky="news")
    connectionLabel.grid(column=11, row=1, sticky="news")


def connected_ui():
    connectionLabel.configure(text="Tilkoblet")
    connectionLabel.configure(foreground="green")

def finished_ui():
    saveButton.grid(column=11, row=3, sticky="news", padx=20, pady=20)

def start():
    global comport
    global serialConnection

    if check_if_device_is_connected():
        comport = search_for_comport().name

        print("Starting on com-port: ", comport)
        serialConnection = serial.Serial(port="/dev/" + comport, parity=serial.PARITY_NONE)

        print("Sending starting signal to Tremolometer")
        sendStartSignal()

        measuring_ui()
    else:
        messagebox.showwarning(title="Ikke tilkoblet", message="Koble til tremolometer via USB og prøv igjen.")

def save_as():
    f = filedialog.asksaveasfile(title="Lagre som", defaultextension=".csv", filetypes=[("CSV fil", "*.csv"), ("Excel fil", "*.xlsx")])


    if f is None:
        return

    dataFrame = pd.DataFrame(data, columns=['Tid(s)', 'Bevegelse (mm)'])

    extension = f.name.split(".")[-1]

    if extension == "csv":
        dataFrame.to_csv(f.name)
    else:
        dataFrame.to_excel(f.name, index=False)

    f.close()
