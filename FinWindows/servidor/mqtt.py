#MTEZ importamos las librerias necesarias
import paho.mqtt.client as mqtt
import threading
import logging
import time
import os 
import socket
import sys


from globals import *    #MTEZ variables globales
from comandos import Comandos

com = Comandos() #MTEZ objeto tipo Comandos
#MTEZ banderas indicadoras
tag  = 'Cli'
tag1 = 'Fr'
lista = []

#MTEZ Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#MTEZ constructor de la Clase, recibe credenciales de MQTTT, también se definen los parámetros de conexión del socket
class Servidor():
   
   def __init__(self, MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT ):
        qos=2 #MTEZ estatus de calidad de servicio del mqtt
        self.MQTT_USER = MQTT_USER
        self.MQTT_PASS = MQTT_PASS
        self.MQTT_HOST = MQTT_HOST
        self.MQTT_PORT = MQTT_PORT
        self.client = mqtt.Client(clean_session=True)                      #Nueva instancia de cliente
        self.client.on_publish = self.on_publish                           #Se configura la funcion "Handler" que se activa al publicar algo
        self.client.on_message = self.on_message                           #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.username_pw_set(self.MQTT_USER, self.MQTT_PASS)                  #Credenciales requeridas por el broker
        self.client.connect(host= self.MQTT_HOST, port = self.MQTT_PORT)   
        self.SERVER_ADDR = socket.gethostbyname(socket.gethostname()) 
        self.SERVER_PORT = 9816 #METZpuerto en el que escucha el servidor
        self.BUFFER_SIZE = 8*1024 #MTEZtamaño del buffer
        self.flag_tcp = False #MTEZ bandera de tcp inicializada en falso

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
            self.client.subscribe(("usuarios"+"/"+str(linea[0:9])),2)
        archivo.close()
        archivo = open(ROOMS_FILENAME,'r')
        for linea in archivo.readlines():
            self.client.subscribe(("salas"+"/"+self.grupo+"/"+ str(linea[0:len(linea)-1])),2)
        archivo.close()
        self.client.loop_start()
        

   #MTEZ Callback que se ejecuta cuando nos conectamos al broker
   def on_connect(self,client, userdata, rc):
        logging.info("Conectado al broker")

   #MTEZ Handler en caso se publique satisfactoriamente en el broker MQTT
   def on_publish(self,client, userdata, mid): 
        publishText = "Publicacion satisfactoria"
        #logging.debug(publishText)

    #MTEZ Callback que se ejecuta cuando llega un mensaje al topic suscrito, EN ÉSTE MÉTODO GENERAMOS LAS LISTAS DE CLIENTES ACTIVOS
     
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

        print(lista) #MTEZ PARA VERIFICAR LOS CLIENTES CONECTADOS, además se gestionan los comandos de negociación
        #MTEZ algoritmo transferencia de audio
        if(((str(msg.payload))[0:6]+"'")==(str(com.command_ftr()))):
              self.client_envia = str((str(msg.topic)))[12:(len(str(msg.payload)))] 
              self.destino = (str(msg.payload))[6:15]
              self.tamaño = (str(msg.payload))[16:(len(str(msg.payload))-1)] 
              for i in range(0,len(lista)):
                 if self.destino  == lista[i][tag]:
                   a_dato = com.command_ok() + bytes((self.client_envia), 'utf-8')
                   self.client.publish(("comandos"+"/"+self.grupo+"/"+self.client_envia), a_dato)
                   time.sleep(1)
                   self.flag_tcp = True
                 else:
                   a_dato1 = com.command_no() + bytes((self.client_envia), 'utf-8')
                   self.client.publish(("comandos"+"/"+self.grupo+"/"+self.client_envia), a_dato1)
                   self.flag_tcp = False

   def temp(self): #MTEZ USAMOS ESTE METODO PARA USAR EL RESULTADO DE LA BANDERA TCP
       return bool(self.flag_tcp)                   

   #MTEZ recepcion de audio      
   def recibir(self):
        print("tcp_recibir")
        sock = socket.socket() #MTEZ iniciamos el socket, 
        sock.connect((self.SERVER_ADDR, self.SERVER_PORT)) #MTEZ indicamos donde iniciamos el soket, ip por el momento en host, y puerto designado
        print("tcp_recibir2")
        try:
                print("tcp_recibir21")
                buff = sock.recv(10*1024) #MTEZ definimos la variable para recibir la transferencia
                print("tcp_recibir22")
                file_to_open = os.path.expanduser("temporal.wav") #MTEZ abrimos el archivo o creamos uno nuevo
                print("tcp_recibir23")
                f = open(file_to_open, 'wb+') #MTEZ Aca se guarda el archivo entrante
                print("tcp_recibir3")
 
                while buff:
                    f.write(buff) #MTEZ acá recibimos la transferencia
                    buff = sock.recv(self.BUFFER_SIZE) #MTEZ Los bloques se van agregando al archivo
                f.close() #Se cierra el archivo
                print("Recepcion de archivo finalizada")
        except:
            sock.close #MTEZ cerramos el socket
            self.flag_tcp = False #MTEZ ponemos la bandera de tcp abajo
             

             #MTEZ método para envío a clientes
   def enviar(self): 
        self.filename = 'temporal.wav' #MTEZ archivo a enviar, donde se guardó la ultima recepción
        sock = socket.socket() #abrimos el soket
        sock.bind((self.SERVER_ADDR, self.SERVER_PORT)) #MTEZ conectamos el soket con bind
        sock.listen(10) #10 conexiones a recibir
        run = True
        try:
            while run: #metodo para esperar la conexion remota
                print("\nEsperando conexion remota...\n") 
                conn, addr = sock.accept()
                opcionMenu = input('\n\t presione el #3 -> ') 
                if(opcionMenu == "salir"):
                  run = False
                with open(self.filename, 'rb') as f: #Se abre el archivo a enviar en BINARIO y se envía
                    conn.sendfile(f, 0)
                f.close()
                run = False
                
                #excepcion para desconectar
        except KeyboardInterrupt:
           print('Desconectando...')
           sock.close()   
#cerramos el soket
        finally:
           sock.close()
       

  