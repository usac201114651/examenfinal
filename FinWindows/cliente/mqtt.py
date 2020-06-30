#CATC Importamos librerias necesarias
import paho.mqtt.client as paho
import threading 
import binascii
import logging
import time
import random
import os 
import socket
import sys

from globals import *    #CATC variables globales
from comandos import Comandos
from datetime import datetime

comand = Comandos()


#CATCniveles del loggin
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
#CATC creamos la clase Mtt ("cliente")
class Mqtt(object):
 #CATC constructor de la clase, recibe credenciales del MQTT
    def __init__(self, MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT ):
        self.MQTT_USER = MQTT_USER
        self.MQTT_PASS = MQTT_PASS
        self.MQTT_HOST = MQTT_HOST
        self.MQTT_PORT = MQTT_PORT
        self.SERVER_ADDR = socket.gethostbyname(socket.gethostname()) #IP para conectar el socket tcp
        self.SERVER_PORT = 9816 #definimos el puerto TCP
        self.BUFFER_SIZE = 8*1024 #tamaño del buffer 
        
        self.client = paho.Client(clean_session=True)                         
        self.client.on_publish = self.on_publish                              
        self.client.on_message = self.on_message                              
        self.client.username_pw_set(self.MQTT_USER, self.MQTT_PASS)            
        self.client.connect(host=self.MQTT_HOST, port = self.MQTT_PORT)       
        #CATC se extrae el id del cliente
        archivo = open(USERS_FILENAME,'r')
        self.cod_carnet = str(archivo.readline())[0:9]
        archivo.close()
        #CATC se extrae el grupo del cliente
        archivo = open(ROOMS_FILENAME,'r')
        self.grupo = archivo.readline(2)
        archivo.close()
        #CATC se extrae las salas del cliente
        archivo = open(ROOMS_FILENAME,'r')
        for linea in archivo.readlines():
            self.client.subscribe(("salas/"+ self.grupo +"/"+linea[0:len(linea)-1]),2)
        archivo.close()
        self.topic_1      = "comandos" + "/" + str(self.grupo) + "/" + str(self.cod_carnet)
        self.topic_2      = "usuarios" + "/" + str(self.cod_carnet)
        self.topic_alive  = "comandos" + "/" + str(self.grupo)
        self.topic_4      = "usuarios" + "/" + str(self.grupo)
        self.client.subscribe(self.topic_1, 2)           
        self.client.subscribe(self.topic_2, 2)   
        self.client.subscribe(self.topic_4, 2) 
        self.client.loop_start()
        self.flag_tcp = False

#CATC Métodos para el ordenamiento de los topics
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
   
    #USEOB Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self,client, userdata, msg):
       #USEOB Acá dividimos la trama de mensaje

        logging.info((str(msg.payload)))
        self.data_1= ((str(msg.payload))[6:15])
        self.data_2= ((str(msg.payload))[0:6]+"'")
        self.data_3= ((str(msg.payload))[0:6]+"'")
        self.data_4= ((str(msg.payload))[0:6]+"'")
        print(msg.payload) #USEOB para mostrar los mensajes        
        
        #USEOB algoritmo recepcion audio desde servidor
        if(self.data_2==(str(comand.command_frr()))): 
          print("22")
          self.recibir()
        if(self.data_2==(str(comand.command_ok()))): 
          self.enviar("enviar.wav")
        if(self.data_3==(str(comand.command_no()))): 
          logging.error('Usuario no activo')

    #USEOB método para envio del paquete por tcp
    def enviar(self, paquete):
           sock = socket.socket() #USEOB iniciamos el socket
           sock.bind((self.SERVER_ADDR, self.SERVER_PORT))
           sock.listen(10) 

           try: #USEOB inicia la comunicación
                while True: 
                     print("\nEsperando conexion remota...\n")
                     conn, addr = sock.accept()
                     with open('enviar.wav', 'rb') as f: # USEOB Se abre el archivo a enviar en BINARIO
                        conn.sendfile(f, 0)
                     f.close()
                     logging.info("Mensaje enviado...")
                     print("\n\nArchivo enviado a: ", addr) #muestra a donde se envía el paquete
           except:
              conn.close()


#USEOB recepcion de audio      
    def recibir(self):
        print("recibir")
        now = datetime.now()
        self.arch_audio = str(datetime.timestamp(now))+".wav"
        sock = socket.socket()
        sock.connect((self.SERVER_ADDR, self.SERVER_PORT))
        try:
             buff = sock.recv(self.BUFFER_SIZE) 
             file_to_open = os.path.expanduser(self.arch_audio)
             f = open(file_to_open, 'wb+') #USEOB Aca se guarda el archivo entrante

             while buff:
                f.write(buff)
                buff = sock.recv(self.BUFFER_SIZE) #USEOB Los bloques se van agregando al archivo
             f.close() #USEOB Se cierra el archivo
             print("Recepcion de archivo finalizada")
          
        except KeyboardInterrupt:
         print('Desconectando del broker MQTT...')
         sock.close()

        finally:
         print("Cerrando el servidor...")
         sock.close() 
          
          
    

         
            
    