"""
Para la implementacion de el algoritmo genetico que resuleve el problema de las N-Reynas utilizamos la librearia DEAP,
por lo que es necesario importar las diferentes herramientas para poder utilizarlo correctamente, ademas que se usa
numpy y matplotlib para la visualizacion de resultados.
"""
import random
import numpy
import matplotlib.pyplot as plt
from deap import base
from deap import creator
from deap import tools
#se determina la semilla para la aleatoriedad.
random.seed(69)
N = int(input("Ingresa el tamaño del tablero: "))

"""
La funcion fitness recibira un individuo y comprobarar que no existan choques en sus diagonales, 
choque_izq, choque_Der y repetidos son del tamaño 2*size - 1 para que los indices donde ocurren choques no se salgan del rango.
si hay choque se incrementa su debida variable y despues se checha en donde hubo choque y se regresa el valor del fitness, entre menor mejor.  
"""

def fitness(individuo):
    size = len(individuo)
    choque_Izq = [0] * (2*size-1)
    choque_Der = [0] * (2*size-1)
    repetidos = [0] * (2*size-1)
    for i in range(size):
        if(individuo.count(individuo[i])>1):
            repetidos[individuo[i]] += 1
        choque_Izq[i+individuo[i]] += 1
        choque_Der[size-1-i+individuo[i]] += 1
    suma = 0
    for i in range(2*size-1):
        if(repetidos[i] > 1):
            suma += repetidos[i] - 1
        if choque_Izq[i] > 1:
            suma += choque_Izq[i] - 1
        if choque_Der[i] > 1:
            suma += choque_Der[i] - 1
    return suma,

"""La funcion de choque recibe un tablero, y calcula con un proceso parecido al del fitness si existe o no un choque
 en caso de existir, regresa las posiciones donde ocurren dichos choques, si no regresa una lista vacia.
"""

def choque(tablero):
    size = len(tablero)
    choque_Izq = [0] * (2*size-1)
    choque_Der = [0] * (2*size-1)
    repetidos = [0] * (2*size-1)
    for i in range(size):
        if(tablero.count(tablero[i])>1):
            repetidos[tablero[i]] += 1
        choque_Izq[i+tablero[i]] += 1
        choque_Der[size-1-i+tablero[i]] += 1
    choques = []
    o = 0
    for i in range(2*size-1):
        if(o == size-1):
            o = 0
        if(repetidos[tablero[o]]>1):
            choques.append((o,tablero[o]))
        if(choque_Izq[o+tablero[o]]>1):
            choques.append((o,tablero[o]))
        if(choque_Der[size-1-o+tablero[o]]>1):
            choques.append((o,tablero[o]))
        o+=1
    return choques

"""Se definen las propiedades a utilizar para el algoritmo, la funcion fitness en su parametro de 'weights' se le da un -1.0 por que se desea
que sea una funcion de minimizacion.
el individuo es una lista y se vincula con la funcion de fitness.

para el toolbox, se usa una permutacion para hacer los individuos de manera aleatoria y su rango de numeros ira hasta N.
se define como es que se creara el individuo.
se define el tipo de la poblacion
se define como se va a evaluar los individuos.
y por ultimo se definen los metodos de seleccion y cruce, asi como la forma en que ocurrira la mutacion"""

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(N), N)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/N)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(seed=0):
    pop = toolbox.population(n=int(input("Ingresa el tamaño de la Poblacion: ")))
    stats = {"MAX":[],"MIN":[],"AVG":[]}
    cxPB = float(input("Ingresa la Probabilidad de Cruzamiento: "))
    mutacion = float(input("Ingresa la Probabilidad de Mutacion: "))
    #se obtienen los valores del fitness de la poblacion
    fitnessvals = [n for x in map(toolbox.evaluate,pop) for n in x]
    #se emparejan los individuos de la poblacion con los valores de fitness
    for ind,fit in zip(pop,fitnessvals):
        ind.fitness.values = tuple([fit,])
    generacionMax = int(input("Ingresa el numero de generaciones:"))
    generacion = 0
    while(max(fitnessvals) < 100 and generacion < generacionMax):
        fitnessvals = [n for x in map(toolbox.evaluate,pop) for n in x]
        maximo = max(fitnessvals)
        minimo = min(fitnessvals)
        avg = numpy.mean(fitnessvals)
        stats["MAX"].append(maximo)
        stats["MIN"].append(minimo)
        stats["AVG"].append(avg)
        generacion += 1
        print("Generacion #",generacion)
        print("MAX: ",maximo)
        print("MIN: ",minimo)
        print("AVG: ",avg)

        #obtiene los hijos aplicando el metodo de seleccion definido
        hijos = toolbox.select(pop,len(pop))

        hijos = list(map(toolbox.clone,hijos))

        #de la lista de hijos toma el primero y segundo hijo, hasta llegar al final del arreglo
        for hijo1,hijo2 in zip(hijos[0::2], hijos[1::2]):
            if(random.random() < cxPB):
                #si los individuos logran cruzarse, entonces se obtienen dos hijos y se invalidan sus respectivos valores de fitness
                toolbox.mate(hijo1,hijo2)
                del hijo1.fitness.values
                del hijo2.fitness.values

        #dependiendo de la probabilidad se impone una mutacion
        for individuo in hijos:
            if(random.random() < mutacion):
                toolbox.mutate(individuo)
                del individuo.fitness.values

        #se actualizan todos los valores de fitness invalidos(hijos).
        ind_invalido = [ind for ind in hijos if not ind.fitness.valid]
        fits = map(toolbox.evaluate, ind_invalido)
        for ind, fit in zip(ind_invalido,fits):
            ind.fitness.values = fit
        #se reemplaza la poblacion actual con los hijos
        pop[:] = hijos
    return pop,stats

if __name__ == "__main__":
    res = main()
    #se organizan los valores obtenidos de las generaciones
    res[1]["AVG"].sort(key=lambda x:-x)
    res[1]["MAX"].sort(key=lambda x:-x)
    res[1]["MIN"].sort(key=lambda x:-x)
    print("""
    
    POBLACION FINAL
    
    """)
    for n in res[0]:
        print(n)
    print("""
    
    Solucion Final FINAL
    
    """)

    solucion = min(res[0],key=lambda x:fitness(x))
    print(solucion," Con Fitness de : ",fitness(solucion))
    print("MAX: ",numpy.average(res[1]["MAX"]),"MIN: ",numpy.average(res[1]["MIN"]),"AVG: ",numpy.average(res[1]["AVG"]))
    choques = choque(solucion)
    choques = list(set(choques))
    choquesX = [x[0] for x in choques]
    choquesY = [x[1] for x in choques]

    x = [x+0.5 for x in numpy.arange(0, N, 1)]
    y = [x+0.5 for x in solucion]

    x2 = [x+0.5 for x in choquesX]
    y2 = [x+0.5 for x in choquesY]
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(numpy.arange(0, N, 1))
    ax.set_yticks(numpy.arange(0, N, 1))
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.scatter(x,y,c="g",label="Reinas")
    ax.scatter(x2,y2,c="r",label="Choques")
    plt.legend(loc="upper left")
    plt.ylabel("RENGLONES")
    plt.xlabel("COLUMNAS")


    plt.grid()
    plt.show()

    plt.close('all')

    plt.plot(res[1]['MIN'],'r',label = 'min')
    plt.plot(res[1]["MAX"],"b",label = "max")
    plt.plot(res[1]["AVG"],'g',label = "avg")
    plt.legend()
    plt.show()



