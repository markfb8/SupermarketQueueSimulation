# millor treballar amb define o algun sistema simular a l'enum de C++
# from enumeracions import *
from Event import Event
from random import randint


class Server:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatstractades = 0
        self.state = "idle"
        self.scheduler = scheduler
        self.entitatActiva = None
        self.queue = None
        self.server = None
        
    def crearConnexio(self, server, queue):
        self.queue = queue
        self.server = server
    
    def recullEntitat(self, time, entitat):
        self.entitatActiva = entitat
        self.programarFinalServei(time)

    def tractarEsdeveniment(self, event):
        if event.tipus == 'SIMULATION START':
            self.simulationStart(event)
        elif event.tipus == 'END_SERVICE':
            self.processarFiServei(event)

    def simulationStart(self):
        self.state = "idle"
        self.entitatstractades = 0

    def programarFinalServei(self, time):
        # que triguem a fer un servei (aleatorietat)
        tempsservei = self.calcularTemps()
        # incrementem estadistics si s'escau
        self.entitatstractades = self.entitatstractades+1
        self.state = "busy"
        # programació final servei
        return Event('END_SERVICE', time + tempsservei, self.entitatActiva)

    def processarFiServei(self, event):
        # Registrar estadístics
        self.entitatstractades = self.entitatstractades+1
        # Mirar si es pot transferir a on per toqui
        if self.server.state == "idle":
            # transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
            self.server.recullEntitat(event.time, event.entitat)
        else:
            if self.queue.estat == "idle":
                self.queue.recullEntitat(event.time, event.entitat)
        self.state = "idle"
    
    def calcularTemps(self):
        # calculem temps entre arribades segons el nivell d'arribades de forma aleatòria
        return randint(2, 5) * self.entitatActiva.doubts
