#millor treballar amb define o algun sistema simular a l'enum de C++
from enumeracions import *
from Server import *

class Source:

    def __init__(self, scheduler, numarribades, prob0, prob1, prob2):
        # inicialitzar element de simulació
        # guardar probabilitats de configuarció
        self.numarribades = numarribades
        self.probcapdubte = prob0
        self.probpocsdubtes = prob1
        self.probmoltsdubtes = prob2

        self.entitatscreades = 0
        self.state = "idle"
        self.scheduler = scheduler
        self.server = None

    def crearConnexio(self, server):
        self.server = server

    def tractarEsdeveniment(self, event):
        if event.type == 'SIMULATION START':
            self.simulationStart()
        if event.type == 'NEXT ARRIVAL':
            self.processNextArrival()

    def simulationStart(self):
        nouevent = self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouevent)

    def processNextArrival(self, event):
        # Cal crear l'entitat 
        entitat = self.crearEntitat(self)
        # Mirar si es pot transferir a on pertoqui
        if self.server.estat == "idle":
            # transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
            self.server.recullEntitat(event.time, entitat)
        else:
            # incrementar entitats perdudes en creació (si s'escau necessari)

        # Cal programar la següent arribada
        nouevent = self.properaArribada(event.temps)
        self.scheduler.afegirEsdeveniment(nouevent)

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsentrearribades = self.calcularTemps()
        # incrementem estadistics si s'escau
        self.entitatscreades = self.entitatscreades+1
        self.state = "busy"
        # programació primera arribada
        return Event(self, 'NEXT ARRIVAL', time + tempsentrearribades, None)

    def calcularTemps(self):
        # calculem temps entre arribades segons el nivell d'arribades de forma aleatòria
        if self.numarribades == 1:
            return 40
        elif self.numarribades == 2:
            return 20
        elif self.numarribades == 3:
            return 5
