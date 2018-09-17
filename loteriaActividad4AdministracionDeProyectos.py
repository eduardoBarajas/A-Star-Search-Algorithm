import random
class Carta():
    def __init__(self,idCarta):
        self.id = idCarta
        self.numsUtilizados = []
        self.tablero = []
        for n in range(4):
            while(len(self.tablero)!=4):
                temp = []
                while(len(temp)!=4):
                    num = random.randint(0, 54)
                    if(num not in self.numsUtilizados):
                        self.numsUtilizados.append(num)
                        temp.append(num)
                self.tablero.append(temp)
    def imprimir(self):
        print("\n\nCarta #",self.id)
        return "\n".join("".join(str(num)) for num in self.tablero)
    def getCarta(self):
        return self.tablero
    def getNumCarta(self):
        return self.id
    def setCarta(self,tablero):
        self.tablero = tablero

class Loteria():
    def __init__(self,numCartas):
        self.cartas = []
        self.idCartaMayorPuntuacion = 0
        for n in range(numCartas):
            self.cartas.append(Carta(n))
    def imprimirTodasLasCartas(self):
        for n in self.cartas:
            print(n.imprimir())
    def getTodasLasCartas(self):
        return self.cartas
    def setCarta(self,id,carta):
        self.cartas[id] = carta
    def getMayorPuntuacion(self):
        puntuacion = 0
        for id,carta in enumerate(self.cartas,0):
            puntos = [y for x in carta.getCarta() for y in x if(y=="X")]
            if(len(puntos)>puntuacion): 
                puntuacion = len(puntos)
                self.idCartaMayorPuntuacion = id
        return puntuacion
    def getCartaGanadora(self):
        return self.cartas[self.idCartaMayorPuntuacion]
def comenzarLoteria(miLoteria):
    cartas_lanzadas = set()
    while(miLoteria.getMayorPuntuacion()!=16):
        carta_lanzada = random.randint(0, 54)
        if(carta_lanzada not in cartas_lanzadas):
            id = 0
            for carta in miLoteria.getTodasLasCartas():
                miLoteria.setCarta(id,buscarCartaLanzadaEnCarta(carta_lanzada,carta))
                id += 1
            miLoteria.imprimirTodasLasCartas()
    cartaGanadora = miLoteria.getCartaGanadora()
    print("Loteria!!!!\n\nGano la carta Numero : ",cartaGanadora.getNumCarta(),"\n")
    cartaGanadora.imprimir()
    exit()
                
def buscarCartaLanzadaEnCarta(cartaLanzada,carta):
    tablero = carta.getCarta()
    newTablero = []
    for n in tablero:
        if(cartaLanzada in n):
            newLista = []
            newLista += n[0:n.index(cartaLanzada)]
            newLista.append("X")
            newLista += n[n.index(cartaLanzada)+1:]
            newTablero.append(newLista)
        else:
            newTablero.append(n)
    carta.setCarta(newTablero)
    return carta
        
loteria = Loteria(4)
comenzarLoteria(loteria)
