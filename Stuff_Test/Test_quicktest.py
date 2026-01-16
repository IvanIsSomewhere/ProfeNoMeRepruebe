'''
Esta parte es solo para comprobar que el codigo funcionara como quiero, de forma pequeña
'''


arreglo = [1]

while arreglo != []:
    while arreglo[-1] < 10:
        print(arreglo[-1])
        arreglo[-1] += 1
        arreglo.append(arreglo[-1]+1)

    arreglo.pop(-1)