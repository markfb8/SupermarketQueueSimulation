from Event import Event
from random import randint


class Server:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatstractades = 0
        self.state = "idle"
        self.scheduler = scheduler
        self.entitatActiva = None
        self.timeprocessing = 0
    
    def recullEntitat(self, time, entitat):
        self.entitatActiva = entitat
        self.programarFinalServei(time)

    def tractarEsdeveniment(self, event):
        if event.tipus == 'SIMULATION_START':
            self.simulationStart()
        elif event.tipus == 'END_SERVICE':
            self.processarFiServei(event.time)

    def simulationStart(self):
        self.state = "idle"
        self.entitatstractades = 0

    def programarFinalServei(self, time):
        # que triguem a fer un servei (aleatorietat)
        tempsservei = self.calcularTemps()
        # incrementem estadistics si s'escau
        self.timeprocessing = self.timeprocessing + 1
        self.entitatstractades = self.entitatstractades+1
        self.state = "busy"
        # programació final servei
        self.scheduler.afegirEsdeveniment(Event('END_SERVICE', time + tempsservei, self))

    def processarFiServei(self, time):
        # Registrar estadístics
        self.entitatActiva = None
        self.entitatstractades = self.entitatstractades+1
        self.state = 'idle'
        # Cal avisar que podem tractar la següent entitat
        self.scheduler.afegirEsdeveniment(Event('NEW_SERVICE', time, self))
    
    def calcularTemps(self):
        # calculem temps entre arribades segons el nivell d'arribades de forma aleatòria
        if self.entitatActiva.doubts == 0:
            return randint(1, 3)
        else:
            return randint(1, 5) * self.entitatActiva.doubts
