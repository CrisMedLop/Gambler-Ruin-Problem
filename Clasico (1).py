# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import random as rnd

# El primer límite es para la rutina de simulación que muestra trayectorias y
# por lo tanto se hace uso de listas dinámicas, el segundo es para una simulación
# que no está sujeta al límite de recursividad (3000), por eso es más grande.

Lim_iteraciones1= 2900
Lim_iteraciones2 = 100000

# Para la lista dinámica se define la clase nodo y el método insertar el cuál es
# recursivo. 

class nodo():
    def __init__ (self,dato):
        self.sig = None
        self.dato = dato
def inserta (inicio, nodo):
    if (inicio.sig == None):
        inicio.sig = nodo
    else:
        p = inicio.sig
        inserta(p,nodo)
        
# La primera función simulación es para presentar las trayetorias que describen el
# comportamiento de la caminata aleatoria, se ingresan los parámetros que definen
# a dicha caminata y se regresa un arreglo con el desarrollo que tuvo el juego.         

def simulacion (p, capI, capT):
    flag = True
    capO = capI
    path = nodo(capO)
    numI = 0
    while (flag == True):
        r = rnd.random()
        if (r <= p):
            capI = capI + 1
        else:
            capI = capI - 1
        inserta(path, nodo(capI))
        numI = numI + 1
        if (capI == 0   or  numI == Lim_iteraciones1 or capI == capT):
            flag = False
            
    tryc = [0]*(numI+1)
    n = path
    for i in range (numI+1):
        tryc[i] = n.dato
        n = n.sig
    
    return(tryc)

# En la segunda función de simulación solo se requiere conocer cuantas rondas
# fueron necesarias para terminar el juego, por lo que se ingresan los tres 
# parámetros que definen la caminata, pero se regresa únicamente un arreglo de
# longitud dos con la información mencionada.

def simulacion2 (p, capI, capT):
    flag = True
    numI = 0
    while (flag == True):
        r = rnd.random()
        if (r <= p):
            capI = capI + 1
        else:
            capI = capI - 1
#        inserta(path, nodo(capI))
        numI = numI + 1
        if (capI == 0   or  numI == Lim_iteraciones2 or capI == capT):
            flag = False
            
    tryc = [0]*2
    tryc[0] = numI
    tryc[1] = capI
    
    return(tryc)    

# Para el problema clásico se deducen expresiones con las que se calcula la 
# probabilidad de ruina y la duración esperada, se declaran para poder apreciar
# el valor numérico que devuelven con respecto al obtenido de las simulaciones 
# para cada ejecución.

def p_ruina(p, capI, capT):
    if p == 0.5:
        result = 1 - (capI)/(capT)
    else:
        result = 1 - ((1 - ((1-p)/p)**capI)/(1 - ((1-p)/p)**capT))
    return result

def duracion(p, capI, capT):
    if p == 0.5:
        result = capI*(capT-capI)
    else:
        result = (1/(1-2*p))*(capI - capT * ((1 - ((1-p)/p)**capI)/(1 - ((1-p)/p)**capT)))
    return result

# Siguen los parámetros que el usuario debe ingresar
print("-----------------------------------------------------------")
print("-------------Problema de la Ruina del Jugador -------------")
print("---------------- B I E N V E N I D O  ---------------------")
p = float(input("Probabilidad de ganar en cada ronda (p) = "))
capI = int(input("Capital inicial (capI) = "))
capT = int(input("Capital total (capT) = "))
numT = int(input("Número de trayectorias a mostrar = "))


# El ciclo que sigue manda a llamar a la función simular de acuerdo al número 
# de trayectorias que el usuario específico, después siguen las instrucciones
# para imprimirlas en un gráfico.

for i in range (numT):
    trayectoria = simulacion(p, capI, capT)
    numRondas = len(trayectoria) - 1
    print("S",i+1,": Después de ",numRondas,"partidas")
    if (trayectoria[numRondas]==0):
        print("     ¡El jugador quedó arruinado!","\U0001F635","\U0001F641")
    else:
        print("     ¡El jugador ganó todo!","\U0001F603","\U0001F601")
    
    plt.plot(trayectoria, zorder=1)

plt.grid()
plt.title("Ruina del jugador")
plt.xlabel("Partida")
plt.ylabel("Capital")
plt . scatter (0, capI , c='black', edgecolors ='none', s=100 , label = 'Cap. Inicial= {0:10.1f}'.format(capI), zorder=2)  
plt . legend ( bbox_to_anchor =(1.04 , 0.98) , loc='upper left', borderaxespad=0.)
plt.show()

# Después están las simulaciones secundarias que no se presentan al usuario
# estás son únicamente para hacer los promedios que aproximen la probabilidad 
# de ruina y la duración del juego.

numSim = 500
jperdido = 0
jnperdido = 0
promD = 0
for i in range (numSim):
    trayectoria = simulacion2(p, capI, capT)
    numJ = trayectoria[0]
    if(trayectoria[1]==0):
        jperdido = jperdido + 1
    else:
        jnperdido = jnperdido + 1
    
    promD = promD + numJ
    
promD = promD/numSim
promR = jperdido/numSim
promNR = jnperdido/numSim
Ruina = ((1-p)/(p))**capI

# Finalmente se presentan los resultados de estos cálculos.

print("                     R E S U L T A D O S")
print("///////////////////////////////////////////////////////////////")
print("Luego de ", numSim, " simulaciones, con los parámetros:")
print("     Probabilidad de perder en cada ronda= ",p)
print("     Capital inicial= ",capI)
print("     Capital total= ",capT)
print("se obtuvo lo siguiente:")
print("     Juegos perdidos= ", jperdido)
print("     Juegos ganados= ", jnperdido)
print("     Promedio de duración= ", promD, "|| Duración esperada= {0:10.3f}".format(duracion(p, capI, capT)))
print("     Probabilidad de ruina (proporción)= ", promR, "|| Probabilidad de ruina= {0:10.3f}".format(p_ruina(p, capI, capT)) )