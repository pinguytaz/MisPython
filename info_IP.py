#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  info_IP.py:  Información sobre una IP pasada, generado para python3
#
#  Historico:
#     - 26 Octubre 2023	V1:	Creación.
#
#  Librerias
################################################################################
import sys
import os
import ipaddress
import socket
import requests

def main(argv):
    
    if len(argv) < 2: # Se tienen que poner IPs
        print ("Uso: python info_IP.py <IPs>")
    else:
        miip = requests.get('https://icanhazip.com').text.strip()
        print("Mi IP: ",miip)
        info_ip(miip)
        for laip in argv[1:]:   # Recorremos las.
            print ("\033[0;32mAnalisis: \033[0;42m%s\033[0;m\033[0;32m ******* \033[0;m" %laip)
            info_ip(laip)
         
################################################################################
#  info_ip(ip)   Imprime informacion de la ip
################################################################################
def info_ip(laip):
    try:
        response = requests.get(f"http://ip-api.com/json/{laip}")
        data = response.json()
        
        print(f"[!] Pais: {data.get('country', 'N/A')}")
        print(f"[!] Codigo pais: {data.get('countryCode', 'N/A')}")
        print(f"[!] Region: {data.get('region', 'N/A')}")
        print(f"[!] Nombre región: {data.get('regionName', 'N/A')}")
        print(f"[!] Ciudad: {data.get('city', 'N/A')}")
        print(f"[!] Codigo postal: {data.get('zip', 'N/A')}")
        print(f"[!] Latitud: {data.get('lat', 'N/A')}")
        print(f"[!] Longitud: {data.get('lon', 'N/A')}")
        print(f"[!] Zona de hora: {data.get('timezone', 'N/A')}")
        print(f"[!] ISP: {data.get('isp', 'N/A')}")
        print(f"[!] Organización: {data.get('org', 'N/A')}")
        print(f"[!] AS: {data.get('as', 'N/A')}")

        try:
            print("\nHostname: %s" % socket.gethostbyaddr(laip)[0])
        except socket.herror:
            print("")


    except Exception as e:
        print(f"[!] Error obteniendo informacion: {e}")
        return None




    

################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)
