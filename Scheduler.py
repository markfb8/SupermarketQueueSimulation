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
        self.server1 = Server()
        self.server2 = Server()
        self.queue = Queue()

        # Establim connexions
        self.source.crearConnexio(self.server1)
        self.server.crearConnexio(self.server2, self.queue)

        # Iniciem simulació
        simstart = Event('SIMULATION_START', 0, None)
        self.eventList.append(simstart)

    def run(self):
        # Rellotge de simulacio a 0
        self.currentTime = 0
        # Bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            # Recuperem event simulacio
            event = self.eventList.donamEsdeveniment
            # Actualitzem el rellotge de simulacio
            self.currentTime = event.time
            # Deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # També podríem delegar l'acció a un altre objecte
            event.objecte.tractarEsdeveniment(event)

        # Recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # Inserir esdeveniment de forma ordenada
        self.eventList.inserirEvent(event)

    def tractarEsdeveniment(self, event):
        if event.tipus == "SIMULATION_START":
            # comunicar a tots els objectes que cal preparar-se
            self.source.tractarEsdeveniment(event)
            self.server1.tractarEsdeveniment(event)
            self.server2.tractarEsdeveniment(event)

    def recollirEstadistics(self):
        print("")
        print("ESTADÍSTICS")
        print("Nombre d'entitats creades: " + str(self.source.entitatscreades))
        print("Nombre d'entitats perdudes: " + str(self.source.entitatsperdudes))
        print("Nombre d'entitats processades per caixa 1: " + str(self.server1.entitatstractades))
        print("Nombre d'entitats processades per caixa 2: " + str(self.server2.entitatstractades))
        print("")


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
