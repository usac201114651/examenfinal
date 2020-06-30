#MTEZ variables
ALIVE_PERIOD            = 2            #Período entre envío de tramas ALIVE
ALIVE_CONTINUOUS        = 0.1      #Período entre envío de tramas ALIVE si no hay respuesta

#MTEZ COMMANDS
COMMAND_FRR             = b'\x02'
COMMAND_FTR             = b'\x03'
COMMAND_ALIVE           = b'\x04'
COMMAND_ACK             = b'\x05'
COMMAND_OK              = b'\x06'
COMMAND_NO              = b'\x07'

#MTEZ System filenames
USERS_FILENAME          = "usuario.txt"
ROOMS_FILENAME          = "salas.txt"

