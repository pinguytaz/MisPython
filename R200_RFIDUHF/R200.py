# -*- coding: utf-8 -*-
#########################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  R200.py: Clase para lector R200
#     Conexión UART 115200 8N1
#     Protocolo “R200 User Protocol v2.3.x” 
#         cabecera(AA), tipo, comando, longitud_payload(2bytes), payload y checksum fin(DD)
#     Placa: M100 26dBm V1.0 (UHF EPC C1G2/ISO 18000-6C, 840–960 MHz) ~19.5 a 26 dBm(pasos de 1.5db
#     V.Software: V2.3.5   
#     Fabricante: MagicRf
#
#     requiere el fichero .env con las variables de entorno
#
#  Historico:
#     - Noviembre 2025    V1: Creación 
#########################################################################
import serial
import time
from dataclasses import dataclass
from typing import List

import constantes
import utils


# Estructuras
@dataclass
class TagRead:
    rssi: bytes        
    pc: bytes        
    epc: bytes       
    crc: bytes       

@dataclass
class Firmware:
    dr: int = 8        # primer bit que sera uno indicando que es 8
    m: int = 1         # bit 2-3 sera 00 que es M=1 (01=2 10=4 11=8
    TRext: int = 1     # bit 4 sera 1 "pilot tone" 
    sel: int = 0       # 5-6   ALL=00 o 01 -SL=10 SL=11
    sesion: int = 0   # 7-8   00=S0 01=S1 10=S2 11=S3
    target: int = 1   # 9-10  0=A 1=B
    q: int = 4         # 11-14 Q



class R200():          # Clase para manejar Lector R200 (probado M100 26dBm)

    ################  Constructor #######################
    def __init__(
        self, port: str, velocidad: int = 115200, timeout: float = 1.0, debug: bool = False):


        self.debug = debug
        self.port = None

        # print(f"{port}, {velocidad}, {timeout}, {debug}")

        try:
            self.port = serial.Serial(
                port=port,
                baudrate=velocidad,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=timeout,
                write_timeout=timeout,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to open serial port: {e}")

    ################  Cierre puertos #######################
    def close(self) -> None:
        if self.port and self.port.is_open:
            self.port.close()
        else:
            raise RuntimeError("Serial port not opened")

    ####################################################################
    # hw_info    Nos da la información de HW, SW y fabricante
    ####################################################################
    def hw_info(self, debug: bool = False) -> str:
        # Obtiene la version de SW
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_INFO_MODULO, "00") 
        res = self.enviaComando(frame,debug)
        res_ascii = bytes((c if 32 <= c <= 126 else 46) for c in res).decode("ascii", errors="replace")
        vHW = res_ascii[6:-2]

        # Obtiene la version de SW
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_INFO_MODULO, "01") 
        res = self.enviaComando(frame,debug)
        res_ascii = bytes((c if 32 <= c <= 126 else 46) for c in res).decode("ascii", errors="replace")
        vSW = res_ascii[6:-2]

        # Obtiene fabricante
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_INFO_MODULO, "02") 
        res = self.enviaComando(frame,debug)
        res_ascii = bytes((c if 32 <= c <= 126 else 46) for c in res).decode("ascii", errors="replace")
        fabricante = res_ascii[6:-2]

        return vHW, vSW, fabricante
        
    #####################################################################
    # construyeFrame construye el frame se pasa tipo, comando y param.
    # AA <tipo> <comando> <len_hi> <len_lo> <params...> <crc> DD
    #####################################################################
    def construyeFrame(self, tipo: int, comando: int, parametros: str) -> bytes:
        if not (0 <= tipo <= 0xFF):
            raise ValueError("Tipo frame fuera de rango (0..255)")
        if not (0 <= comando <= 0xFF):
          raise ValueError("comando fuera de rango (0..255)")
    
        params = utils.parse_hex_bytes(parametros) if parametros else b""
        n = len(params)
        if n > 0xFFFF:
            raise ValueError("parametros  demasiado largo (max 65535)")
    
        len_hi = (n >> 8) & 0xFF
        len_lo = n & 0xFF
    
        core = bytes([tipo, comando, len_hi, len_lo]) + params
        crc = sum(core) & 0xFF

        return bytes([constantes.R200_FRAME_HEADER]) + core + bytes([crc, constantes.R200_FRAME_END])

    ####################################################################
    # enviaComando Envia el frame y recibe la información que devolvemos.
    ####################################################################
    def enviaComando(self, frame: bytes, debug: bool = False) -> bytes:
        # Limpia buffers
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        time.sleep(0.05)

        # Envía el comando
        n = self.port.write(frame)
        self.port.flush()
        if debug:
           print(f"TX ({n} bytes): {utils.hexdump(frame)}")
    
        # Lee respuesta: intenta varias ráfagas durante 1 segundo total
        deadline = time.time() + 1.0
        rx = bytearray()
        while time.time() < deadline:
            chunk = self.port.read(256)  # hasta 256 bytes por ráfaga
            if chunk:
                rx.extend(chunk)
            else:
                # breve pausa para siguiente intento
                time.sleep(0.02)
    
        if not rx:
            print("Sin respuesta dentro del tiempo de espera.")
        else:
            if debug: # Muestra en HEX y como ASCII imprimible
                print(f"RX ({len(rx)} bytes): {utils.hexdump(rx)}")
                safe_ascii = bytes((c if 32 <= c <= 126 else 46) for c in rx).decode("ascii", errors="replace")
                print(f"RX (ASCII): {safe_ascii}")
            return rx

    ####################################################################
    # get_Region Nos retorna la region 
    ####################################################################
    def get_Region(self,debug: bool = False) -> bytes:
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_GET_REGION, "") 
        res = self.enviaComando(frame,debug)
        return res[5]

    ####################################################################
    # set_Region Ponemos la region
    ####################################################################
    def set_Region(self, area: str, debug: bool = False) -> None:
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_SET_REGION, area) 
        self.enviaComando(frame,debug)


    ####################################################################
    # get_Canal Nos retorna La frecuencia de trabajo
    ####################################################################
    def get_Canal(self,debug: bool = False) -> bytes:
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_GET_CANAL, "") 
        res = self.enviaComando(frame,debug)
        return res[5]

    ####################################################################
    # set_Canal Ponemos la frecuencia de trabajo
    ####################################################################
    def set_Canal(self, frecuencia: str, debug: bool = False) -> None:
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_SET_CANAL, frecuencia) 
        self.enviaComando(frame,debug)


    ####################################################################
    # get_Potencia Obtiene la potencia
    ####################################################################
    def get_Potencia(self,debug: bool = False) -> bytes:
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_GET_POTENCIA, "") 
        res = self.enviaComando(frame,debug)
        
        return (int.from_bytes(res[5:7],byteorder="big", signed=False))/100

    ####################################################################
    # set_Potencia Ponemos la potencia de 10(03E8)-26
    ####################################################################
    def set_Potencia(self, potencia: int, debug: bool = False) -> None:
        potencia = potencia * 100
        dato = utils.hexdump(potencia.to_bytes(2, byteorder="big", signed=False))
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_SET_POTENCIA, dato) 
        self.enviaComando(frame,debug)


    ####################################################################
    # buscaTAG Realiza una lectura y retorna número encontrado
    ####################################################################
    def buscaTAG(self,debug: bool = False) -> list[TagRead]:
        Tags: list[TagRead] = []    # Lista Vacia
        localizadas = 0
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_SIMPLE_POLL, "") 
        res = self.enviaComando(frame,debug)
        if (res[1] == 0x02):    # Tenemos respuesta etiquetas
            tag = 0
            pos = 0
            while (pos < len(res)):
                # Trata respuesta 0x02 comando 0x22
                tag = tag +1
                longTAG = int.from_bytes(res[3:5],byteorder="big", signed=False) # Longitud de datos de la etiqueta pos 3-4
                if(debug):
                    print(f"------- Etiqueta {tag} -------------")
                    print(f"\t{utils.hexdump(res[pos+0:pos+longTAG+7])}") # Datos entero 0:AATipoCmdLong(2)LongTAG(2)ChecksumDD
                pos = pos + 5 # Nos situamos en RSSI[5]
                RSSI = res[pos:pos+1]
                pos = pos + 1 # Nos situamos en PC[6-7]
                PC = res[pos:pos+2]
                pos = pos + 2 # Nos situamos en Inicio de EPC[8-longTAG-5]
                EPC = res[pos:pos+longTAG-5]
                pos = pos + longTAG - 5 # Nos situamos en CRC[8+longTAG-5:+2
                CRC = res[pos:pos+2]
                pos = pos + 2  # posicionado en Checksum
                pos = pos + 2 # Saltamos Checksum y DD para situarnos al inicio de la otra

                # Cargamos lista con los datos recuperados
                Tags.append(TagRead(rssi=RSSI, pc=PC, epc=EPC, crc=CRC))

                if(debug):
                    print(f"\tRSSI: {utils.hexdump(RSSI[0:1])}\n\tPC: {utils.hexdump(PC)}\n\tEPC: {utils.hexdump(EPC)}\n\tCRC: {utils.hexdump(CRC)}")

            localizadas = tag
        elif (res[1] == 0x01 and res[2] == 0xFF and res[5] == 0x15):  # Error de lectura
            print(f"Error lectura inventario")
        else:
            print("Error desconocido al leer etiquetas")

        if(debug):
            print(f"Localizadas: {len(Tags)}") 
            
        return Tags


    ####################################################################
    # get_Firmware Recoge parametros formware
    ####################################################################
    def get_Firmware(self,debug: bool = False) -> bytes:
        firmware = Firmware()     # Lista Vacia
        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO,
                                     constantes.CMD_GET_FIRMWARE, "") 
        res = self.enviaComando(frame,debug)
        par1 = res[5]
        par2 = res[6]

        # Parametro DR: tasa division de datos y siempre 0 que es igual a 8 sino es 64/3
        DR = (par1 >> 7)  & 0b1 
        # Parametro M indice de modulación siempre 00 que es igual a 1, 01=2 10=4 11=8
        M=  (par1 >> 5)  & 0b11 
        # TRext presencia de tono piloto, siempre sera 1 que es usa tono piloto
        TRext =  (par1 >> 4)  & 0b1 
        
        # Los siguientes en nuestro firmware si que cambian
        # Sel: 2 bits banco/poblacion logica de tasg a inventariar 00/01=ALL 10=-SL 11=SL
        SEL = (par1 >> 2)  & 0b11 
        
        # Session: 2 bits mecanismo anticulisión y persistencia, tiempo que una etiqueta esta silenciada tras ser leida
        #  00=S0 01=S1 10=S2 11=S3
        SESS = par1  & 0b11    # Sin desplazamiento

        # target un bit flag A/B permite barre poblaciones en multiples pasadas sin reconsultar de inmediato 
        TARGET = (par2 >> 7) & 0b1

        # Q 4 bits que es el parametro de algoritmo de anticolision establece ranuras 2Q2Q colision/latencia Q=4 16 ranuras 
        Q = (par2 >> 3)  & 0b1111

        if(debug):
            print(f"DR:{DR} M:{M} TRext:{TRext} SEL:{SEL} SESS:{SESS} TARGET:{TARGET} Q:{Q}")

        firmware.dr = DR
        firmware.m  = M
        firmware.TRext = TRext
        firmware.sel = SEL
        firmware.sesion = SESS
        firmware.target = TARGET
        firmware.q = Q

        return firmware

    ####################################################################
    # set_Firmware Ponemos datos Firmware
    ####################################################################
    def set_Firmware(self, firmware: Firmware, debug: bool = False) -> None:
        # Generamos parametro
        #Los parametros DR, M y TRext van fijos en este firmware asi que da igual lo que venfa
        #if(debug):
        parametro = 0x01
        parametro = (parametro << 2) | firmware.sel   # Parametro sel
        parametro = (parametro << 2) | firmware.sesion   # Parametro sesion
        parametro = (parametro << 1) | firmware.target   # Parametro target
        parametro = (parametro << 4) | firmware.q   # Parametro q
        parametro = (parametro << 3) # Movemos 3 restantes sin uso.
        dato = utils.hexdump(parametro.to_bytes(2, byteorder="big", signed=False))
        if(debug):
            print(f"{parametro:b} ")
            print(f"{dato} ")

        frame = self.construyeFrame(constantes.FRAME_TIPO_COMANDO, constantes.CMD_SET_FIRMWARE, dato) 
        self.enviaComando(frame,debug)


