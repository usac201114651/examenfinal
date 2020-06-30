#CATC importamos  librerias  autilizar 
import paho.mqtt.client as paho
import threading 
import binascii
import logging
import time
import random
import os 
import socket
import sys
#CATC importamos  variables  de los programas
from globals import *    #CATC variables globales
from comandos import Comandos#CATC importamos  comandos

comand = Comandos()


#CATC  configuramos  los  levels   con logging
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

#CATC  creamos la  clase  Mqtt 
class Mqtt(object):
    #CATC inicializamos  variables 
    def __init__(self, MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT,USER_ID_1,USER_ID_2,USER_ID_3 ):
        self.MQTT_USER = MQTT_USER
        self.MQTT_PASS = MQTT_PASS
        self.MQTT_HOST = MQTT_HOST
        self.MQTT_PORT = MQTT_PORT
        self.SERVER_ADDR = socket.gethostbyname(socket.gethostname()) 
        self.SERVER_PORT = 9816
        self.BUFFER_SIZE = 64*1024
        self.USER_ID_1  = USER_ID_1
        self.USER_ID_2  = USER_ID_2
        self.USER_ID_3  = USER_ID_3
        
        #CATC  configuramos el cliente MqTT

        self.client = paho.Client(clean_session=True)                         
        self.client.on_publish = self.on_publish                              
        self.client.on_message = self.on_message                              
        self.client.username_pw_set(self.MQTT_USER, self.MQTT_PASS)            
        self.client.connect(host=self.MQTT_HOST, port = self.MQTT_PORT)    

        ##CATC se extrae el id del cliente
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
            #CATC  se  subscribe al cliente  a los topics  
            self.client.subscribe(("salas/"+ self.grupo +"/"+linea[0:len(linea)-1]),2)
            self.client.subscribe(("audio/"+ self.grupo +"/"+linea[0:len(linea)-1]),2)
        archivo.close()

        #CATC  se  asignan unos  topics
        self.topic_1      = "comandos/"+ str(self.grupo) + "/" + str(self.cod_carnet) 
        self.topic_2      = "usuarios/16/"+ str(self.cod_carnet)
        self.topic_alive  = "comandos" + "/" + str(self.grupo)
        #self.topic_4      = "usuarios/#" #+ str(self.grupo)
        self.topic_5      = "audio" + "/" + str(self.grupo) + "/" + str(self.cod_carnet)
       
       #CATC   se  subscribe  a  los topics
        self.client.subscribe(self.topic_1, 2)           
        self.client.subscribe(self.topic_2, 2)   
        self.client.subscribe(self.topic_5, 2) 
        self.client.loop_start()
        self.flag_tcp = False
    #USEOB  devuelbe el  nombre  del topoc 
    def topic_esp(self):
     return str(self.topic_1)    
    #USEOB devuelve el topic de los  live
    def topicalive(self):
      return str(self.topic_alive) 
    #USEOB envia el carnet del  usuario 
    def carnet(self):
      return str(self.cod_carnet)
    #USEOB envia  el numero de  grupo  16
    def room(self):
      return str(self.grupo)    
    #USEOB envia el  topic  comandos 
    def topic_comandos(self):
      return str(self.topic_1)  
    #USEOB envia  el topic del  usuario
    def topic_usuarios(self):
      return str(self.topic_2)  
    #USEOB es  un  aviso de  nuestros  mensajes  enviados 
    def on_publish(self, client, userdata, mid): 
        publishText = 'Publicación satisfactoria'
        #print(publishText)
   
    #CATC Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self,client, userdata, msg):
       #CATC 	Algoritmo para redirección de archivos de audio
        print((str(msg.payload)))
        self.data_1= ((str(msg.payload))[6:15])
        self.data_2= ((str(msg.payload))[0:6]+"'")
        self.data_3= ((str(msg.payload))[0:6]+"'")
        self.data_4= ((str(msg.payload))[0:6]+"'")
        print("11")
        #CATC algoritmo recepcion audio desde servidor
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
        
        #USEOB  si el  usuario se  encuentra  desconectado
        if(self.data_3==(str(comand.command_no()))): 
          print(self.data_4)
          self.flag_tcp = False
          print("44")
          logging.error('Usuario no activo')
          run=False  

    #USEOB muestra  nuestro estado  en tcp    
    def tcp_a(self):
       return bool(self.flag_tcp)
    #USEOB  funcion para enviar los archivos 
    def enviar(self, paquete):
          print("enviar")
          self.filename = paquete
          sock = socket.socket()
          sock.bind((self.SERVER_ADDR, self.SERVER_PORT))
          sock.listen(10) # #USEOB1 conexion activa y 9 en cola
          run = True
          try:
            while run: 
                print("\nEsperando conexion remota...\n")
                conn, addr = sock.accept()
                opcionMenu = input('\n\t presione el #3 -> ') 
                if(opcionMenu == "salir"):
                  run = False
                with open(self.filename, 'rb') as f: #USEOBSe abre el archivo a enviar en BINARIO
                    conn.sendfile(f, 0)
                f.close()
                run = False
                
          except KeyboardInterrupt:#USEOB nos  desconecta
           print('Desconectando del broker MQTT...')
           sock.close()   

          finally: #USEOB  sierra  el programa
           sock.close()   

#CATC  recepcion de audio      
    def recibir(self):
        print("recibir")
        now = datetime.now()
        self.arch_audio=str(datetime.timestamp(now))+".wav"
        sock=socket.socket()
        sock.connect_ex((self.SERVER_ADDR,self.SERVER_PORT))
        try:
             buff = sock.recv(self.BUFFER_SIZE)
             file_to_open = os.path.expanduser('self.arch_audio')
             f = open(file_to_open, 'wb+')  #USEOB Aca se guarda el archivo entrante

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
          
    #USEOB es el menú principal
    def mainMenu(self): 
        #os.system('clear') 
        print ('Menú principal')
        print ('\t1 - Enviar texto')
        print ('\t2 - Enviar mensaje de voz')
        print ('\t3 - Salir')
      
    
    #USEOB menú de selección
    def typeMenu(self):  
        #os.system('clear') 
        print ('Seleccione una opcion')
        print ('\t1 - Enviar a usuario')
        print ('\t2 - Enviar a sala')

    #USEOB menú de usuarios
    def userMenu(self):  
        #os.system('clear') 
        print ('Seleccione Seleccione un usuario')
        print ('\t1 -'+ USER_ID_2)
        print ('\t2 -'+ USER_ID_3)
       
    #USEOB menú de salas
    def roomMenu(self):  
        #os.system('clear') 
        print ('Seleccione Sala')
        print ('\t0 - S00')
        print ('\t1 - S01')
        print ('\t2 - S02')
        print ('\t3 - S03')

    #CATC funcion para enviar mensaje a un usuario
    def sendTextUser(self,num):
        #os.system('clear')
        #CATC se diferencia al usuario destinatario
        self.num = num  
        if num == 1:
            UX = USER_ID_2
        else:
            UX = USER_ID_3 

        a_enviar = input ('Escribe mensaje ->')
        a_enviar = "A llegado un mensaje a USUARIO " +str(UX)+" ->-> "+self.USER_ID_1 + ' dice: ' + a_enviar
        self.client.publish(('usuarios/16/' +str(UX)), a_enviar)
        print('...enviado')   
    #CATC funcion para enviar mensaje a un salas
    def sendTextRoom(self,num):
        #os.system('clear')
        self.num=num             
        a_enviar = input ('Escribe mensaje ->')
        a_enviar = "A llegado un mensaje a SALA 16S0"+ str(num)+" ->-> "+self.USER_ID_1 + ' dice: ' + a_enviar
        self.client.publish(("salas/16/16S0"+ str(num)),  a_enviar )
        print('...enviado') 
              
         
            
    