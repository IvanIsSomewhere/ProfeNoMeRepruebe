#aqui es donde debo crear la base para el sitio
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import Test_Create_grid as testcg

# Create the main window
root = tk.Tk()
root.title("My First App")
root.geometry("1000x1000")  # width x height


root.title("Basic Widgets")

# Create a label
label = tk.Label(root, text="Esto es una prueba!")
label.pack(pady=10)  # Add vertical padding

# Create a button
button = tk.Button(root, text="Click Me!")
button.pack(pady=10)


# Add this before mainloop()
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Button to get the entry text
def get_text():
    user_text = entry.get()
    print(f"You typed: {user_text}")

get_button = tk.Button(root, text="Get Text", command=get_text)
get_button.pack()


#okay digamos que queremos crear un grid sencillo
def create_rgb_grid(x,y):
    number = 0
    grid = np.zeros((y,x,3), dtype= np.uint8)

    for i in range(y):
        for j in range(x):
            match number:
                case 0:
                    grid[i,j,0] = 100
                    number = 1
                case 1:
                    grid[i, j, 1] = 100
                    number = 2
                case 2:
                    grid[i, j, 2] = 100
                    number = 0

    return grid

y = 100
x = 100
test_grid = create_rgb_grid(x,y)

#for i in range(x):
 #   for j in range(y):
 #       print((test_grid[i][j]), end = " | ")
 #   print("\n")


_, test_grid = testcg.build_square_map(x,y)

#test_grid = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)
pil_image = Image.fromarray(test_grid)
#Image._show(pil_image)

#mostrarlo en el grid
imagen_lista = ImageTk.PhotoImage(image=pil_image)
button = tk.Button(root, image=imagen_lista, command=lambda: print("Clicked!"))
button.image = imagen_lista  # Keep a reference to prevent garbage collection
button.pack(padx=20, pady=20)


root.mainloop()

