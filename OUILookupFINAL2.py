import time #Libreria dedicada al trabajo del tiempo
import requests #Libreria dedicada para realizar solicitudes a paginas web 
import getopt #Analasis de argumentos
import sys #Permite algunas interacciones con el sistema y el intérprete de Python.
import subprocess #Permite ejecutar programas o scripts externos y capturar su salida
import re # Permite buscar, manipular, y analizar textos en base a patrones
import platform #Dedicada a detectar el sistema operativo 

def mensajeHelp(): #Funcion del mensaje help
    print("""
          Use: python OUIlookup.py --mac <mac> | --arp | [--help]
          --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
          --arp: Muestra los fabricantes de los host disponibles en la tabla arp.
          --help: Muestra este mensaje y termina.
          """)
def consultarMac(mac): #Funcion que busca fabricantes, recibe la direccion MAC y retorna su fabricante
    url = f"https://api.maclookup.app/v2/macs/{mac}" #Request para recibir la info asociada a la MAC 
    response = requests.get(url) #Se almacena la info asociada 
    
    data = response.json()  #Se almacena en un archivo de texto
    if data.get("success") and data.get("found"): #Caso: Si esta registrada la MAC
         fabricante = data.get("company", "Desconocido") #Se obtiene el nombre del fabricante
         return fabricante
    else: #Caso: La MAC no esta registrada
        return "Not found"
    
def mostrarARP(): #Funcion que muestra la tabla ARP con sus fabricantes
    print("MAC/VENDOR")
    sistema = platform.system().lower() #Guardamos el sistema operativo 
    comando_arp = "arp -a" #Mismo comando para ambos sistemas 
    result = subprocess.check_output(comando_arp, shell=True, text=True) #Obtencion de tabla ARP con IPS y MAC de el dispositivo en la red
    if sistema == "windows":
        #Formato de Direccion MAC
        macs = re.findall(r"([0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2})", result)
        macs_formateadas = [mac.replace('-', ':') for mac in macs] #Las ordenamos al formato deseado Cambiando - por :
    else:
        #Formato de Direccion MAC
        macs = re.findall(r"([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})", result)
        macs_formateadas = macs  #Ya se encuentran en el formato deseado con :
    for mac in macs_formateadas:
        print(mac+" / "+consultarMac(mac) )
def main():
    #Lectura de arumentos
    opts, args = getopt.getopt(sys.argv[1:], "", ["help", "mac=", "arp"])
    #Definicion de variables de posibles argumentos
    arguementoMac = None
    argumentoHelp = True
    ArgumentoARP = False
    #En caso de ser seleccionada su estado cambiara a true y entrara al if 
    for opt, arg in opts:
        if opt == "--help":
            continue
        elif opt == "--mac":
            argumentoHelp = False
            arguementoMac = arg
        elif opt == "--arp":
            argumentoHelp = False
            ArgumentoARP = True
    # Comportamiento según los argumentos
    if argumentoHelp: #Caso argumento : --help
        mensajeHelp()
        return
    if arguementoMac: #Caso argumento --mac
        start_time = time.time() #Comienza a correr el tiempo de demora para la solicitud 
        fabricante = consultarMac(arguementoMac) #Se hace la consulta
        tiempo_respuesta = (time.time() - start_time) * 1000  #El cronometro se detiene
        print(f"MAC Address      : {arguementoMac}")
        print(f"Fabricante       : {fabricante}") 
        print(f"Tiempo de respuesta: {tiempo_respuesta:.0f}ms")
        return
    if ArgumentoARP: #Caso argumento --arp
        mostrarARP()
        return
if __name__ == "__main__":
    main()


