#MTEZ Servidor para gestion de comandos para transferencia tcp, comentarios completos en version FinalWindows
#MTEZ Implemento 
import threading 
import time
import sys
#MTEZ importamos librerias propiaas
from mqtt import Servidor
from comandos import Comandos
#Se inicializa el objeto con los parametros de conexion Mqtt 
Ser = Servidor("proyectos", "proyectos980", "167.71.243.238", 1883)
com = Comandos()
#metodo para obtener, ordenar y administrar los mensajes de los topics 
def run(delay = 1):
    while True:
        Ser.run_topics()       
#se inicializa como hilo y se envia el proceso al fondo como demonio
t1 = threading.Thread(name = 'run',
                        target = run,
                        daemon = True
                        )


#Luego de configurar cada hilo, se inicializan
t1.start()                             

#se inicializa el ciclo para conexion
try:
    print('Servidor activo')  
    while True:
     Ser.client.loop_start()

#se desconecta por interrupción
except KeyboardInterrupt:
 print('Desconectando del broker MQTT...')
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     
#desconectamos 
finally:
 Ser.client.loop_stop()                        
 Ser.client.disconnect()                     
     
