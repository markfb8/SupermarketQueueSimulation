from Event import Event
from random import randint


class Server:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatstractades = 0
        self.state = "idle"
        self.scheduler = scheduler
        self.entitatActiva = None
    
    def recullEntitat(self, time, entitat):
        self.entitatActiva = entitat
        self.programarFinalServei(time)

    def tractarEsdeveniment(self, event):
        if event.tipus == 'SIMULATION START':
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
        self.entitatstractades = self.entitatstractades+1
        self.state = "busy"
        # programació final servei
        return Event('END_SERVICE', time + tempsservei, self)

    def processarFiServei(self, time):
        # Registrar estadístics
        self.entitatActiva = None
        self.entitatstractades = self.entitatstractades+1
        # Si hi ha algú esperant a la cua passem a processar-lo sinó passem a estar disponibles
        if not self.scheduler.queue.empty():
            self.recullEntitat(time, self.scheduler.queue.get())
        else:
            self.state = "idle"
    
    def calcularTemps(self):
        # calculem temps entre arribades segons el nivell d'arribades de forma aleatòria
        return randint(2, 5) * self.entitatActiva.doubts
