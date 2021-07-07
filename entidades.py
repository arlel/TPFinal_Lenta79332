import random

valDemanda = [0, 10, 20, 30, 40, 50]
probDemanda = [0.05, 0.12, 0.18, 0.25, 0.22, 0.18]

valDemora = [1, 2, 3, 4]  # Dias
probDemora = [0.15, 0.20, 0.40, 0.25]


def buscarProbabilidad(nro, probabilidades):
    acum = 0
    pAC = []
    for p in probabilidades:
        acum += p
        pAC.append(acum)
    for i in range(0, len(pAC)):
        if nro < pAC[i]:
            return i


class Politica:
    nombre = "Politica"
    decenasPedidas = [-1, 100, 200]  # comparo mayor que valDecenas[i]
    costoDecenasPed = [200, 280, 300]
    reaprobicionar = 0  # Cantidad de decenas a reaprovisionar
    dias = 0  # Dias entre cada pedido de reposicion
    acumularDemandaDeLosUltimosDias = 0 # Cantidad de dias que acumulo

    def __init__(self, reap, days, nombre):
        self.reaprobicionar = reap
        self.dias = days
        self.nombre = nombre
        self.acumularDemandaDeLosUltimosDias = 0

    def setAcumularDias(self, diasAAcumular):
        # Con esta variable, le decimos al programa que debe acumular
        # la demanda, cuando la cantidad de dias para el proximo pedido
        # dias para reaprobicionar < 10
        self.acumularDemandaDeLosUltimosDias = diasAAcumular

    # Obtiene el costo de restock para la cantidad de decenas
    def calcularCostoPedido(self, acumulado):
        if self.reaprobicionar == 0:
            temp = acumulado
        else:
            temp = self.reaprobicionar
        for i in range(len(self.decenasPedidas)-1, -1, -1):
            if temp > self.decenasPedidas[i]:
                return self.costoDecenasPed[i]

    def deboAcumularDemanda(self, diaActual):
        # diaActual% self.dias me dice cuantos dias faltan para el pedido de restock
        if self.acumularDemandaDeLosUltimosDias != 0:
            if diaActual == 1:
                return True
            if (diaActual % self.dias) == 0 or (diaActual % self.dias) == 1:
                # Si es el decimo ida o el noveno
                return True
            if diaActual % self.dias >= self.dias - self.acumularDemandaDeLosUltimosDias+2:
                return True
        return False

    def getNombre(self):
        return self.nombre

    def getReaprobicionamiento(self):
        return self.reaprobicionar


class Fila:
    politica = Politica(0, 0, "null")
    dia = 0
    rndDemanda = 0
    demanda = 0
    stock = 0
    diaPedidoReposicion = 0
    rndDemora = 0
    demora = 0
    diaRestock = 0
    acumuladoDemanda = 0  # esta fila se emplea en la politica B.
    costoAlmacenamiento = 0
    costoFaltante = 0
    costoAdquisicion = 0
    costoTotalDia = 0
    # Constantes:
    costoDAlmacenamiento = 50  # cuesta 50 por cada decena de producto
    costoDFaltante = 80  # 8 por unidad = 80 por decena

    # Variables Estadisticas:
    acumuladorCosto = 0
    # Con esta variable estadistica obtendre cual es la mejor politica.
    promedioCostoPorDia = 0

    # init para el dia 0
    def __init__(self, stockInicial, politica):
        self.politica = politica
        self.stock = stockInicial
        self.diaPedidoReposicion = 1

    def mostrarFila(self):
        return [self.dia, round(self.rndDemanda, 4), self.demanda, self.stock,
                self.diaPedidoReposicion, round(self.rndDemora, 4), self.demora,
                self.diaRestock, self.acumuladoDemanda, self.costoAlmacenamiento,
                self.costoFaltante, self.costoAdquisicion, self.costoTotalDia,
                self.acumuladorCosto, round(self.promedioCostoPorDia, 4)]

    def calcularProximaFila(self):

        self.dia += 1
        # reinicio ciertos campos de la fila
        self.costoAdquisicion = 0
        self.costoFaltante = 0
        self.costoAlmacenamiento = 0
        self.rndDemora = 0
        self.demora = 0
        self.calcularDemanda()
        self.calcularStock()
        self.evaluarPedidoReposicion()
        self.sumarCostos()
        self.estadisticas()
        return self

    def calcularDemanda(self):
        self.rndDemanda = random.random()
        self.demanda = valDemanda[buscarProbabilidad(self.rndDemanda, probDemanda)]
        if self.politica.deboAcumularDemanda(self.dia):
            self.acumuladoDemanda += self.demanda

    def calcularStock(self):
        # Si es el dia de restock reaprobiciono
        if self.diaRestock == self.dia:
            if self.politica.acumularDemandaDeLosUltimosDias == 0:
                self.stock += self.politica.getReaprobicionamiento()
            else:
                # Si tuve que ir acumulando dias para saber cuanto reaprobicionar
                self.stock += self.acumuladoDemanda
                self.acumuladoDemanda = 0
        # Siempre me fijare en la demanda asi que procedo a restar el valor de la demanda del dia
        self.stock -= self.demanda
        if self.stock < 0:
            # Si el stock es negativo calculo costo por faltante
            self.costoFaltante = -self.stock * self.costoDFaltante
            self.stock = 0
        elif self.stock > 0:
            self.costoAlmacenamiento = self.stock * self.costoDAlmacenamiento

    def evaluarPedidoReposicion(self):
        # Si es el dia de pedido de reposicion hago el pedido
        if self.diaPedidoReposicion == self.dia:
            self.diaPedidoReposicion += self.politica.dias
            self.hacerPedidoReposicion()
        elif self.diaRestock < self.dia:
            self.diaRestock = 0

    def hacerPedidoReposicion(self):
        self.rndDemora = random.random()
        self.demora = valDemora[buscarProbabilidad(self.rndDemora, probDemora, )]
        self.costoAdquisicion = self.politica.calcularCostoPedido(self.acumuladoDemanda)
        self.diaRestock = self.dia + self.demora

    def sumarCostos(self):
        self.costoTotalDia = self.costoAdquisicion + self.costoFaltante + self.costoAlmacenamiento

    def estadisticas(self):
        self.acumuladorCosto += self.costoTotalDia
        self.promedioCostoPorDia = self.acumuladorCosto / self.dia

    def getPolitica(self):
        return self.politica

    def getPromedioCostoPorDia(self):
        return self.promedioCostoPorDia

    def getDia(self):
        return self.dia

