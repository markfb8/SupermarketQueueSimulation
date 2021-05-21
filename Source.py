from Event import Event
from Client import Client
from random import randint


class Source:
    def __init__(self, scheduler, numarribades, prob0, prob1, prob2):
        # inicialitzar element de simulació
        # guardar probabilitats de configuarció
        self.numarribades = numarribades
        self.probcapdubte = prob0
        self.probpocsdubtes = prob1
        self.probmoltsdubtes = prob2

        self.entitatscreades = 0
        self.scheduler = scheduler

        self.server1 = None
        self.server2 = None
        self.server3 = None
        self.server4 = None

    def creaConnexions(self, server1, server2, server3, server4):
        self.server1 = server1
        self.server2 = server2
        self.server3 = server3
        self.server4 = server4

    def tractarEsdeveniment(self, event):
        if event.tipus == 'SIMULATION START':
            self.simulationStart()
        elif event.tipus == 'NEXT ARRIVAL':
            self.processNextArrival(event)

    def simulationStart(self):
        nouevent = self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouevent)

    def processNextArrival(self, event):
        # Cal crear l'entitat 
        entitat = self.crearEntitat(event.time)
        # Incrementem estadistics si s'escau
        self.entitatscreades = self.entitatscreades + 1
        # Ho passem a on pertoqui, sinó ho posem a la cua
        if self.scheduler.queue.empty():
            if self.server1.state == "idle":
                self.server1.recullEntitat(entitat)
            elif self.server2.state == "idle":
                self.server2.recullEntitat(entitat)
            elif self.server3.state == "idle":
                self.server3.recullEntitat(entitat)
            elif self.server4.state == "idle":
                self.server4.recullEntitat(entitat)
            else:
                self.scheduler.queue.put(entitat)
        else:
            self.scheduler.queue.put(entitat)

        # Cal programar la següent arribada
        nouevent = self.properaArribada(event.temps)
        self.scheduler.afegirEsdeveniment(nouevent)

    def properaArribada(self, time):
        # Cada quan generem una arribada (aleatorietat)
        tempsentrearribades = self.calcularTemps()
        # Programació primera arribada
        return Event('NEXT ARRIVAL', time + tempsentrearribades, self)

    def calcularTemps(self):
        # Calculem temps entre arribades segons el nivell d'arribades de forma aleatòria
        if self.numarribades == 1:
            return 40
        elif self.numarribades == 2:
            return 20
        elif self.numarribades == 3:
            return 5

    def crearEntitat(self, time):
        random = randint(1, 100)
        if random < self.probcapdubte:
            return Client(0, time)
        elif random < self.probpocsdubtes:
            return Client(3, time)
        else:
            return Client(7, time)
