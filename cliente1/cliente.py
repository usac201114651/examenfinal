import threading 
import logging
import time
import os 
import sys

from mqtt import Mqtt
from audio import Sonido
from comandos import Comandos
from datetime import datetime

cli = Mqtt("proyectos", "proyectos980", "167.71.243.238", 1883)
com = Comandos()
aud = Sonido()

def alive(delay = com.delay_a()):
    while True:
        alive  = com.command_alive()  +  bytes(str(cli.carnet()), 'utf-8')
        cli.client.publish(str(cli.topicalive()), alive)
        time.sleep(delay)          

t1 = threading.Thread(name = 'alive',
                        target = alive,
                        daemon = True
                        )

listaHilos = []
#Luego de configurar cada hilo, se inicializan
t1.start()
for i in listaHilos:
    i.start()
#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
try:
    while True: 
        #os.system('clear') 
        print ('Menú principal')
        print ('\t1 - Enviar texto')
        print ('\t2 - Enviar mensaje de voz')
        print ('\t3 - Salir')
        opcionMenu = input('\n\tDigite opcion -> ')                                         
        if opcionMenu == '1':
          #os.system('clear') 
          print ('Seleccione tipo')
          print ('\t1 - Enviar a usuario')
          print ('\t2 - Enviar a sala')  
          opcionMenu = input('\n\tDigite tipo -> ')
          if opcionMenu == '1':     
           #os.system('clear')
           destino = input ('Escribe el destino ->')
           a_enviar = input ('Escribe mensaje ->')
           a_enviar = cli.carnet() + ' dice: ' + a_enviar
           cli.client.publish(("usuarios/16"+"/"+destino), a_enviar, 2)
           print('...enviado') 
          elif opcionMenu == '2':
           #os.system('clear')
           destino = input ('Escribe el destino ->')
           a_enviar = input ('Escribe mensaje ->')
           a_enviar = cli.carnet() + ' dice: ' + a_enviar
           cli.client.publish(("salas/16/"+"/"+destino), a_enviar, 2)
           print('...enviado')    
        elif opcionMenu == '2':
            #os.system('clear') 
            print ('Seleccione tipo')
            print ('\t1 - Enviar a usuario')
            print ('\t2 - Enviar a sala')  
            opcionMenu = input('\n\tDigite tipo -> ') 
            if opcionMenu == '1':
             now = datetime.now()
             file_audio = "prueba.wav" #str(datetime.timestamp(now))+".wav"   
             #os.system('clear')
             destino = str(input ('Escribe el destino ->'))
             audio_t = int(input("indique el tiempo de grabación >> "))
             aud.record(audio_t, file_audio)
             aud.play(file_audio)
             file_size = (os.stat(file_audio).st_size)
             ftr = com.command_ftr() + bytes(str(destino), 'utf-8') + bytes(str(file_size), 'utf-8')
             cli.client.publish(cli.topic_esp(), ftr)
             time.sleep(1)
             for x in range(3):
              time.sleep(0.2)    
              if(bool(cli.tcp_a())==True):  
               for x in range(2):
                time.sleep(0.2)    
                if(bool(cli.tcp_a())==True):  
                   print("enviar_audio")
                   cli.enviar(file_audio)
                   cli.enviar(file_audio)
             
        elif opcionMenu == '3':   
            exit()  

except KeyboardInterrupt:
    print('Desconectando del broker MQTT...')
    cli.client.disconnect()
    if t1.isAlive():
        t1._stop()

finally:
     print('Se ha desconectado del broker. Saliendo...')