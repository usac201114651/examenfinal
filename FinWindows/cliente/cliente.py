import threading 
import logging
import time
import os 
import sys

from mqtt import Mqtt
from audio import Sonido
from comandos import Comandos

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
        #os.system('cls') 
        print ('Menú principal')
        print ('\t1 - Enviar texto')
        print ('\t2 - Enviar mensaje de voz')
        print ('\t3 - Salir')
        opcionMenu = input('\n\tDigite opcion -> ')                                         
        if opcionMenu == '1':
          os.system('cls') 
          print ('Seleccione tipo')
          print ('\t1 - Enviar a usuario')
          print ('\t2 - Enviar a sala')  
          opcionMenu = input('\n\tDigite tipo -> ')
          if opcionMenu == '1':     
           os.system('cls')
           destino = input ('Escribe el destino ->')
           a_enviar = input ('Escribe mensaje ->')
           a_enviar = cli.carnet() + ' dice: ' + a_enviar
           cli.client.publish(("usuarios"+"/"+destino), a_enviar)
           print('...enviado') 
          elif opcionMenu == '2':
           os.system('cls')
           destino = input ('Escribe el destino ->')
           a_enviar = input ('Escribe mensaje ->')
           a_enviar = cli.carnet() + ' dice: ' + a_enviar
           cli.client.publish(("usuarios"+"/"+destino), a_enviar)
           print('...enviado')    
        elif opcionMenu == '2':
            os.system('cls') 
            print ('Seleccione tipo')
            print ('\t1 - Enviar a usuario')
            print ('\t2 - Enviar a sala')  
            opcionMenu = input('\n\tDigite tipo -> ') 
            if opcionMenu == '1':
             file_audio = "enviar.wav" 
             os.system('cls')
             destino = str(input ('Escribe el destino ->'))
             audio_t = int(input("indique el tiempo de grabación >> "))
             aud.record(audio_t, file_audio)
             aud.play(file_audio)
             file_size = (os.stat(file_audio).st_size)
             ftr = com.command_ftr() + bytes(str(destino), 'utf-8') + bytes(str(file_size), 'utf-8')
             cli.client.publish(cli.topic_esp(), ftr)
        elif opcionMenu == '3':   
            exit()  

except KeyboardInterrupt:
    print('Desconectando del broker MQTT...')
    cli.client.disconnect()
    if t1.isAlive():
        t1._stop()

finally:
     print('Se ha desconectado del broker. Saliendo...')