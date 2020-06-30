#se intenta hacer la gestión de comandos através de las funciones
import os 
import sys

from globals import *    #variables globales

class Comandos(object):
 
    def command_alive(self):
        return COMMAND_ALIVE  

    def command_ftr(self):
        return COMMAND_FTR 

    def command_ack(self):
        return COMMAND_ACK 

    def command_ok(self):
        return COMMAND_OK  

    def command_no(self):
        return COMMAND_NO  

    def command_frr(self):
        return COMMAND_FRR 

    def delay_a(self):
        return ALIVE_PERIOD    


            
         
           
            
            