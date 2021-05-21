from queue import Queue
from Server import *
from Source import *
from Event import Event;


class Scheduler:
    currentTime = 0
    eventList = []

    def __init__(self, numarribades, prob0, prob1, prob2):
        # Creació dels objectes que composen el meu model
        self.source = Source(self, numarribades, prob0, prob1, prob2)
        self.server1 = Server(self)
        self.server2 = Server(self)
        self.server3 = Server(self)
        self.server4 = Server(self)
        self.source.creaConnexions(self.server1, self.server2, self.server3, self.server4)
        self.queue = Queue()

        # Estadístic
        self.clientsperduts = 0

        # Iniciem simulació
        simstart = Event('SIMULATION_START', 0, None)
        self.eventList.append(simstart)

    def run(self):
        # Rellotge de simulacio a 0
        self.currentTime = 0
        # Bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            # Recuperem event simulacio i el treiem de la llista
            event = self.eventList[0]
            self.eventList.pop(0)
            # Actualitzem el rellotge de simulacio
            self.currentTime = event.time
            # Deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # També podríem delegar l'acció a un altre objecte
            if event.entitat is None:
                if event.tipus == "SIMULATION_START":
                    # comunicar a tots els objectes que cal preparar-se
                    self.source.tractarEsdeveniment(event)
                    self.server1.tractarEsdeveniment(event)
                    self.server2.tractarEsdeveniment(event)
                    self.server3.tractarEsdeveniment(event)
                    self.server4.tractarEsdeveniment(event)
            else:
                event.entitat.tractarEsdeveniment(event)
                if event.tipus == "END_SERVICE":
                    self.comprovaCua()

        # Recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # Inserir esdeveniment de forma ordenada
        self.eventList.append(event)
        # Ordenar eventlist per temps
        self.eventList.sort(key=lambda x: x.time, reverse=True)

    def tractarEsdeveniment(self, event):
        if event.tipus == "SIMULATION_START":
            # comunicar a tots els objectes que cal preparar-se
            self.source.tractarEsdeveniment(event)
            self.server1.tractarEsdeveniment(event)
            self.server2.tractarEsdeveniment(event)
            self.server3.tractarEsdeveniment(event)
            self.server4.tractarEsdeveniment(event)

    def comprovaCua(self):
        auxqueue = Queue()
        while not self.queue.empty():
            entitat = self.queue.get()
            if (entitat.created_at + self.currentTime) > 15:
                self.clientsperduts = self.clientsperduts + 1
            else:
                auxqueue.put(entitat)

        while not auxqueue.empty():
            self.queue.put(auxqueue.get())

    def recollirEstadistics(self):
        print("")
        print("ESTADÍSTICS")
        print("Nombre d'entitats creades: " + str(self.source.entitatscreades))
        print("Nombre d'entitats processades per caixa 1: " + str(self.server1.entitatstractades))
        print("Nombre d'entitats processades per caixa 2: " + str(self.server2.entitatstractades))
        print("Nombre d'entitats processades per caixa 3: " + str(self.server3.entitatstractades))
        print("Nombre d'entitats processades per caixa 4: " + str(self.server4.entitatstractades))
        print("")
