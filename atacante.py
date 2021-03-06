import subprocess
import threading
import socket
import sys
import os

FIN_COMANDO = b'#00#'

def inicializar_servidor(puerto):
    """
    Crea el servidor bind y se queda esperando
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', int(puerto)))  # hace el bind en cualquier interfaz disponible
    servidor.listen(5) # peticiones de conexion simultaneas
    print('Escuchando peticiones en el puerto %s' % puerto)
    while True:
        cliente, addr = servidor.accept()
        print('recibi la conexion de', addr)
        hiloc = threading.Thread(target=leer_comandos, args=(cliente, )) #hacemos un hilo para que los comandos siempre esten leyendose
        hiloc.start()

def leer_comandos(socket):
    """
    Función con la interfaz de usuario
    """
    comando = ''
    while comando != 'exit': 
        comando = input('$> ') # lee un str no binario
        respuesta = mandar_comando(comando, socket) 
    socket.close()



def mandar_comando(comando, socket):
    """
    Envía el comando a través del socket, haciendo conversiones necesarias
    Espera la respuesta del servidor y la regresa
    comando viene como str
    """
    comando = comando.encode('utf-8') # convertimos a binario el comando pasado
    comando += FIN_COMANDO #le añadimos el fin del comando
    print("el comando a mandar es:", comando)
    socket.send(comando) #mandamos el comando convertido en binario 
    salida = leer_respuesta(socket) #obtenemos la salida 
    desplegar_salida_comando(salida)


def leer_respuesta(socket):
    """
    Lee el canal de comunicación del servidor y reconstruye
    la salida asociada
    """
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += socket.recv(2048)
    a_quitar_caracteres = len(FIN_COMANDO) #le quitamos el final de comando
    return salida[:-a_quitar_caracteres] #regresa la salida 

def desplegar_salida_comando(salida):
    """
    Despliega la salida regresada por el servidor
    salida es una cadena binaria
    """
    salida = salida.decode('utf-8') #decodificamos el binario que nos envio
    print(salida)
    


if __name__ == '__main__':
    puerto = sys.argv[1]
    socket = inicializar_servidor(puerto) #inicializamos el servidor y le pasamos el puerto