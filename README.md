# Cueva helada

El juego del laberinto es una actividad enfocada a que los alumnos desarrollen destreza a la hora de utilizar las recta en el plano y sus ecuaciones. 
Se trata de una carrera entre dos o más alumnos en el que cada uno ocupa un punto en un laberinto parametrizado y estos tienen que lograr llegar a la 
meta a través de movimientos descritos por una recta. El juego se desarrolla en turnos en los que el jugador tendrá que proporcionar una ecuación de
una recta que pase por el punto en el que se encuentra para moverse a la siguiente posición. La intersección de esta recta con la primera pared del 
laberinto, será la nueva posición alcanzada.

Este juego ha sido implementado en un programa de Python para poder automatizar la visualización de las rectas, los puntos de corte con las paredes del laberinto,
la verificación de que la recta pasa por el punto inicial, etc. Para la implementación del programa hemos tenido que sortear algunos retos. 
En primer lugar, la aproximación de los cálculos. Se quería evitar que un alumno estuviese en posiciones como (5.66666667,1.00000001) por ejemplo.
Para ello se ha definido un épsilon (EPS) para aproximar los número a la fracción más cercana posible. La función rational (v) 
automatiza este proceso para utilizarlo a la hora de mostrar a los alumnos su posición en el plano mediante fracciones.
Otro problema es el caso de las rectas con pendiente infinita. Aunque los alumnos no van a poder meter estas rectas porque se les pide dar la ecuación implícita:
$y=mx+b$,
los muros del laberinto sí serán segmentos de rectas verticales. Es importante tener en cuenta estos casos dentro del programa porque pueden conducir a 
divisiones entre 0 al calcular los puntos de intersección de una recta con un muro vertical.

Por último, el reto más grande ha sido modelar correctamente los puntos de intersección de las rectas y la dirección en la que se mueven. Hay que tener
en cuenta que un punto en el plano no es suficiente para definir la posición de un jugador, es necesario también especificar en qué lado del muro se encuentra. 
El lado del muro en el que se encuentra un jugador define la dirección que puede tomar la tortuga respecto a una recta dada, la dirección no permitida sería la 
que atravesaría el muro. Una vez conocida la recta y la dirección, se calculan todas las interacciones de la recta con los obstáculos o conjunto de segmentos que 
definen el laberinto, se descartan los que se encuentran del otro lado del muro anterior y se toma el punto intersección que se encuentre más cerca del punto anterior. 
Este algoritmo es el que se utiliza en la función move() de la clase Player().

Mediante el paquete py2exe se puede exportar este programa a un archivo ejecutable para ser descargado por cada alumno en el aula de ordenadores.
