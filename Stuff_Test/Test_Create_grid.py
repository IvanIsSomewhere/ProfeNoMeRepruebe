import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

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


def build_square_map(X,Y,square_size = 24):
    #cada segmento del mapa sera un cuadro de 120x120 pixeles por defecto
    game_grid = np.zeros((X,Y,1))

    pixel_grid = np.zeros((X*square_size,Y*square_size,3),dtype=np.uint8)

    for  i in range(Y*square_size):
        for j in range(X*square_size):
            match (int(i/square_size)% 2):
                case 0:
                    if int(j/square_size)%2 == 0:
                        pixel_grid[j][i][0] = 255
                        pixel_grid[j][i][1] = 0
                        pixel_grid[j][i][2] = 0
                    else:
                        pixel_grid[j][i][0] = 0
                        pixel_grid[j][i][1] = 0
                        pixel_grid[j][i][2] = 0
                case 1:
                    if int(j/square_size)%2 == 0:
                        pixel_grid[j][i][0] = 0
                        pixel_grid[j][i][1] = 0
                        pixel_grid[j][i][2] = 0
                    else:
                        pixel_grid[j][i][0] = 255
                        pixel_grid[j][i][1] = 0
                        pixel_grid[j][i][2] = 0




    return game_grid, pixel_grid


