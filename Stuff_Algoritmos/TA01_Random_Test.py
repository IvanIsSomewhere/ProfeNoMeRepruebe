import Stuff_Test.Test_Create_Grid_2 as stg
import Stuff_Test.Test_Agent_explorer as AG
import random
import cv2

x = 12
y = 12

prob_think = .7
'''
    Para problematizar el algoritmo tengo que crear un agente capaz de checar la interconectividad de las celulas.
'''



Mapa = stg.Map(12,12,18)
mapa_test = Mapa
mapa_best = Mapa

random.seed("balatro")

for i in range(x):
    for j in range(y):
        if random.randrange(0,1) >= prob_think:
            mapa_test.change_cell(i,j,1)



#print(mapa_test.grid)



agente = AG.Explorer(mapa_test.grid)

agente.correr()
agente.show_explored()
mapa_test.show_cv2()