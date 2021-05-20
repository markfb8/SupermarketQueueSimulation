import Scheduler

if __name__ == '__main__':

    # Recollim uns paràmetres inicials

    # Nombre d'arribades
    print("")
    print("Especifica nivell d'arribades (1, 2 o 3):")
    print("1. Baixa")
    print("2. Intermitja")
    print("3. Alta")
    numarribades = int(input())

    # Tipus de clients
    print("")
    print("Especifica probabilitat de clients de tipus ""cap dubte"":")
    probcapdubte = int(input())
    print("Especifica probabilitat de clients de tipus ""molts dubtes"":")
    probmoltsdubtes = int(input())
    probpocsdubtes = 100 - (probmoltsdubtes + probcapdubte)

    # Imprimim els paràmetres escollits
    print("")
    print("PARÀMETRES SELECCIONATS:")
    print("Nivell d'arribades: " + str(numarribades))
    print("Clients de tipus ""cap dubte"": " + str(probcapdubte))
    print("Clients de tipus ""pocs dubtes"": " + str(probpocsdubtes))
    print("Clients de tipus ""molts dubtes"": " + str(probmoltsdubtes))

    #Iniciem el simulador
    Scheduler(numarribades, probcapdubte, probpocsdubtes, probmoltsdubtes)

