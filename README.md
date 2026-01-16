# ProfeNoMeRepruebe
Si llego al 8??
---
## Detalles de python:
 ### Version de python:
  **Python 3.12**
  
  Se escribio completamente en utilizando Pycharm
  
## Paqueterias Necesarias:
  * Numpy
  * OpenCV / cv2
  * Pillow / PIL
  * Pandas (Tecnicamente no se utiliza pero por si las moscas estara instalado)

## Guia para gente que quiera usar en su estado actual
> ESTA VERSION ESTA DISEÑADA PARA QUE SOLO SE USE EL ALGORITMO EVOLUTIVO PRINCIPAL
 1. Instalar las librerias necesarias
 2. El algoritmo principal esta dentro del archivo **Test_Agent_explorer.py** 
 3. En la parte debajo del codigo de la clase se encuentra un uso para pruebas

### class Evolutivo()
> ADVERTENCIA: Puede que dado mapas particularmente grandes y habitados, puede que el algoritmo falle debido a el limite de recursividad de python.


| Parametro | |Descripcion | Tipo (datos permitidos) |
| :---: | :--- | :--: |
| **width** | Longitud Horizontal del mapa | int |
| **height** | Longitud Vertical del mapa | int |
| **p_mapa** | Probabilidad de que un espacio sea habitable | float *(0-1)* |
| **poblacion:** | Numero de individuos/soluciones que se exploraran a la vez | int |
| **p_mutacion** | Probabilidad de que un dato mute | float *(0-1)* |
| **gen_max** | Numero de generaciones a iterar | int |
| **seed** | Semilla para las funciones aleatorias | string |
| **agente_lados** | determina si el agente evaluativo explora 4 u 8 lados | int(4 u 8) |
 
