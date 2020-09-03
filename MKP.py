import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Función que lee los archivos de dsistancia y flujo


def leeArchivo(nombre):
    nombre = "./archivos/" + nombre + ".txt"
    archivo = open(nombre, 'r')
    lista = []

    for linea in archivo:
        linea = linea.strip().split(' ')
        for elemento in linea:
            lista.append(int(elemento))

    valores_principales = lista[0:3]
    del lista[0:3]

    #  -----  Obtener valores principales --------
    objetos = valores_principales[0]
    dimensiones = valores_principales[1]
    # optimo = valores_principales[2]

    # ------ Lista de beneficios de cada objeto i --------
    beneficios = lista[0: objetos]
    del lista[0:objetos]

    lista_objetos = lista[0:(dimensiones*objetos)]
    del lista[0:(dimensiones*objetos)]

    matriz_pesos = []
    # matriz de objetos i con cada uno de sus pesos en las j dimensiones
    for i in range(dimensiones):
        fila = []
        for j in range(objetos):
            fila.append(lista_objetos[i * objetos + j])
        matriz_pesos.append(fila)

    # capacidad de cada dimension m
    capacidades = lista

    # trasponer matriz de pesos para acceder facilmente
    archivo.close()

    return objetos, beneficios, matriz_pesos, capacidades


def shuffle(cadena):
    lista = list(cadena)
    random.shuffle(lista)
    cadena = ''.join(lista)
    return cadena


def esFactible(solucion, matriz_pesos, capacidades):
    for j in range(len(matriz_pesos)):
        suma = 0
        for i in range(len(matriz_pesos[j])):
            if solucion[i] == '1':
                suma = suma + matriz_pesos[j][i]
        if suma > capacidades[j]:
            return False
    return True

# solucion inicial semi aleatoria con una probabilidad baja de que se obtena un 1


def solucionInicial(objetos, matriz_pesos, capacidades):
    cadena = ""
    for i in range(objetos):
        probabilidad = random.uniform(0, 1)
        if probabilidad < 0.35:
            cadena += '1'
        else:
            cadena += '0'
    # si no es factible se genera nuevamente una solución aleatoria
    if not esFactible(cadena, matriz_pesos, capacidades):
        cadena = solucionInicial(objetos, matriz_pesos, capacidades)
    return cadena


def funcionObjetivo(cadena, beneficios):
    valor_objetivo = 0
    i = 0
    for i in range(len(cadena)):
        valor_objetivo += beneficios[i] * int(cadena[i])

    return valor_objetivo


def generarVecino(solucion):
    i = random.randint(0, len(solucion)-1)
    lista = list(solucion)
    lista[i] = '1' if solucion[i] == '0' else '0'
    return ''.join(lista)


def probablidadAceptacion(delta, temperatura_actual):
    probabilidad = math.e ** -(delta/temperatura_actual)
    return probabilidad


def graficar(LIS, lista_mejors, lista_probabilidades, mejor_objetivo):
    plt.figure(1)
    plt.subplot(4, 1, 1)
    graficoMejores = plt.plot(lista_mejors)
    plt.setp(graficoMejores, "linestyle", "none", "marker",
             "s", "color", "b", "markersize", "1")
    plt.title(u"Simulated annealing QAP")
    plt.ylabel(u"Valor objetivo")
    plt.subplot(4, 1, 2)
    grafico = plt.plot(LIS)
    plt.setp(grafico, "linestyle", "none", "marker",
             "s", "color", "r", "markersize", "1")
    plt.ylabel(u"Valor actual")
    plt.subplot(4, 1, 3)
    grafico = plt.plot(lista_probabilidades)
    plt.setp(grafico, "linestyle", "none", "marker",
             "s", "color", "g", "markersize", "1")
    plt.ylabel(u"Probabilidad")
    plt.xlabel(u"Valor óptimo : " + str(mejor_objetivo))
    return True


def SimulatingAnniling(temperatura_actual, temperatura_minima, estado_equilibrio, enfriamiento, alpha, beta):
    # archivo = 'test'
    archivo = 'OR5x100-0.25_1'
    objetos, beneficios, matriz_pesos, capacidades = leeArchivo(archivo)

    # Inicializacion de variables
    solucion_inicial = solucionInicial(objetos, matriz_pesos, capacidades)
    solucion_actual = solucion_inicial
    # mejor_solucion = solucion_actual.copy()
    objetivo_actual = funcionObjetivo(solucion_inicial, beneficios)
    mejor_objetivo = objetivo_actual
    lista_objetivos = [objetivo_actual]
    lista_mejores = [objetivo_actual]
    lista_probabilidades = []

    while temperatura_actual > temperatura_minima:
        i = 0
        while i < estado_equilibrio:
            solucion_candidato = generarVecino(solucion_actual)
            if esFactible(solucion_candidato, matriz_pesos, capacidades):
                objetivo_candidata = funcionObjetivo(
                    solucion_candidato, beneficios)
                delta = objetivo_actual - objetivo_candidata
                if delta < 0:
                    solucion_actual = solucion_candidato
                    objetivo_actual = objetivo_candidata
                    if objetivo_candidata > mejor_objetivo:
                        mejor_objetivo = objetivo_candidata
                        # mejor_solucion = solucion_candidato
                else:
                    probabilidad = probablidadAceptacion(
                        delta, temperatura_actual)
                    lista_probabilidades.append(probabilidad)
                    if random.random() < probabilidad:
                        solucion_actual = solucion_candidato
                        objetivo_actual = objetivo_candidata
                lista_mejores.append(mejor_objetivo)
                lista_objetivos.append(objetivo_actual)

            print(
                f"Temperatura: {temperatura_actual} - Objetivo:actual: {objetivo_actual} - Mejor objetivo: {mejor_objetivo} - Solucion actual: {solucion_actual}")
            i = i + 1
        if enfriamiento == "lineal":
            temperatura_actual = temperatura_actual - beta
        else:
            temperatura_actual = temperatura_actual * alpha

    graficar(lista_objetivos, lista_mejores,
             lista_probabilidades, mejor_objetivo)
    plt.show()
    return mejor_objetivo


# print("---------------------------\n")
# print(f'Dimensiones: {dimensiones}')
# print(f'Objetos: {objetos}')
# print(f'Beneficios: {beneficios}')
# print(f'Capacidaddes: {capacidades}')
# print(f'Matriz de pesos: {matriz_pesos}')
# print("\n---------------------------")
# solucion_inicial = solucionInicial(objetos, matriz_pesos, capacidades)
# print(f"solucion inicial: {solucion_inicial}")
# es_factible = esFactible(solucion_inicial, matriz_pesos, capacidades)
# print(es_factible)
# valor = funcionObjetivo(solucion_inicial, beneficios)
# print(f"valor objetivo: {valor}")

temperatura_actual = 100000000000
temperatura_minima = 0.01
estado_equilibrio = 30
enfriamiento = "geometrico"
alpha = 0.99
beta = 0.99


SimulatingAnniling(temperatura_actual, temperatura_minima,
                   estado_equilibrio, enfriamiento, alpha, beta)


# objetos, beneficios, matriz_pesos, capacidades = leeArchivo('test')
# print(matriz_pesos)
# print(esFactible('011001', matriz_pesos, capacidades))
