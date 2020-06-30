#MTEZ importamos las librerías necesarias

import threading 
import time
import sys
from mqtt import Servidor
from comandos import Comandos

#MTEZ creamos un objeto nuevo de la clase Servidor, con atributos Credednciales de Mqtt
Ser = Servidor("proyectos", "proyectos980", "167.71.243.238", 1883)
#MTEZ objeto tipo Comandos
com = Comandos()

#MTEZ función para los hilos de ejecución
def run(delay = 1):
    while True:
        Ser.run_topics()       
       
t1 = threading.Thread(name = 'run',
                        target = run,
                        daemon = True
                        )

listaHilos = []
#MTEZ Luego de configurar cada hilo, se inicializan
t1.start()                             

#MTEZ main, bucle principal al iniciarse el servidor
try:
    print('Servidor')  
    while True:   
     if(Ser.temp() == True):   #MTEZ compara el resultado del método temp, de la clase Servidor, si es verdadero, se mantiene 
        Ser.recibir()   #MTEZ funcion de recepción
     Ser.client.loop_start() #MTEZ funcion bloqueante

except KeyboardInterrupt: #MTEZ excepción para salir  
 print('Desconectando del broker MQTT...')
 Ser.client.loop_stop()                      #MTEZ cerrando conexión  
 Ser.client.disconnect()                     #MTEZ desconectando 

finally:
 Ser.client.loop_stop()   #MTEZ Cerrando conexión         
 Ser.client.disconnect()  #MTEZ desconectando 
     