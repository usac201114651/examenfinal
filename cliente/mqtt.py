import paho.mqtt.client as paho
import threading 
import binascii
import logging
import time
import random
import os 
import socket
import sys

from globals import *    #variables globales
from comandos import Comandos

comand = Comandos()



LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

class Mqtt(object):
 
    def __init__(self, MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT ):
        self.MQTT_USER = MQTT_USER
        self.MQTT_PASS = MQTT_PASS
        self.MQTT_HOST = MQTT_HOST
        self.MQTT_PORT = MQTT_PORT
        self.SERVER_ADDR = socket.gethostbyname(socket.gethostname()) 
        self.SERVER_PORT = 9816
        self.BUFFER_SIZE = 6400
        
        self.client = paho.Client(clean_session=True)                         
        self.client.on_publish = self.on_publish                              
        self.client.on_message = self.on_message                              
        self.client.username_pw_set(self.MQTT_USER, self.MQTT_PASS)            
        self.client.connect(host=self.MQTT_HOST, port = self.MQTT_PORT)       
        #se extrae el id del cliente
        archivo = open(USERS_FILENAME,'r')
        self.cod_carnet = str(archivo.readline())[0:9]
        archivo.close()
        #se extrae el grupo del cliente
        archivo = open(ROOMS_FILENAME,'r')
        self.grupo = archivo.readline(2)
        archivo.close()
        #se extrae las salas del cliente
        archivo = open(ROOMS_FILENAME,'r')
        for linea in archivo.readlines():
            self.client.subscribe(("salas/"+ self.grupo +"/"+linea[0:len(linea)-1]),2)
        archivo.close()
        self.topic_1      = "comandos" + "/" + str(self.grupo) + "/" + str(self.cod_carnet)
        self.topic_2      = "usuarios/16" + "/" + str(self.cod_carnet)
        self.topic_alive  = "comandos" + "/" + str(self.grupo)
        self.topic_4      = "salas/16" + "/" + str(self.grupo)
        self.client.subscribe(self.topic_1, 2)           
        self.client.subscribe(self.topic_2, 2)   
        self.client.subscribe(self.topic_4, 2) 
        self.client.loop_start()
        self.flag_tcp = False

    def topic_esp(self):
     return str(self.topic_1)    

    def topicalive(self):
      return str(self.topic_alive) 

    def carnet(self):
      return str(self.cod_carnet)

    def room(self):
      return str(self.grupo)    

    def topic_comandos(self):
      return str(self.topic_1)  

    def topic_usuarios(self):
      return str(self.topic_2)  

    def on_publish(self, client, userdata, mid): 
        publishText = 'Publicación satisfactoria'
        #print(publishText)
   
    #Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self,client, userdata, msg):
       #•	Algoritmo para redirección de archivos de audio
        logging.info((str(msg.payload)))
        self.data_1= ((str(msg.payload))[6:15])
        self.data_2= ((str(msg.payload))[0:6]+"'")
        self.data_3= ((str(msg.payload))[0:6]+"'")
        self.data_4= ((str(msg.payload))[0:6]+"'")
        print("11")
        print(msg.payload)
        #algoritmo recepcion audio desde servidor
        if(self.data_2==(str(comand.command_frr()))): 
          print(self.data_2)
          print(((str(msg.payload))[0:6]+"'"))
          print("22")
          self.recibir()

        if(self.data_2==(str(comand.command_ok()))): 
          print(self.data_3)
          self.flag_tcp = True
          print(bool(self.flag_tcp))
          print("33")

        if(self.data_3==(str(comand.command_no()))): 
          print(self.data_4)
          self.flag_tcp = False
          print("44")
          logging.error('Usuario no activo')
          run=False  

        
    def tcp_a(self):
       return bool(self.flag_tcp)

    def enviar(self, paquete):
          print("enviar")
          self.filename = paquete
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.bind((self.SERVER_ADDR, self.SERVER_PORT))
          sock.listen(10) #1 conexion activa y 9 en cola
          run = True
          try:
            while run: 
                print("\nEsperando conexion remota...\n")
                conn, addr = sock.accept()
                opcionMenu = input('\n\t presione el #3 -> ') 
                if(opcionMenu == "salir"):
                  run = False
                with open(self.filename, 'rb') as f: #Se abre el archivo a enviar en BINARIO
                    conn.sendfile(f, 0)
                f.close()
                run = False
                
          except KeyboardInterrupt:
           print('Desconectando del broker MQTT...')
           sock.close()   

          finally:
           sock.close()   

# recepcion de audio      
    def recibir(self):
        self.arch_audio = "prueba2.wav" #str(datetime.timestamp(now))+".wav"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex((self.SERVER_ADDR, self.SERVER_PORT))
        try:
             buff = sock.recv(self.BUFFER_SIZE)
             file_to_open = os.path.expanduser('self.arch_audio')
             f = open(file_to_open, 'wb+') #Aca se guarda el archivo entrante

             while buff:
                f.write(buff)
                buff = sock.recv(self.BUFFER_SIZE) #Los bloques se van agregando al archivo
             f.close() #Se cierra el archivo
             print("Recepcion de archivo finalizada")
          
        except KeyboardInterrupt:
         print('Desconectando del broker MQTT...')
         sock.close()

        finally:
         print("Cerrando el servidor...")
         sock.close() 
          
          
    

         
            
    