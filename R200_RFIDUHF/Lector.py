#!./rfid/bin/python
# -*- coding: utf-8 -*-
#########################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  Lector.py: Programa lectura de tarjetas, para probar el lector R200
#			requiere el fichero .env con las variables de entorno
#			PORT    Puerto por donde comunica
# Placa de pruebas: M100 26dBm V1.0 
#                   (UHF EPC C1G2/ISO 18000-6C, 840–960 MHz) ~19.5 a 26 dBm(pasos de 1.5db
#                   V.Software: V2.3.5     
#                   Fabricante: MagicRf
#                   Conexión UART 115200 8N1
# Comando Formato cabecera(AA), tipo, comando, longitud_payload(2bytes), payload y checksum fin(DD)
#
#  Historico:
#     - Noviembre 2025    V1: Creación 
#
# Previo:
#    python3 -m venv rfid    Genera entorno
#    source rfid/bin/activate        Activación del entorno Virtual
#    pip3 install -r requirements.txt     Instalación de dependencias en el entorno activado
#
#########################################################################
import sys            # Para recoger los parámetros
import os

from dotenv import load_dotenv

import R200         # Archivo clase lector R200
import constantes
import utils

def main(argv):
    load_dotenv()
    PORT = os.getenv('PORT')
    BAUD = int(os.getenv('BAUD'))
    TIMEOUT = float(os.getenv('TIMEOUT'))

    rfid = R200.R200(PORT,BAUD,TIMEOUT, debug=True)
    vHW, vSW, fabricante = rfid.hw_info()
    print(f"Hardware: {vHW} Versión: {vSW} Fabricante: {fabricante}")

    print(" ------------- Configuración -------------------")
    region = rfid.get_Region()
    if region != 0x03:
        print("Ponemos region Europea")
        rfid.set_Region("03") 
    region = rfid.get_Region()

    potencia = rfid.get_Potencia()
   
    #rfid.set_Potencia(20, True)
    potencia = rfid.get_Potencia()

    print(f"Región: {constantes.REGION.get(region,"Desconocida")} Potencia: {potencia} dBm")

    firmware = rfid.get_Firmware()

    if (firmware.dr == 0x00): DR="DR8"
    else: DR="DR 64/3" 
    if (firmware.m == 0x00): M="M1"
    elif (firmware.m == 0x01): M="M2"
    elif (firmware.m == 0x10): M="M4"
    elif (firmware.m == 0x11): M="M8"
    if (firmware.TRext == 0x00): TRext="Tono Piloto"
    else: TRext = "Sin tono"

    if (firmware.sel == 0x00): SEL="ALL"
    elif (firmware.sel == 0x01): SEL="ALL"
    elif (firmware.sel == 0x10): SEL="-SL"
    elif (firmware.sel == 0x11): SEL="SL"
    if (firmware.sesion == 0x00): SESS="S0"
    elif (firmware.sesion == 0x01): SESS="S1"
    elif (firmware.sesion == 0x10): SESS="S2"
    elif (firmware.sesion == 0x11): SESS="S3"
    if (firmware.target == 0x00): TARGET="A"
    else: TARGET = "B"
    Q = firmware.q

    print(f"Configuración: {DR} {M} {TRext} {SEL} {SESS} {TARGET} Q:{Q}")
    
    # Leemos tarjetas Pool Simple.
    Tags = rfid.buscaTAG()
    print(f"----- TAGs Localizados: {len(Tags)} -------")
    for idx, t in enumerate(Tags, start=1):
        dBrssi = int.from_bytes(t.rssi[0:1],byteorder="big", signed=False) -230
        print(f"Tag {idx}:\n\tRSSI: {dBrssi}dBm\n\tPC: {utils.hexdump(t.pc)}\n\tEPC: {utils.hexdump(t.epc)}\n\tCRC: {utils.hexdump(t.crc)}")


####################################################################
# getFrecuencia  Nos da la frecuencia segun la region y el canal
####################################################################
def getFrecuencia(region, canal):
    if (region == 0x01):  # China 900MHz
        return canal*0.25+920.125 
    elif (region == 0x02): # US
        return canal*0.5+902.25
    elif (region == 0x03): # EU
        return canal*0.2+865.1
    elif (region == 0x04): # China 800MHz
        return canal*0.25+840.125
    elif (region == 0x06): # Korea
        return canal*0.2+917.1


####################################################################
# getCanal  Nos da el canal segun frecuencia y region
####################################################################
def getCanal(region, frecuencia):
    if (region == 0x01):  # China 900MHz
        return int((frecuencia-920.125)/0.25)
    elif (region == 0x02): # US
        return int((frecuencia-902.25)/0.5)
    elif (region == 0x03): # EU
        return int((frecuencia-865.1)/0.2)
    elif (region == 0x04): # China 800MHz
        return int((frecuencia-840.125)/0.25)
    elif (region == 0x06): # Korea
        return int((frecuencia-917.1) /0.2)

################# Lanzamiento de la funcion principal ###################
if __name__ == "__main__":
    main(sys.argv)
