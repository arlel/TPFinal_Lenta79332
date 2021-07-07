import copy
import enum
import random as rnd
import entidades as entity
global fila

politicas = []
cantidadDiasSimulacion = 360
stockInicial = 20
fila = entity.Fila(0, "null")


def cargarPoliticas():
    # creacion de las politicas
    politicas.append(entity.Politica(180, 7, "Politica A"))
    politicas.append(entity.Politica(0, 15, "Politica B"))
    politicas[1].setAcumularDias(10)
    politicas.append(entity.Politica(100, 5, "Politica C"))
    salida = []
    for i in politicas:
        salida.append(i.getNombre())
    return salida


def empezarSimulacion(politicaSeleccionada):
    global fila
    politica = obtenerPolitica(politicaSeleccionada)
    fila = entity.Fila(stockInicial, politica)
    salida = mostrarFila(fila.mostrarFila())
    return salida


def obtenerPolitica(p):
    for i in politicas:
        if i.getNombre() == p:
            return i


def mostrarFila(v):
    # si quiero que me muestre el stock en 0 cuando este sea 0
    temp = copy.deepcopy(v)
    for i in range(1, 9, 1):
        if i != 3:
            if temp[i] == 0 or v[i] == 0.0:
                if not(temp[0] > 0 and i == 2):
                    temp[i] = ""

    return temp


# A partir de la fila en la que estoy, calculo la siguiente fila.
def calcularSiguienteFila():
    global fila
    fila = fila.calcularProximaFila()
    temp = mostrarFila(fila.mostrarFila())
    return temp
