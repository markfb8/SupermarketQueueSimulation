from queue import Queue

from Server import *
from Source import *
from event import *;


class Scheduler:

    currentTime = 0
    eventList = []
    ...
    
    def __init__(self, numarribades, prob0, prob1, prob2):
        # creació dels objectes que composen el meu model
        self.source = Source(self,numarribades, prob0, prob1, prob2)
        self.server1 = Server()
        self.server2 = Server()
        self.server3 = Server()
        self.server4 = Server()
        self.queue = Queue()

        self.source.crearConnexio(server)
        self.server.crearConnexio(server2, queue)
        
        self.simulationStart=Event(self,'SIMULATION_START', 0,null))
        self.eventList.append(simulationStart)

    def run(self):
        #configurar el model per consola, arxiu de text...
        self.configurarModel()

        #rellotge de simulacio a 0
        self.currentTime=0        
        #bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            #recuperem event simulacio
            event=self.eventList.donamEsdeveniment
            #actualitzem el rellotge de simulacio
            self.currentTime=event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.objecte.tractarEsdeveniment(event)
        
        #recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self,event):
        #inserir esdeveniment de forma ordenada
        self.eventList.inserirEvent(event)

    def tractarEsdeveniment(self,event):
        if (event.tipus=="SIMULATION_START"):
            # comunicar a tots els objectes que cal preparar-se            
            

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
