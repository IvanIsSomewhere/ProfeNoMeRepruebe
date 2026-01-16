from pickletools import uint8

import numpy as np

import Stuff_Test.Test_Create_Grid_2 as TCG
import random
import sys
import cv2
from PIL import Image



class Explorer:
    def __init__(
            self,
            map = np.zeros((10,10)),
            initX = 0,
            initY= 0,
            directions = 4
    ):


        self.pos_y = initY
        self.pos_x = initX

        self.map_default = map
        self.map_width = len(map)
        self.map_height = len(map[0])
        self.directions = directions

        self.explorable_map = 0

        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map_default[i,j] != 0:
                    self.explorable_map += 1


        if self.explorable_map < 1:
            self.explorable_map = 1
        #print(f"Espacios explorables ={self.explorable_map}")
        self.map_explored = map

        self.score_max = 1
        self.score_current = 0
        self.score_per_cell = (self.score_max / self.explorable_map)
        #print(f"puntaje por espacio = {self.score_per_cell}")
        #print(f"Limite = {sys.getrecursionlimit()}")

    def _move_check(self,direction):
        '''
         checa la disponibilidad del mapa,
         utilizando las direcciones del numpad
        '''
        m_y = 0
        m_x = 0
        match direction:
            case 8:
                m_y = -1
            case 2:
                m_y = +1
            case 4:
                m_x = -1
            case 6:
                m_x = +1

                '''
                direcciones diagonales
            '''
            case 7:
                m_x = -1
                m_y = -1
            case 9:
                m_x = +1
                m_y = -1
            case 1:
                m_x = -1
                m_y = +1
            case 3:
                m_x = +1
                m_y = +1


        if  0 <= (self.pos_x + m_x) < self.map_width:
            if 0 <= (self.pos_x + m_y) < self.map_height:
                if self.map_default[self.pos_x+m_x,self.pos_y+m_y] != 0:
                    return True
        return False
    def _move(self,direccion):
        m_y = 0
        m_x = 0
        match direccion:
            case 8:
                m_y = -1
            case 2:
                m_y = +1
            case 4:
                m_x = -1
            case 6:
                m_x = +1

            # direcciones diagonales
            case 7:
                m_x = -1
                m_y = -1
            case 9:
                m_x = +1
                m_y = -1
            case 1:
                m_x = -1
                m_y = +1
            case 3:
                m_x = +1
                m_y = +1

        self.pos_x +=  m_x
        self.pos_y +=  m_y

    def _find_starting_spot(self):
        if self.map_default[self.pos_x,self.pos_y] != 1:
            for y in range(self.map_height):
                for x in range(self.map_width):
                    if self.map_default[x,y] == 1:
                        self.pos_x = x
                        self.pos_y = y
                        return

    def _tick_map(self):
        self.map_explored[self.pos_x,self.pos_y] = 2


    def _flood(self,x,y):
        if (x < 0) or (y < 0) or x >= self.map_width or y>= self.map_height:
            return
        if (self.map_default[x,y] == 0) or (self.map_explored[x,y] == 2):
            return
        else:
            self.map_explored[x][y] = 2
            self.score_current = self.score_current + self.score_per_cell

            match self.directions:
                case 8:
                    self._flood(x, y - 1)  # arriba
                    self._flood(x - 1, y - 1)  # arriba izquierda
                    self._flood(x + 1, y - 1)  # arriba derecha

                    self._flood(x - 1, y)  # derecha
                    self._flood(x + 1, y)  # izquierda

                    self._flood(x + 1, y + 1)  # abajo derecha
                    self._flood(x, y + 1)  # abajo
                    self._flood(x - 1, y + 1)  # abajo izquierda

                case 4:
                    self._flood(x, y - 1)  # arriba
                    self._flood(x - 1, y)  # derecha
                    self._flood(x + 1, y)  # izquierda
                    self._flood(x, y + 1)  # abajo

    def _flood_fixed(self,x,y):

        return













    def _explored_to_image(self,format = "PIL"):
        arreglo = np.zeros((self.map_width*6,self.map_height*6,3),dtype= np.uint8)

        for i in range(self.map_width):
            for j in range(self.map_height):
                if self.map_explored[i,j] == 2:
                    arreglo[i*6:i*6+6,j*6:j*6+6,0] = 255

        img = Image.fromarray(arreglo)

        if format == "cv2":
            numpy_image_rgb = arreglo
            opencv_image = cv2.cvtColor(numpy_image_rgb, cv2.COLOR_RGB2BGR)
            img = opencv_image

        return img

    def show_explored(self):
        img = self._explored_to_image("cv2")

        img = cv2.resize(img, (500, 500))
        cv2.imshow("MAP TEST", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def correr(self):
        sys.setrecursionlimit(2000)
        self._find_starting_spot()
        self.score_current = 0
        #print(f"Posicion Inicial = {self.pos_x} , {self.pos_y}")

        self._flood(self.pos_x,self.pos_y)
        sys.setrecursionlimit(1000)
       # print(f"puntaje = {self.score_current}")


    def correr_return(self):
        sys.setrecursionlimit(2000)
        self._find_starting_spot()
        self.score_current = 0
        #print(f"Posicion Inicial = {self.pos_x} , {self.pos_y}")

        self._flood(self.pos_x,self.pos_y)
        #print(f"puntaje = {self.score_current}"
        sys.setrecursionlimit(1000)
        return self.score_current










