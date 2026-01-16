import random
from PIL import Image, ImageTk
import numpy as np
import cv2



class Map:
    def __init__(
            self,
            x=30,
            y=30,
            pixel_width = 12,
            type= "square",
        ):

        #informacion de la cuadricula
        self.x = x
        self.y = y
        self.px_width = pixel_width
        self.type =type


        '''
        ----------------------------------------------------------------------
        Creacion del grid basico:
            grid = informacion abstracta del grid
            px_gird = grid pixel a pixel
            
        ----------------------------------------------------------------------
        '''
        self.cell_data = {
            "Caminable" : 0, #el valor debe ser 0 1

        }
        self.pixel_data = {
            "rgb" : [0,0,0],
            "px_state" : 0,
        }

        #llenar pixeles
        self.grid = np.zeros(
            shape= (self.x,self.y),
            dtype=np.int64
        )
        self.grid_pixel= np.zeros(
            shape= (
                self.x,
                self.y,
                self.px_width,
                self.px_width,
                3
            ),
            dtype = np.int64
        )
        self.grid_pixel_deph = np.zeros(
            #Grid que determina la "Altura del pixel al pixel
            shape = (
                self.x,
                self.y,
                self.px_width,
                self.px_width
            )
        )

        for X in range(self.x):
            for Y in range(self.y):
                #print (X)
                if (X%2 == 0 and Y%2 == 1) or (X%2 == 1 and Y%2 == 0):
                    self.grid_pixel[X][Y][:][:][:]=0
                    #print("a")
                else:
                    self.grid_pixel[X][Y][:][:][:] = 255
                    #print("b")


    '''
    ---------------------------------------------------
    FUNCIONES DE PRUEBA
    ---------------------------------------------------
    '''
    def print_sample_cell(self):
        print(self.grid[0][0])
        print(self.grid_pixel[0][0][0][0][:])


        print(self.grid[0][1])
        print(self.grid_pixel[0][1][0][0][:])

    '''
    -----------------------------------------------------
        FUNCIONES DE MODIFICACION DE CELDA
            *change_cell : celda individual
    -------------------------------------------------------
    '''

    def change_cell(self,cell_x,cell_y,state = -1):
        match state:
            case 0:
                self.grid[cell_x,cell_y] = 0

                if (cell_x % 2 == 0 and cell_y % 2 == 1) or (cell_x % 2 == 1 and cell_y % 2 == 0):
                    self.grid_pixel[cell_x,cell_y,:,:,:] = 0
                    # print("a")
                else:
                    self.grid_pixel[cell_x,cell_y,:,:,:] = 255
                    # print("b")
            case 1:
                self.grid[cell_x][cell_y] = 1
                self.grid_pixel[cell_x,cell_y,:,:,:] = 0
                self.grid_pixel[cell_x,cell_y,:,:,2] = 254
                #( f" se actualizo esto: {self.grid_pixel[cell_x][cell_y][0][0][2]}")
            case _:
                match self.grid[cell_x][cell_y]:
                    case 0:
                        self.grid[cell_x][cell_y] = 0
                        if (cell_x % 2 == 0 and cell_y % 2 == 1) or (cell_x % 2 == 1 and cell_y % 2 == 0):
                            self.grid_pixel[cell_x][cell_y][:][:][:] = 0
                            # print("a")
                        else:
                            self.grid_pixel[cell_x][cell_y][:][:][:] = 255
                            # print("b")
                    case 1:
                        self.grid[cell_x][cell_x] = 1
                        self.grid_pixel[cell_x][cell_y][:][:][0] = 0
                        self.grid_pixel[cell_x][cell_y][:][:][1] = 0
                        self.grid_pixel[cell_x][cell_y][:][:][2] = 255


    def _check_grid(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i,j] == 0:
                    if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                        self.grid_pixel[i,j,:,:,:] = 0
                        # print("a")
                    else:
                        self.grid_pixel[i,j,:,:,:] = 255
                        # print("b")
                else:
                    self.grid_pixel[i,j,:,:,:] = 0
                    self.grid_pixel[i,j,:,:,2] = 255

    def _import_grid_array(self,array, type = "grid"):
        #funcion para que se importe el mapa de un arreglo
        if type== "grid":
            if len(array) == self.x and (len(array[0]) == self.y):
                for i in range(len(array)):
                    for j in range(len(array[0])):
                        self.change_cell(i,j,array[i,j])

        return



    '''
    ----------------------------------------------------------------------------
        FORMAS DE EXPORTAR EL MAPA
        *   return_map_as_array
        *   return_map_as_image ("PIL" o "cv2")
        FORMAS DE VISUALISAR EL MAPA    
        *   show_cv2 
              
    --------------------------------------------------------------------------
    '''

    def return_map_as_array(self):
        w = self.x * self.px_width
        h = self.y * self.px_width
        array = np.zeros(shape=(self.x * self.px_width,self.y * self.px_width,3),dtype= np.uint8)

        for i in range(self.x):
            for j in range(self.y):
                for k in range(self.px_width):
                    for l  in range(self.px_width):
                        array[(i*self.px_width + k),(j*self.px_width+l),0] = self.grid_pixel[i,j,k,l,0]
                        array[(i*self.px_width + k),(j*self.px_width+l),1] = self.grid_pixel[i,j,k,l,1]
                        array[(i*self.px_width + k),(j*self.px_width+l),2] = self.grid_pixel[i,j,k,l,2]

        return array


    def return_map_as_image(self, format = "PIL"):
        array = self.return_map_as_array()
        image = Image.fromarray(array)

        if format == "cv2":
            numpy_image_rgb = array
            opencv_image = cv2.cvtColor(numpy_image_rgb, cv2.COLOR_RGB2BGR)
            image = opencv_image

        return image

    def show_cv2(self):
        img = self.return_map_as_image("cv2")
        img = cv2.resize(img,(500,500))
        cv2.imshow("MAP TEST", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class Map_string:
    def __init__(self,
                 x,
                 y,
                 ):
        self.width = x
        self.height =y
        self.length = x*y


        self.binary_string = np.zeros(shape=(x*y))
        self.matrix = np.zeros(shape=(x,y))



    def switch_val_s(self,val):
        if self.binary_string[val] == 0:
            self.binary_string[val] = 1

            _y = val // self.width  # Integer division
            _x = val % self.width

            self.matrix[_x,_y] = 1
        else:
            self.binary_string[val] = 0

            _y = val // self.width  # Integer division
            _x = val % self.width

            self.matrix[_x, _y] = 0



    def import_string(self,array_1d):
        if len(array_1d) == (self.width * self.height):
            i = 0
            x = 0
            y = 0

            for i in range(len(array_1d)):
                y = i // self.width
                x = i % self.width
                self.matrix[x,y] = array_1d[i]
                self.binary_string[i] = array_1d[i]

        return

    def map_randomize(self, prob = .7):
        arreglo = np.zeros(self.length)

        #probabilidad

        for i in range(self.length):
            if random.uniform(0,1) <= prob :
                arreglo[i] = 1


        self.import_string(arreglo)







#mapa= Map(10,10)

#print(mapa.show_cv2())
