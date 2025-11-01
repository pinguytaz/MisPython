# -*- coding: utf-8 -*-
#########################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  Constantes para la clase R200 de lectura del lector RFID-UHF M100 26dBm 
#
#  Historico:
#     - Noviempre 2025    V1: Creación 
#########################################################################
# Constantes del Frame Inicio, FIN y los tipos de envio o retornos.
R200_FRAME_HEADER = 0xAA
R200_FRAME_END = 0xDD
FRAME_TIPO_COMANDO = 0x00
FRAME_TIPO_RESPUESTA = 0x01
FRAME_TIPO_NOTIFICACION = 0x02

# Codigos de error
ERR_COMANDO = 0x17
ERR_FHSS_FAIL = 0x20
ERR_INVENTORY_FAIL = 0x15
ERR_ACCESS_FAIL = 0x16
ERR_READ_FAIL = 0x09
ERR_WRITE_FAIL = 0x10
ERR_LOCK_FAIL = 0x13
ERR_KILL_FAIL = 0x12

# Comandos
CMD_INFO_MODULO = 0x03
CMD_FALLO_EJECUCION = 0xFF
CMD_SET_REGION = 0x07    # Region de trabajo 
CMD_GET_REGION = 0x08  
CMD_SET_CANAL = 0xAB   # Canal de trabajo Frecuencia
CMD_GET_CANAL = 0xAA
CMD_GET_POTENCIA = 0xB7   #  Potencia de transmision
CMD_SET_POTENCIA = 0xB6   
CMD_GET_FIRMWARE = 0x0D  # Parametro Firmware
CMD_SET_FIRMWARE = 0x0E


### Comandos lectura Escritura Tarjetas
CMD_SIMPLE_POLL = 0x22    

CMD_MULTIPLE_POLL = 0x27      # Realiza el sondeo varias veces 0-65535
CMD_PARA_MULTIPLE_POLL = 0x28
CMD_SET_PARM_SELCCION = 0x0C
CMD_GET_PARM_SELCCION = 0x0B
CMD_SET_INTRUCCION_ENVIO_SELECT = 0x12

CMD_LEE_ETIQUETA = 0x39
CMD_ESCRIBE_ETIQUETA = 0x49
CMD_BLOQUEA_ETIQUETA = 0x82
CMD_KILL_TAG = 0x65


#################### No programados
CMD_SET_SALTO_AUTOMATICO_FRECUENCIAS = 0xAD # Pone 0xFF 0 quita 0x00 el salto frecuencia. FHSSON OFF
CMD_SET_CANALES_SALTO = 0xA9
CMD_SET_TRANSMISION_CONTINUA_CARRIER = 0xB0     # CW ON OFF
CMD_GET_PARAMETROS_DEMODULADOR = 0xF1   # Parametros demodulador
CMD_SET_PARAMETROS_DEMODULADOR = 0xF0   
CMD_TEST_SENAL_BLOQUEO_RF = 0xF2      # Bloqueo de señal
CMD_TEST_CANALES_RSSI = 0xF3                  # Test RSSI
CMD_CONTROL_IO_PORT = 0x1A       # Configuración puerto IO placa
CMD_MODULE_SLEEP = 0x17          # Modo Sleep
CMD_SET_MODULE_IDLE_SLEEP_TIME = 0x1D   # Tiempo dormido

###### Tablas codigos
# Region
REGION = {
           0x01: "China 900 Mhz",
           0x02: "US",
           0x03: "EU",
           0x04: "China 800 Mhz",
           0x06: "Korea",
        }

