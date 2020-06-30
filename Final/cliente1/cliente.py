#CATC------ importamos  las sigueintes  librerias 
import threading 
import logging
import time
import os 
import sys

#CATC importamos de otros  programas 
from mqtt import Mqtt
from audio import Sonido
from comandos import Comandos
from datetime import datetime
from  globals import *

#CATC imvocamos  ala clase  Mqtt  y  le  enviamos parametros
cli = Mqtt("proyectos", "proyectos980", "167.71.243.238", 1883,USER_ID_1,USER_ID_2,USER_ID_3)

#CATC igualamos una  funciones a  utilizar
com = Comandos()
aud = Sonido()

#CATC configuramos la  fucion Alive para  estar  avisando en elsevidor
#CATC que  nos  encontremaos activos
def alive(delay = com.delay_a()):
    while True:
        alive  = com.command_alive()  +  bytes(str(cli.carnet()), 'utf-8')
        cli.client.publish(str(cli.topicalive()), alive)
        time.sleep(delay)          

#CATC  ejecutamso  un hilo con la funcion Alive 
t1 = threading.Thread(name = 'alive',
                        target = alive,
                        daemon = True
                        )
#CATCLuego de configurar cada hilo, se inicializan
t1.start()

#CATC empieza  a correr  la interfas del usuario 
try:
    while True: 
       
        cli.mainMenu()    #CATC aparece el menu principarl                                       
        opcionMenu = input('\n\tDigite opción -> ')

        if opcionMenu == '1':
            cli.typeMenu() #CATC aparece el menu de topics para  enviar texto
            opcionMenu = input('\n\tDigite tipo -> ')    

            if opcionMenu == '1':
                cli.userMenu() #CATC aparece el menu principal de  mis  contactos
                opcionMenu = input('\n\tDigite Usuario -> ') 

                if opcionMenu == '1':
                    #CATC se  seleciona e primer  usuario 
                    print('va  enviar un mensaje a '+USER_ID_2+':')
                    cli.sendTextUser(1)  #CATC invoca  la funcion enviar texto al usuario
                elif opcionMenu == '2':
                    #CATC se  seleciona al segundo  usuario 
                    print('va  enviar un mensaje a '+USER_ID_3+':')
                    cli.sendTextUser(2) #CATC invoca  la funcion enviar texto al usuario
            elif opcionMenu == '2':
                cli.roomMenu() #CATC aparece  el menu de las  salas
                opcionMenu = input('\n\tDigite Sala -> ') 

                if opcionMenu == '0':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(0) #CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '1':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(1)#CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '2':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(2)#CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '3':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(3)  #CATC se  se invoca  a la  funcion enviar  texto a una sala

        elif opcionMenu == '2':
            cli.typeMenu() #CATC se muestra  el menu principal
            opcionMenu = input('\n\tDigite tipo -> ')  

            if opcionMenu == '1':
                cli.userMenu()#CATC se  se invoca al menu de usuarios 
                opcionMenu = input('\n\tDigite Usuario -> ') 

                if opcionMenu == '1' or opcionMenu == '2':
                    #CATC se  selecciona  a que   husuario se  enviara  en el topic
                    if opcionMenu == '1':
                        UX = USER_ID_2 
                    else:
                         UX= USER_ID_3 

                    #CATC empesamos con la grbacion del  audio 
                    now = datetime.now()
                    #CATC nomrbramos el  arcivo de  audio 
                    file_audio = "prueba.wav"
                    #CATCingresamos el  tiempo del audio 
                    audio_t = int(input("indique el tiempo de grabación >> "))
                    #CATC se  invica  a la  funcion  grabar  audio 
                    aud.record(audio_t, file_audio)
                    #CATC luego de  grabar  se  reproduce la grabacion 
                    aud.play(file_audio)
                    #CATC s e calcula  el tamño del  archivo par  enviarlo 
                    file_size = (os.stat(file_audio).st_size)
                    #CATC se  envia el  aviso a  al topic  comman/
                    ftr = com.command_ftr() + bytes(str(UX), 'utf-8') + bytes(str(file_size), 'utf-8')
                    cli.client.publish(cli.topic_esp(), ftr)
                    time.sleep(1)

                    for x in range(3):
                        time.sleep(0.2) 
                        #CATC verificacmos si estamso activos  en tcp teniendo 3  oportunidades    
                        if(bool(cli.tcp_a())==True):  
                            for x in range(2):
                                time.sleep(0.2)    
                                #CATC confirmamos si  estamos  activos   
                                if(bool(cli.tcp_a())==True):  
                                    print("enviar_audio")
                                    #CATC invicamos la  fucion enviar, para enviar  el audio 
                                    cli.enviar(file_audio)
                                    cli.enviar(file_audio)
                                
                       

                   

            elif opcionMenu == '2':
                cli.roomMenu()#CATC despliega  el menu de salas
                opcionMenu = input('\n\tDigite Sala -> ') 
                num=opcionMenu
                now = datetime.now()
                #CATC nomrbramos el  arcivo de  audio
                file_audio = "prueba.wav"
                audio_t = int(input("indique el tiempo de grabación >> "))
                #CATC se  invica  a la  funcion  grabar  audio 
                aud.record(audio_t, file_audio)
                #CATC luego de  grabar  se  reproduce la grabacion 
                aud.play(file_audio)
                #CATC s e calcula  el tamaño del  archivo par  enviarlo 
                file_size = (os.stat(file_audio).st_size)
                #CATC se  envia el  aviso a  al topic  comman/
                ftr = com.command_ftr() + bytes(str("16S0"+num), 'utf-8') + bytes(str(file_size), 'utf-8')
                cli.client.publish(cli.topic_esp(), ftr)
                time.sleep(1)
                for x in range(3):
                    time.sleep(0.2)
                    #CATC verificacmos si estamso activos  en tcp teniendo 3  oportunidades    
                    if(bool(cli.tcp_a())==True):  
                        for x in range(2):
                            time.sleep(0.2)
                            #CATC confirmamos si  estamos  activos      
                            if(bool(cli.tcp_a())==True):  
                                print("enviar_audio")
                                #CATC invicamos la  fucion enviar, para enviar  el audio 
                                cli.enviar(file_audio)
                                cli.enviar(file_audio)
                
                
                
        elif opcionMenu == '3':    
             exit() #CATC para el proceso 
             
            
        

except KeyboardInterrupt:#CATC para el proceso  y nos  desconectamos  del broker 
    print('Desconectando del broker MQTT...')
    cli.client.disconnect()#CATC nos  desconectams del cliente 
    if t1.isAlive():#CATC paramos  la funcions alive
        t1._stop()

finally:#CATC  finalmente muetra  el ensaje
     print('Se ha desconectado del broker. Saliendo...')
     