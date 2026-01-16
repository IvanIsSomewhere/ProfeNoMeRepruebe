#aqui es donde pruebo hacer el layout
import tkinter as tk
from tkinter.ttk import *

from PIL import Image, ImageTk
import numpy as np
#import Test_Create_grid as testcg


app = tk.Tk()
app.title = "Hola buenas tardes"
width = 720
length = 980
app.geometry(f"{length}x{width}")


texto1 = Label(app, text="hola")
texto1.grid(row = 0, column = 0, sticky = "w", pady = 2)

app.mainloop()