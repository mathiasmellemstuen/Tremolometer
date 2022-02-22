from cgitb import text
from tkinter import *
from turtle import color
from matplotlib import widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import xticks
# Window
window = Tk()
window.title("Tremolometer")
window.configure(bg="white")

figure = Figure(figsize = (19, 5))
plot = figure.add_subplot(111)
plot.set_xlabel("Tid (s)")
plot.set_ylabel("Differanse (mm)")
plot.grid(color='gray', linestyle='dashed')
plot.plot([])
plot.set_xticks(range(0,21))
plot.set_xlim([0, 20])
figure.tight_layout()

canvas = FigureCanvasTkAgg(figure, master = window)
canvas.draw()

widget = canvas.get_tk_widget()
widget.grid(column = 1, row = 2 , columnspan=11, sticky = W + E)

startButton = Button(text="Start", padx=10, pady= 10, background="white", foreground="black")
startButton.grid(column=1, row=1, sticky ="news", padx = 20, pady = 20)

frequencyLabel = Label(text="Frequency: --Hz", padx=10, pady=10, background="white", foreground="black", anchor="w")
frequencyLabel.grid(column=1, row=3, sticky="news", padx = 20, pady = 20)

measureLabel = Label(text="Måling: 0 / 20", background="white", foreground="black", anchor="w")
measureLabel.grid(column=6, row=1, sticky="news")

connectionLabel = Label(text="Tilkoblet", background="white", foreground="green")
connectionLabel.grid(column=11, row=1, sticky="news")

def disconnectedUI():
    pass

def connectedUI(): 
    pass

def measuringUI():
    pass

def finishedUI():
    pass

def update():
    canvas.draw()
    window.after(1, update)



# Packing

# canvas.get_tk_widget().pack()
# label.pack()
# startButton.pack()

# Calling the update function for the first time
update()

window.mainloop()