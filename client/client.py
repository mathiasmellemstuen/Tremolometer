from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from matplotlib import widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import xticks
import pandas as pd

deviceConnected = False

# Window
window = Tk()
window.title("Tremolometer")
window.configure(bg="white")

# List of tuples with x (s) and y (mm) elements
data = [(1, 1), (2, 2), (3, 2.2), (4, 4), (5, 5)]

figure = Figure(figsize = (19, 5))
plot = figure.add_subplot(111)
plot.set_xlabel("Tid (s)")
plot.set_ylabel("Bevegelse (mm)")
plot.grid(color='gray', linestyle='dashed')
plot.plot([element[0] for element in data], [element[1] for element in data], color = (1.0, 0.0, 0.0))
plot.set_xticks(range(0,21))
plot.set_xlim([0, 20])
figure.tight_layout()

canvas = FigureCanvasTkAgg(figure, master = window)
canvas.draw()

widget = canvas.get_tk_widget()
widget.grid(column = 1, row = 2 , columnspan=11, sticky = W + E)

def dataToCSVString(): 
    csvString = "\"Tid(s)\",\"Bevegelse (mm)\""
    for element in data: 
        csvString += f'\n{element[0]},{element[1]}'
    
    return csvString

def start():
    if deviceConnected: 
        measuringUI()
    else: 
        messagebox.showwarning(title="Ikke tilkoblet", message = "Koble til tremolometer via USB og prøv igjen.")

def saveAsCSV():  
    f = filedialog.asksaveasfile(title="Lagre som csv", defaultextension = ".csv", filetypes = [("CSV fil", "*.csv")])

    if f is None: 
        return

    f.write(dataToCSVString())
    f.close()

def saveAsXLSX():
    f = filedialog.asksaveasfile(title="Lagre som XLSX", defaultextension = ".xlsx", filetypes = [("Excel fil", "*.xlsx")])

    if f is None: 
        return

    path = f.name 
    f.close()
    dataFrame = pd.DataFrame(data, columns=['Tid(s)', 'Bevegelse (mm)'])
    dataFrame.to_excel(path, index=False)

# Creating GUI objects
frequencyLabel = Label(text="Frequency: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
measureLabel = Label(text="Måling: 0 / 20 s", background="white", foreground="black", anchor="center")
connectionLabel = Label(text="Tilkoblet", background="white", foreground="green", anchor="e", padx=25)
startButton = Button(text="Start", padx=10, pady= 10, background="white", foreground="black", command = start)
saveCSVButton = Button(text="Lagre som csv", padx=10, pady=10, background="white", foreground="black", command = saveAsCSV)
saveXLSSButton = Button(text="Lagre som xlsx", padx=10, pady=10, background="white", foreground="black", command = saveAsXLSX)

def disconnectedUI():

    connectionLabel.configure(text="Ikke tilkoblet")
    connectionLabel.configure(foreground="red")

    startButton.grid(column=1, row=1, sticky ="news", padx = 20, pady = 20)
    frequencyLabel.grid(column=1, row=3, sticky="news", padx = 20, pady = 20)
    measureLabel.grid(column=6, row=1, sticky="news")
    connectionLabel.grid(column=11, row=1, sticky="news")

def connectedUI(): 
    pass

def measuringUI():
    pass

def finishedUI():
    saveCSVButton.grid(column=10, row=3, sticky="news", padx=20, pady=20)
    saveXLSSButton.grid(column=11, row=3, sticky="news", padx=20, pady=20)

def update():
    canvas.draw()
    window.after(1, update)


disconnectedUI()
finishedUI()
update()

window.mainloop()