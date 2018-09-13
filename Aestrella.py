#es necesario importar la liberia time para que muestre el tiempo que tardo en la ejecucion
import time
"""
Definir la clase Node y sus propiedades
donde pos es una tupla con la posicion en X y en Y del objeto.
y en padre se almacenara el padre del nodo actual.
f = g(n) + h(n)
h = es la distancia de Manhattan 
g = es la distancia desde el inicio al nodo actual
se hizo Override a la funcion de __lt__ para obtener los valores mas pequeños de f durante la ejecucion
"""
class Node():
    def __init__(self,pos,padre=None,f = 0,h = 0,g = 0):
        self.pos = pos
        self.x = pos[1]
        self.y = pos[0]
        self.padre = padre
        self.f = f
        self.h = h
        self.g = g
    def printNodo(self):
        print("posicion: ",self.pos)
        print("\npadre: ",self.padre)
        print("\ndistancia f(g(n)+h(n)): ",self.f)
        print("\nheuristica h(n): ",self.h)
        print("\ndistancia g(n): ",self.g)
    def getDistance(self):
        return self.f
    def getPos(self):
        return self.pos
    #__lt__ es el equivalente a < b
    #se implemento para comparar los nodos dentro de una lista y obtener el menor
    def __lt__(self,other):
        return self.f < other.f

"""
la funcion generaHijos recibe como parametros el nodo del cual se obtendran los hijos,
el laberinto y la lista de nodos visitados.
En se comprobaran que sea un moviemiento valido las siguientes posiciones en este orden:
1.-Arriba
2.-Izquierda
3.-Derecha
4.-Abajo
"""
def generaHijos(nodo,world):
    hijos = []
    #up
    if(world[nodo.y-1][nodo.x] != "%" ):
        node = Node((nodo.y-1,nodo.x),nodo)
        hijos.append(node)
   #left
    if(world[nodo.y][nodo.x-1] != "%" ):
        node = Node((nodo.y,nodo.x-1),nodo)
        hijos.append(node)
	#right
    if(world[nodo.y][nodo.x+1] != "%" ):
        node = Node((nodo.y,nodo.x+1),nodo)
        hijos.append(node)
    #down
    if(world[nodo.y+1][nodo.x] != "%" ):
        node = Node((nodo.y+1,nodo.x),nodo)
        hijos.append(node)
    return hijos

#la funcion de distancia es utilizada para obtener las distancias de la heuristica
def distancia(nodo,final):
    return abs(final[1] - nodo.x ) + abs(final[0] - nodo.y)

start_time = time.time()
lista = []
visitados = []
inicio = (35,35)
final = (35,1)
tamanio = (37,37)
mapa = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-------%-%-%-----------%---%-----%-%
%-%%%%%%%-%-%%%-%-%%%-%%%-%%%%%%%-%-%
%-------%-------%-%-----%-----%-%---%
%%%%%-%%%%%-%%%-%-%-%-%%%-%%%%%-%-%%%
%---%-%-%-%---%-%-%-%---%-%---%-%---%
%-%%%-%-%-%-%%%-%%%%%-%%%-%-%%%-%%%-%
%-------%-----%---%---%-----%-%-%---%
%%%-%%%%%%%%%-%%%%%%%-%%%-%%%-%-%-%-%
%-------------%-------%-%---%-----%-%
%-%-%%%%%-%-%%%-%-%-%%%-%-%%%-%%%-%-%
%-%-%-----%-%-%-%-%-----%---%-%-%-%-%
%-%-%-%%%%%%%-%-%%%%%%%%%-%%%-%-%%%-%
%-%-%-%-----%---%-----%-----%---%---%
%%%-%%%-%-%%%%%-%%%%%-%%%-%%%-%%%%%-%
%-----%-%-%-----%-%-----%-%---%-%-%-%
%-%-%-%-%-%%%-%%%-%%%-%%%-%-%-%-%-%-%
%-%-%-%-%-----------------%-%-%-----%
%%%-%%%%%%%-%-%-%%%%%-%%%-%-%%%-%%%%%
%-------%-%-%-%-----%---%-----%-%---%
%%%%%-%-%-%%%%%%%%%-%%%%%%%%%%%-%-%%%
%---%-%-----------%-%-----%---%-%---%
%-%%%-%%%%%-%%%%%%%%%-%%%%%-%-%-%%%-%
%-%---%------%--------%-----%-------%
%-%-%-%%%%%-%%%-%-%-%-%-%%%%%%%%%%%%%
%-%-%---%-----%-%-%-%-------%---%-%-%
%-%-%%%-%%%-%-%-%-%%%%%%%%%-%%%-%-%-%
%-%---%-%---%-%-%---%-%---%-%-%-----%
%-%%%-%%%-%%%%%-%%%-%-%-%%%%%-%-%%%%%
%-------%---%-----%-%-----%---%-%---%
%%%-%-%%%%%-%%%%%-%%%-%%%-%-%%%-%-%%%
%-%-%-%-%-%-%-%-----%-%---%-%---%-%-%
%-%-%%%-%-%-%-%-%%%%%%%%%-%-%-%-%-%-%
%---%---%---%-----------------%-----%
%-%-%-%-%%%-%%%-%%%%%%%-%%%-%%%-%%%-%
%.%-%-%-------%---%-------%---%-%--P%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
matriz = []
for n in mapa.split("\n"):
    l = []
    for m in n:
        l.append(m)
    matriz.append(l)
start = Node(inicio)
camino = []
lista.append(start)
"""
Inicia el ciclo:
visit: es una variable booleana usada para saber si un nodo fue visitado o no
q = al que tenga menor valor F en la lista

"""
while(len(lista)>0):
    visit = False
    q = min(lista)
    lista.remove(q)
    #si "q" es la solucion se construye el camino
    if(q.getPos() == final):
        k = q
        camino.insert(0,str(k.getPos()[0])+" "+str(k.getPos()[1]))
        while(k != None):
            k = k.padre
            if(k != None):
                camino.insert(0,str(k.getPos()[0])+" "+str(k.getPos()[1]))
        break
    else:
        for n in visitados:
            if(n.getPos() == q.getPos()):
                visit = True
        if(visit == False):
            #si el nodo no ha sido visitado entonces se generan hijos y se inserta en visitados y se actualizan sus distancias
            visitados.append(q)
            hijos = generaHijos(q,matriz)
            for n in hijos:
                n.g = q.g + distancia(n,inicio)
                n.h = distancia(n,final)
                n.f = n.g + n.h
                lista.append(n)
print(len(camino)-1)
for n in camino:
    print(n)
print("--------%s seconds -----"%(time.time() - start_time))
