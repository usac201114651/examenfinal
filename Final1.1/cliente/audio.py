#USEOB imbocamos libreias
import threading 
import time
import os 
import sys


#USEOB iciamos una calse  sonido
class Sonido():
    def __init__(self):    
        self.fs = 44100  
        
    #USEOB  nos ayudar  a garbar   los  audios a  enviar,  con todos  los  parametros  que  resive  
    def record(self, seconds, filename_rec):
        self.filename_rec = filename_rec
        self.seconds = seconds
        seconds1=str(seconds)
        os.system('arecord -d ' + seconds1 +' -f U8 -r 8000 '+ filename_rec)
    #USEOB   nos  ayudara  a reproducirl  loa  audios  enviados     
    def play(self, filename_play):    
        self.filename_play = filename_play 
        print ('Reproduciendo')
        os.system('aplay '+ filename_play)
       
#USEOB  mantenemos  activos los  alives 
t1 = threading.Thread(name = 'alive',
                            target = Sonido,
                            daemon = True)

t1.start()