#MTEZ Este es el servidor, que gestiona los comandos, usuarios vivos, y transferencia de TCP
import threading 
import time
import sys

from mqtt import Servidor
from comandos import Comandos

#MTEZ SE crea la instancia de la clase Servidor con atributos para conexion mqtt
Ser = Servidor("proyectos", "proyectos980", "167.71.243.238", 1883)
com = Comandos()

#MTEZ metodo para correr ordenar y recibir de los topics
def run(delay = 1):
    while True:
        Ser.run_topics()       
       #MTEZ inicio atraves de hilo, muere cuando muere el proceso, se va al fondo por ser demonio
t1 = threading.Thread(name = 'run',
                        target = run,
                        daemon = True
                        )


#MTEZ Luego de configurar cada hilo, se inicializan
t1.start()                             

#MTEZ Se inicia el servidor
try:
    print('Servidor activo')  
    while True:
     Ser.client.loop_start()

#MTEZ desconexión
except KeyboardInterrupt:
 print('Desconectando del broker MQTT...')
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     

finally:
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     
     