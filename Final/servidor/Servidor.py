import threading 
import time
import sys

from mqtt import Servidor
from comandos import Comandos

Ser = Servidor("proyectos", "proyectos980", "167.71.243.238", 1883)
com = Comandos()

def run(delay = 1):
    while True:
        Ser.run_topics()       
       
t1 = threading.Thread(name = 'run',
                        target = run,
                        daemon = True
                        )


#Luego de configurar cada hilo, se inicializan
t1.start()                             


try:
    print('Servidor activo')  
    while True:
     Ser.client.loop_start()

except KeyboardInterrupt:
 print('Desconectando del broker MQTT...')
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     

finally:
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     
     