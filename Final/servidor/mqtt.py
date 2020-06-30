#comentado MTEZ

import paho.mqtt.client as mqtt
import threading
import logging
import time
import os 
import socket
import sys
#MTEZ importamos variables globales
from globals import *    #variables globales
from comandos import Comandos

com = Comandos()
#banderas indicadoras
tag  = 'Cli'
tag1 = 'Fr'
lista = []

#MTEZ Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
#MTEZ creamos la clase servidor
class Servidor():
  #el constructor recibe parametros de mqtt
   def __init__(self, MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT ):
        qos=2 #estatus de calidad de servicio en 2
        self.MQTT_USER = MQTT_USER
        self.MQTT_PASS = MQTT_PASS
        self.MQTT_HOST = MQTT_HOST
        self.MQTT_PORT = MQTT_PORT
        self.client = mqtt.Client(clean_session=True)                      #Nueva instancia de cliente
        self.client.on_publish = self.on_publish                           #Se configura la funcion "Handler" que se activa al publicar algo
        self.client.on_message = self.on_message                           #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.username_pw_set(self.MQTT_USER, self.MQTT_PASS)                  #Credenciales requeridas por el broker
        self.client.connect(host= self.MQTT_HOST, port = self.MQTT_PORT) #conectamos al broker   
        self.SERVER_ADDR = ""#socket.gethostbyname(socket.gethostname()) #ahora esta en host la ip
        self.SERVER_PORT = 9816 #conectar al puerto 9816 para el tcp
        self.BUFFER_SIZE = 8*1024 #tamaño del buffer
        self.flag_tcp = False #bandera de tcp inicializada en falso

   #MTEZ algoritmo topics obtenidos por archivos de texto
   def run_topics(self):               
        archivo = open(ROOMS_FILENAME,'r')
        self.grupo = archivo.readline(2)
        archivo.close()
        self.topic_alive = ("comandos"+"/"+self.grupo)
        self.client.subscribe(self.topic_alive,2)
        archivo = open(USERS_FILENAME,'r')
        for linea in archivo.readlines():
            self.topic_com = ("comandos"+"/"+self.grupo+"/"+str(linea[0:9]))
            self.client.subscribe(self.topic_com,2)
        archivo.close()
        archivo = open(USERS_FILENAME,'r')
        for linea in archivo.readlines():
            self.client.subscribe(("usuarios/16/"+str(linea[0:9])),2)
            self.client.subscribe(("audio/16/"+str(linea[0:9])),2)
        archivo.close()
        archivo = open(ROOMS_FILENAME,'r')
        for linea in archivo.readlines():
            self.client.subscribe(("salas"+"/"+self.grupo+"/"+ str(linea[0:len(linea)-1])),2)
            self.client.subscribe(("salas"+"/"+self.grupo+"/"+ str(linea[0:len(linea)-1])),2)
        archivo.close()
        self.client.loop_start()
        

   #MTEZ Callback que se ejecuta cuando nos conectamos al broker
   def on_connect(self,client, userdata, rc):
        logging.info("Conectado al broker")

   #MTEZ Handler en caso se publique satisfactoriamente en el broker MQTT
   def on_publish(self,client, userdata, mid): 
        publishText = "Publicacion satisfactoria"
        logging.info(publishText)

    #MTEZ EN ÉSTE MÉTODO GENERAMOS LAS LISTAS DE CLIENTES ACTIVOS
     
   def on_message(self,client, userdata, msg): 
        #logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        #logging.info("El contenido del mensaje es: " + str(msg.payload))
        #diccionario alive

        if(str(msg.topic) == self.topic_alive):
            list_alive = str((str(msg.payload))[6:15])
            
            if(len(lista)==0):
                lista.append({tag:list_alive, tag1:0}) 

            flag = True

            for i in range(0,len(lista)):
                    lista[i][tag1] = lista[i][tag1] + 1

            for i in range(0,len(lista)):
                    if list_alive == lista[i][tag]:
                                flag = False
                                lista[i][tag1] = 0
                    if  lista[i][tag1] >= 3:
                        del lista[i]
            
            if(flag):
             lista.append({tag:list_alive, tag1:0}) 

        print(lista)

        ##MTEZ PARA VERIFICAR LOS CLIENTES CONECTADOS, además se gestionan los comandos de negociación
        if(((str(msg.payload))[0:6]+"'")==(str(com.command_ftr()))):
              self.client_envia    = str((str(msg.topic)))[12:(len(str(msg.payload)))] 
              self.destino         = (str(msg.payload))[6:15]
              self.tamaño          = (str(msg.payload))[16:(len(str(msg.payload))-1)] 
              for i in range(0,len(lista)):
                 if self.destino  == lista[i][tag]:
                   a_dato = com.command_ok() + bytes((self.client_envia), 'utf-8')
                   self.client.publish(("comandos"+"/"+self.grupo+"/"+self.client_envia), a_dato)
                   time.sleep(1)
                   self.flag_tcp = True 
                   print("tcp")
                   self.mens()  
                 else:
                   a_dato1 = com.command_no() + bytes((self.client_envia), 'utf-8')
                   self.client.publish(("comandos"+"/"+self.grupo+"/"+self.client_envia), a_dato1)
                   self.flag_tcp = False
    ##MTEZ USAMOS ESTE METODO PARA USAR EL RESULTADO DE LA BANDERA TCP
   def mens(self):
        if(self.flag_tcp == True):
            self.recibir() 

   # MTEZ recepcion de audio      
   def recibir(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex((self.SERVER_ADDR, self.SERVER_PORT))
        try:
             print("tcp_recibiendo")
             buff = sock.recv(self.BUFFER_SIZE)
             print("stocontiene el bufer:"+  str(buff))
             file_to_open = os.path.expanduser('temporal.wav')
             f = open(file_to_open, 'wb+') #MTEZ abrimos el archivo entrante

             while buff:
                f.write(buff)
                buff = sock.recv(self.BUFFER_SIZE) #MTEZ Los bloques se van agregando al archivo
             f.close() #MTEZ Se cierra el archivo
             print("Recepcion de archivo finalizada")
             self.a_dato2 = com.command_frr() + bytes((str(self.destino)), 'utf-8')
             self.client.publish(("comandos"+"/"+self.grupo+"/"+str(self.destino)), self.a_dato2) #negociacion "intento"
             time.sleep(1)
             self.enviar() #MTEZ llamamos al envio
        except KeyboardInterrupt:
         print('Desconectando del broker MQTT...')
         sock.close()
        finally:
  
         ""
             
   def enviar(self): #MTEZ metodo para el envio de audio
        self.filename = 'temporal.wav'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.SERVER_ADDR, self.SERVER_PORT))
        sock.listen(5) #1 conexion activa y 9 en cola
        run = True
        try:
            while run: 
                print("\nEsperando conexion remota...\n")
                conn, addr = sock.accept()
                opcionMenu = input('\n\t presione el #3 -> ') 
                if(opcionMenu == "3"): #MTEZ se pide confirmacion
                  run = False
                with open(self.filename, 'rb') as f: #MTEZ Se abre el archivo a enviar en BINARIO
                    conn.sendfile(f, 0)
                f.close()
                run = False
                
        except KeyboardInterrupt:
           print('Desconectando del broker MQTT...')
           sock.close()   

        finally:
           sock.close()
       

  
