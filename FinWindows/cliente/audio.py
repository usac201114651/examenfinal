
##USEOB librerias de audio para windows
import sounddevice as sd
import soundfile as sf
import threading 
import time
import os 
import sys

from scipy.io.wavfile import write

#USEOB creamos el objeto sonido, constructor con su tasa de muestreo
class Sonido():
    def __init__(self):    
        self.fs = 44100  
        

#USEOB metodo para grabar
    def record(self, seconds, filename_rec):
        self.filename_rec = filename_rec
        self.seconds = seconds
        self.myrecording = sd.rec(int(self.seconds * self.fs), samplerate = self.fs, channels=2)
        print ('Grabando')
        sd.wait()  # Wait until recording is finished
        write(self.filename_rec, self.fs, self.myrecording)  # Save as WAV file 
        # Extract data and sampling rate from file

    def play(self, filename_play):    
        self.filename_play = filename_play 
        print ('Reproduciendo')
        data, self.fs = sf.read(self.filename_play , dtype='float32')  
        sd.play(data, self.fs)
        status = sd.wait()  # Wait until file is done playing

t1 = threading.Thread(name = 'alive', #iniciamos la ejecución por hilo, pusimos el demonio en false pero daba error
                            target = Sonido,
                            daemon = True)

listaHilos = []
t1.start() #iniciamos el hilo