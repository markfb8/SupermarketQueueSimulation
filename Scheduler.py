from queue import Queue
from Server import *
from Source import *
from Event import Event


class Scheduler:
    currentTime = 0
    eventList = []

    def __init__(self):
        # Recollim paràmetres de configuració
        # Nombre d'arribades
        print("")
        print("Volume of arrivals (1, 2 o 3):")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        numarribades = int(input())
        # Tipus de clients
        print("")
        print("Specify the probability of <no doubts> customers with an integer from 1 to 100:")
        probcapdubte = int(input())
        print("Specify the probability of <lots of doubts> customers with an integer from 1 to 100:")
        probmoltsdubtes = int(input())
        probpocsdubtes = 100 - (probmoltsdubtes + probcapdubte)
        # Temps de simulació
        print("Simulation time in minutes:")
        self.simulationtime = int(input())

        # Imprimim els paràmetres escollits
        print("")
        print("SELECTED PARAMETERS:")
        print("Volume of arrivals: Level" + str(numarribades))
        print("<No doubts>  customers: " + str(probcapdubte) + "%")
        print("<Some doubts> customers: " + str(probpocsdubtes) + "%")
        print("<Lots of doubts> customers: " + str(probmoltsdubtes) + "%")
        print("Simulation time: " + str(self.simulationtime) + " minutes")

        # Creació dels objectes que composen el meu model
        self.source = Source(self, numarribades, probcapdubte, probpocsdubtes, probmoltsdubtes)
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
        while self.eventList and self.currentTime <= self.simulationtime:
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
                if event.tipus == 'NEW_SERVICE':
                    if not self.queue.empty():
                        event.entitat.recullEntitat(event.time, self.queue.get())
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
        self.eventList.sort(key=lambda x: x.time, reverse=False)

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
        print("STATISTICS")
        print("Total number of customers: " + str(self.source.entitatscreades))
        if self.clientsperduts == 0:
            print("No lost customers! :)")
        else:
            print("Lost customers: " + str(self.clientsperduts) + " :(")

        print("Customers who payed at checkout 1: " + str(self.server1.entitatstractades))
        print("Customers who payed at checkout 2: " + str(self.server2.entitatstractades))
        print("Customers who payed at checkout 3: " + str(self.server3.entitatstractades))
        print("Customers who payed at checkout 4: " + str(self.server4.entitatstractades))
        avg1 = (self.server1.timeprocessing / self.server1.entitatstractades)
        avg2 = (self.server2.timeprocessing / self.server2.entitatstractades)
        avg3 = (self.server3.timeprocessing / self.server3.entitatstractades)
        avg4 = (self.server4.timeprocessing / self.server4.entitatstractades)
        print("Average process time of supermarket checkouts: " + str((avg1 + avg2 + avg3 + avg4) / 4))
        print("")


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()

