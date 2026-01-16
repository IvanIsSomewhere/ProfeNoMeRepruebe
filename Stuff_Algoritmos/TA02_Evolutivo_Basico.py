import random
from array import array

import numpy as np
import time

import Stuff_Test.Test_Create_Grid_2 as Mapas
import Stuff_Test.Test_Agent_explorer as Agente






class Evolutivo():

    def __init__(self,
                 width = 20, # x len
                 height = 20, #y len
                 p_mapa = .30, #probabilidad de que aparezcan espacios habitables en el mapa

                 poblacion = 5, #poblacion de soluciones
                 p_mutacion = .2, #probabilidad de que mute un espacio
                 gen_max = 1, #numero maximo de generacion
                 seed = "balatro", #la semilla que determina que hace
                 agente_lados = 4 # solo se permiten 4 u 8
                 ):
        self.width = width
        self.height = height
        self.length = width * height


        self.p_mapa = p_mapa
        self.p_mutacion = p_mutacion
        self.agente_lados = agente_lados

        self.n_poblacion = poblacion

        self.gen_max = gen_max
        self.seed = seed

        self.individuos_seleccionables = int(self.n_poblacion/5) + 1
        self.crossover_points_n = int(self.length/25+1)

        '''
            history_score =  arreglo historial del puntaje de todas las soluciones.
            history_best_score = arreglo historial de todas las mejores soluciones
            history_best_map = arreglo que guarda todos los mejores mapas
        
        '''
        self.generacion = 0
        self.history_score = []
        self.history_best_score = []
        self.history_best_map = []
        self.history_average_best = [] #Lista de la aptitud promedio de el mapa conforme se desarolla el promedio

        self.score = 0 # % de veces que se muto
        self.solutions_xplored = 0 # numero de soluciones exploradas

        self.has_run = False

        '''
        ----------------------------------
        Checklist:
            1. Iniciacion x
    
            2. Evaluacion x
            3. Seleccion x
            4. Cruzamiento
            5. Mutacion
            6  Reemplazo
    
            7. Finalizar
            -----------------------------
        '''

    def _bubblesort_scores(self,arr_puntajes,arr_soluciones):
        if self.n_poblacion ==1:
            return arr_puntajes, arr_soluciones

        _sorted = False

        _score_ordenado = arr_puntajes
        _solut_ordenado = arr_soluciones

        while _sorted == False:
            _sorted = True
            for i in range(1,len(arr_puntajes)):
                #la lista va en orden descendiente.

                if _score_ordenado[i-1] < _score_ordenado[i]:
                    #swap scores
                    _sorted = False

                    _sco = _score_ordenado[i]
                    _sol =  _solut_ordenado[i]

                    _score_ordenado[i] = _score_ordenado[i-1]
                    _solut_ordenado[i] = _solut_ordenado[i-1]

                    _score_ordenado[i-1] = _sco
                    _solut_ordenado[i-1] = _sol

        return arr_puntajes, arr_soluciones

    def _limpiar_poblacion(self):
        for i in range(self.n_poblacion):
            self.population[i].import_string(self.population[i].binary_string)


    def inicializar(self):
        #1. INICIALIZACION------------------------------------------------------------------
        self.population = []
        random.seed(self.seed)

        for i in range(self.n_poblacion):

            self.population.append(Mapas.Map_string(self.width,self.height))
            self.population[i].map_randomize(self.p_mapa)


        #proceso para guardar en que parte de los puntos se alternara.
        self.crossover_step = int(self.length / self.crossover_points_n)
        self.crossover_points = [0]
        for i in range(1,self.crossover_points_n):
            self.crossover_points.append(i*self.crossover_step)
        #print(self.crossover_points_n)






    def loop(self):
        '''
        -----------------------------------------------------------------------------------------------------------
            #2. EVALUACION
            1. Se evalua la generacion actual
            2. Se guarda el mejor resultado
            3. Se actualiza el historial.
        ----------------------------------------------------------------------------------------------------------
        '''


        lista_puntajes = np.zeros(shape=(self.n_poblacion))
        lista_soluciones = np.zeros(shape=(self.n_poblacion,self.width*self.height))

        current_best_solution = 0
        current_best_score = 0

        for i in range(self.n_poblacion):
            lista_soluciones[i] = self.population[i].binary_string

            agente = Agente.Explorer(self.population[i].matrix,directions= self.agente_lados)
            lista_puntajes[i] = agente.correr_return()



            if lista_puntajes[i] > current_best_score:
                current_best_solution = self.population[i]
                current_best_score = lista_puntajes[i]



        #Guardar toda la informacion de los mejores puntajes
        self.history_score.append(lista_puntajes)
        if (self.history_best_score != []):
            if current_best_score > self.history_best_score[-1]:
                print("better_score")
                self.history_best_score.append(current_best_score)
                self.history_best_map.append(current_best_solution)
            else:
                self.history_best_score.append(self.history_best_score[-1])
                self.history_best_map.append(self.history_best_map[-1])
        else:
            self.history_best_score.append(current_best_score)
            self.history_best_map.append(current_best_solution)

        '''
        ---------------------------------------------------------------------------------------------------------------
        3. Seleccion
            Por ahora tomare el numero de "mejores soluciones" aceptadas como 1/5 poblacion +1 (vease arriba)
            0. Ordear los mayores resultados
            1.Seleccionar los mejores de la lista de un numero de soluciones seleccionables.
            2.guardarlos para mezclar con otras.
        --------------------------------------------------------------------------------------------------------------
        '''

        _seleccion_soluciones = np.zeros(shape = (self.individuos_seleccionables, self.width * self.height))
        _seleccion_puntajes = np.zeros(shape = (self.individuos_seleccionables))

        _puntaje_ordenado,_soluciones_ordenadas = self._bubblesort_scores(lista_puntajes,lista_soluciones)
        #print(_puntaje_ordenado)

        for i in range(self.individuos_seleccionables):
            _seleccion_soluciones[i] = _soluciones_ordenadas[i]
            _seleccion_puntajes[i] = _puntaje_ordenado[i]

        #print((_seleccion_puntajes))
        '''
        ------------------------------------------------------------------------------------------------------------
        4. CROSSOVER / CRUZA
           
            0.Se crea el arreglo de soluciones hijos
            1. Se mantiene la mejor solucion
            2. Se mezclan el resto de los hijos con 
            
        ----------------------------------------------------------------------------------------------------------
        '''
        _child_solutions = np.zeros(shape=(len(self.population),self.length))

        _child_solutions[0] = current_best_solution.binary_string

        for i in range(1,self.n_poblacion):
            #seleccion de los 2 padres:
            _parent_champion = _seleccion_soluciones[(random.randint(0,self.individuos_seleccionables-1))]
            _parent_random   = lista_soluciones[(random.randint(0,self.n_poblacion-1))]


            for z in range(1,self.crossover_points_n):
                #seleccionar un padre de los 2 aleatoriamente
                if (random.randint(0,1) == 0):
                    #selecciona las secciones del padre campeon y lascopia al hijo
                    _child_solutions[i,self.crossover_points[z-1]:self.crossover_points[z]] = _parent_champion[self.crossover_points[z-1]:self.crossover_points[z]]
                else:
                    #selecciona las secciones del padre aleatorio y las copia al hijo
                    _child_solutions[i, self.crossover_points[z - 1]:self.crossover_points[z]] = _parent_champion[
                                                                                                 self.crossover_points[
                                                                                                     z - 1]:
                                                                                                 self.crossover_points[
                                                                                                     z]]

        '''
        ---------------------------------------------------------------------------------------------------------------
        5. MUTACION
            0. Pasar por la cadena donde cada dato individual puede modificarse.
               *En general creo que lo ideal es que el chance de mutacion sea mas pequeño que la probabilidad de
                espacios en el mapa, debido a que si son el mismo o mayor puede que se termine rehaciendo todo el mapa
                completamente
        ---------------------------------------------------------------------------------------------------------------
        '''
        _mutation_score = 0 # porcentaje de la poblacion que ha sido modificado.

        for i in range(1,self.n_poblacion):

            for j in range(self.length):
                if (random.uniform(0,1) <= self.p_mutacion):
                    if _child_solutions[i,j] == 1:
                        _child_solutions[i, j] = 0
                    else: _child_solutions[i, j] = 1
                    _mutation_score += 1

        _mutation_score = (_mutation_score)/(self.n_poblacion * self.length)
        #print(f"mutacion = {_mutation_score}")

        '''
        ---------------------------------------------------------------------------------------------------------------
        5. REMPLAZO
            La generacion de hijos sustituye a los papas.
        ---------------------------------------------------------------------------------------------------------------
        '''

        for i in range(self.n_poblacion):
            self.population[i].import_string(_child_solutions[i])

    def conclude(self):
        '''
        Funcion para hacer la evaluacion final sin modificacion adicional
        '''

        lista_puntajes = np.zeros(shape=(self.n_poblacion))
        lista_soluciones = np.zeros(shape=(self.n_poblacion, self.width * self.height))

        current_best_solution = 0
        current_best_score = 0

        for i in range(self.n_poblacion):
            lista_soluciones[i] = self.population[i].binary_string

            agente = Agente.Explorer(self.population[i].matrix,self.agente_lados)
            lista_puntajes[i] = agente.correr_return()

            if lista_puntajes[i] > current_best_score:
                current_best_solution = self.population[i]
                current_best_score = lista_puntajes[i]

        # Guardar toda la informacion de los mejores puntajes
        self.history_score.append(lista_puntajes)

        if (len(self.history_best_score) > 0):
            if current_best_score >= self.history_best_score[-1]:
                self.history_best_map.append(current_best_solution)
                self.history_best_score.append(current_best_score)
            else:
                self.history_best_map.append(self.history_best_map[-1])
                self.history_best_score.append(self.history_best_score[-1])
        else:
            self.history_best_score.append(current_best_score)
            self.history_best_map.append(current_best_solution)


        self._limpiar_poblacion()



    def correr(self):
        _start_time = time.time()

        self.inicializar()

        for i in range(self.gen_max):
            self.loop()

        self.conclude()


        _end_time = time.time()
        elapsed_time = _end_time - _start_time
        print(f"Algoritmo completado en: {elapsed_time}\n")
        self.has_run = True



    def evaluate(self,show = "none"):
        '''funcion para analizar resultados
            show:
                "none" = no mostrar nada fuera de la consola
                "true" muestra resultados en imagenes
                "full" muestra todos los detalles
        '''

        if self.has_run == False:
            print("El algoritmo no ha sido ejecutado")
            return

        print(f"Len history best score {len(self.history_best_score)}")
        print(f"Len history {len(self.history_best_map)}")

        print(f"Diferencia de puntaje entre el primer y ultimo mejor solucion:")
        print(f"{self.history_best_score[0]} --> {self.history_best_score[-1]}")
        print(f"diff= {self.history_best_score[-1] - self.history_best_score[0]} \n")

        #calcular que tanto cambio el mapa en #


        Mapa_resultado = Mapas.Map(self.width,self.height)
        Mapa_resultado._import_grid_array(self.history_best_map[-1].matrix)

        Agente_resultado = Agente.Explorer(map = self.history_best_map[-1].matrix, directions= self.agente_lados)
        print(f" agente final p = {Agente_resultado.correr_return()}")
        if show != "none":
            if show == "full":
                Mapa_resultado.show_cv2()

            Agente_resultado.show_explored()











        





'''
------------------------------------------------------------------------------------
        LINEA PARA DIVIDIR DONDE HAGO PRUEBAS PQ NECESITO CLARIDAD VISUAL
------------------------------------------------------------------------------------
'''

hola = Evolutivo(
    width       = 20,
    height      = 20,
    p_mapa      = .30,
    gen_max     = 13,
    poblacion   = 5,
    p_mutacion  = .40,
    agente_lados= 4,
    seed= "balatro")
hola.correr()
hola.evaluate("full")