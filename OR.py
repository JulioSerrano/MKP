from __future__ import print_function
from ortools.algorithms import pywrapknapsack_solver

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

    archivo.close()

    return objetos, beneficios, matriz_pesos, capacidades

objetos, beneficios, matriz_pesos, capacidades = leeArchivo('wshi')

profits = beneficios
weights = matriz_pesos
capacities = capacidades

solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver
    .KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
    'Multi-dimensional solver')
solver.Init(profits, weights, capacities)
profit = solver.Solve()

strint = ""
for i in range(len(profits)):
    strint += '1' if solver.BestSolutionContains(i) else '0'

# print(solver.BestSolutionContains(8))

print(strint)
print(profit)
