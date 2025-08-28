#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  VolcadoTAP.py: Vuelca información de ficheros TAP, usados en los emuladores 
#                 de ZXSpectrum
#                 Solo un parametro indica el fichero .TAP y nos da los bloques 
#                 cabecera que encuentra, programas grabados normalmente.
#                 Si indicamos dos, el segundo sera el programa del que deseamos 
#                 realizar un volcado.
#                 Volcados:
#                    SAVE "Basic"    Programa Basic
#                    SAVE "bytes" CODE ini,long   Bytes
#                    SAVE "MatrizN" DATA b(),long   Datos de una matriz numerica
#                    SAVE "MatrizA" DATA b$(),long   Datos de una matriz caracter
#
#  Historico:
#     - 25 Agosto 2025	V1:	Creación.
#     - 28 Agosto 2025	V1.01:	Se mejora el volcado de Basic, obteniendo la longitud de solo BASIC del par2.
#
#  Librerias
################################################################################
import sys
import os
############ TOKENS Basic del ZXSpectrum BASIC (165 - 255)
TOKENS = {
    165: "RND", 166: "INKEY$", 167: "PI", 168: "FN", 169: "POINT",
    170: "SCREEN$", 171: "ATTR", 172: "AT", 173: "TAB", 174: "VAL$",
    175: "CODE", 176: "VAL", 177: "LEN", 178: "SIN", 179: "COS",
    180: "TAN", 181: "ASN", 182: "ACS", 183: "ATN", 184: "LN",
    185: "EXP", 186: "INT", 187: "SQR", 188: "SGN", 189: "ABS",
    190: "PEEK", 191: "IN", 192: "USR", 193: "STR$", 194: "CHR$",
    195: "NOT", 196: "BIN", 197: "OR", 198: "AND", 199: "<=",
    200: ">=", 201: "<>", 202: "LINE", 203: "THEN", 204: "TO",
    205: "STEP", 206: "DEF FN", 207: "CAT", 208: "FORMAT", 209: "MOVE",
    210: "ERASE", 211: "OPEN #", 212: "CLOSE #", 213: "MERGE", 214: "VERIFY",
    215: "BEEP", 216: "CIRCLE", 217: "INK", 218: "PAPER", 219: "FLASH",
    220: "BRIGHT", 221: "INVERSE", 222: "OVER", 223: "OUT", 224: "LPRINT",
    225: "LLIST", 226: "STOP", 227: "READ", 228: "DATA", 229: "RESTORE",
    230: "NEW", 231: "BORDER", 232: "CONTINUE", 233: "DIM", 234: "REM",
    235: "FOR", 236: "GO TO", 237: "GO SUB", 238: "INPUT", 239: "LOAD",
    240: "LIST", 241: "LET", 242: "PAUSE", 243: "NEXT", 244: "POKE",
    245: "PRINT", 246: "PLOT", 247: "RUN", 248: "SAVE", 249: "RANDOMIZE",
    250: "IF", 251: "CLS", 252: "DRAW", 253: "CLEAR", 254: "RETURN", 255: "COPY",
}

def main(argv):

    print("VolcadoTAP (c) 2025 www.pinguytaz.net")

    if len(argv) < 2 or len(argv) > 3: # Parametros erroneos
        print ("Uso: python VolcadoTAP.py.py <FicheroTAP> [<FicheroTAP>]")
        return -1
    else:
         if len(argv) == 2: 
            ficheroTAP = argv[1] 
            ficheroCinta = ""
            print(f"      Bloques existentes en {ficheroTAP}      ")
            print(f"----------------------------------------------")
         if len(argv) == 3: 
            ficheroTAP = argv[1] 
            ficheroCinta = argv[2]

    # Realizamos el recorrido por los bloques del fichero .TAP
    # <0-1>Longitud <2>Flag tipo <3-xx> Datos del bloque <xx+1>Checksum
    info_cabecera = {}  # Inicializacion vacia
    tipo = -1
    with open(ficheroTAP, 'rb') as f:
        bloque_index = 0
        while True:   # Leemos todos los bloques que se encuentran en el fichero.
            longitud_bytes = f.read(2)  # Leemos los dos primeros bytes que nos dan la longitud del bloque en BigEndian
            if len(longitud_bytes) < 2:
                break
                #print("Lectura de bloque incorrecta")
                #return -1
    
            # Leemos el bloque
            longitud = int.from_bytes(longitud_bytes, 'little')  # Longitud del bloque convertimos valor
            bloque = f.read(longitud)  # Leemos tantos bytes como indica que es el bloque
            if len(bloque) < longitud: # Si no logramos leer todos esos bytes es un archivo incompleto.
                 print(f"Bloque {bloque_index}: archivo incompleto o corrupto.")
                 return -1

            # Cogemos datos del bloque siempre
            if bloque[0] == 0x00:    #byte 00 indica cabecera solo damos info de este
                 tipo_bloque = "Cabecera"
                 tipo, info_cabecera = leer_cabecera(bloque)
            if bloque[0] == 0xFF:    #byte FF indica Datos
                 tipo_bloque = "Datos"

            if ficheroCinta == "": #  Se pide un volcado de información de los bloques 
                 # Damos info de bloques cabecera
                 print(f"{bloque_index} {tipo_bloque}, Longitud={longitud} bytes")
                 if bloque[0] == 0x00:    #byte 00 indica cabecera solo damos info de este
                      print(f"\tNombre: {info_cabecera.get('nombre')}")
                      print(f"\tTipo: {info_cabecera.get('tipo')}")
                      print(f"\tLongitud bloque datos: {info_cabecera.get('longitud')}")
                      # Informacion particular de cada bloque
                      if tipo == 0:   # Información Programa Basic
                           if info_cabecera.get('par1') <= 32768:    # No tenemos autoinicio
                                print(f"\tSAVE {info_cabecera.get('nombre')} LINE: {info_cabecera.get('par1')}")
                           else:
                                print(f"\tSAVE {info_cabecera.get('nombre')}")
                      elif tipo == 1:   # Matriz numerica
                           print(f"\tSAVE {info_cabecera.get('nombre')} DATA n()")
                      elif tipo == 2:   # IMatriz alfanumerica
                           print(f"\tSAVE {info_cabecera.get('nombre')} DATA c$()")
                      elif tipo == 3:   # Infoirmación CODE
                          if info_cabecera['par1'] == 16384 and info_cabecera['longitud'] == 6912:
                               print(f"\tSAVE {info_cabecera.get('nombre')} SCREEN$ (origen 16384 y longitud 6912)")
                               #print(f"\tSCREEN$ ({info_cabecera.get('par1')}, {info_cabecera.get('longitud')})")
                          else:
                               print(f"\tSAVE {info_cabecera.get('nombre')} CODE {info_cabecera.get('par1')},{info_cabecera.get('longitud')}")
                               #print(f"\tCODE {info_cabecera.get('par1')}, {info_cabecera.get('longitud')}")
                      else: print(f"Tipo de bloque {tipo} desconocido")
            else:
                if ficheroCinta == info_cabecera.get('nombre') and bloque[0] == 0xFF:   # Es un bloque de datos al que informar
                    # Segun el tipo de grabación indicada por el bloque cabecera tomamos una u otra información
                    if tipo == 0:  # Prog Basic y variables    SAVE "programa"
                        print(f"Programa BASIC: {info_cabecera.get('nombre')} en fichero: {ficheroTAP} ")
                        print(f"-----------------------------------------------------------------------")
                        print(f"Long bloque: {len(bloque)} longitud {info_cabecera.get('longitud')} lonsinvar {info_cabecera.get('par2')}")
                        volcadoBasic(bloque, info_cabecera.get('par2'), info_cabecera.get('par1'))
                    elif tipo == 1:  # Matriz numerica     SAVE "matrices" DATA b()   Array de numeros 
                        print(f"Datos de una matriz numerica: {info_cabecera.get('nombre')} en fichero: {ficheroTAP} ")
                        print(f"-------------------------------------------------------------------------------------")
                        volcadoMatrizN(bloque)
                    elif tipo == 2:  # Matriz caracteres  SAVE "matriz$" DATA b$()
                        print(f"Datos de una matriz Alfanumerica: {info_cabecera.get('nombre')} en fichero: {ficheroTAP} ")
                        print(f"--------------------------------------------------------------------------------------")
                        volcadoMatrizA(bloque)
                    elif tipo == 3:  # SAVE "bytes" CODE 16384,6912  SAVE "pantalla" SCREEN$    Bytes
                         print(f"Volcamos los bytes de: {info_cabecera.get('nombre')} en fichero: {ficheroTAP} NOTA: <CHAR> si no imprimible .(COD)")
                         print(f"-----------------------------------------------------------------------------------------------")
                         volcadoBytes(bloque,info_cabecera.get('par1'),info_cabecera.get('longitud'))
                    else:  # Segun Especificación ZXSpectrum 48K solo son de 0-3
                         print(f" Tipo {tipo}-->{info_cabecera.get('tipo')} de: {info_cabecera.get('nombre')} fichero: {ficheroTAP} no implementado")

            bloque_index += 1

############################################ Funciones  ###############################

##############################################################################################
# leer_cabecera(bloque) Lee un bloque cabecera y retorna el tipo y la información de esta
# Los bloques cabeceras tiene 17 bytes
# <1> Tipo de datos  0-ProgBasic, 1-Datos, 2-Caracteres, 3-CODE (16384,6912 seria SCREE$) 4-Array 5-String
# <2-11> Nombre programa son 10 bytes y se rellena con espacios 
# <12-13>   Longitud 
# <14-15>  Parametro 1
#   En programa Basic si menor o igual a 32768  se grabo con LINE e indica la linea de inicio
#   En CODE indica el inicio de carga
# <16-17>  Parametro 2
#   Longitud del programa sin variables
##############################################################################################
def leer_cabecera(bloque):
    tipo = bloque[1]
    
    info_extra = {}
    info_extra['nombre'] = bloque[2:12].decode('ascii').strip()
    info_extra['longitud'] = int.from_bytes(bloque[12:14], 'little')
    info_extra['par1'] = int.from_bytes(bloque[14:16], 'little')
    info_extra['par2'] = int.from_bytes(bloque[16:18], 'little')
    if tipo == 0:  # Prog Basic y variables    SAVE "programa"
         info_extra['tipo'] = "Programa Basic y variables"

    if tipo == 1:  # Matriz numerica     SAVE "matrices" DATA b()   Array de numeros 
         info_extra['tipo'] = "Matriz numerica"

    if tipo == 2:  # Matriz alfanumerica  SAVE "matriz$" DATA b$()
         info_extra['tipo'] = "Matriz caracteres"

    if tipo == 3:  # SAVE "bytes" CODE 16384,6912  SAVE "pantalla" SCREEN$    Bytes
         info_extra['tipo'] = "Bytes"   
         if info_extra['par1'] == 16384 and info_extra['longitud'] == 6912:
              info_extra['tipo'] = "SCREEN$"      # Tipo Especial de CODE, carga pantalla

    #########  Estan definidos en algunos sitios pero el ZXSpectrum no los graba
    if tipo == 4:  # Array 
         info_extra['tipo'] = "Array"
    if tipo == 5:  # String
         info_extra['tipo'] = "String"

    return tipo, info_extra


##############################################################################################
# volcadoBytes(bloque,inicio,longitud)
#       Imprime un bloque tipo Byte, se pasa el bloque
#       <datos>
##############################################################################################
def volcadoBytes(bloque,inicio,longitud):
    # Nos saltamos el primero que es el FLAG
    for i in range(1, longitud+1 ):
         b = bloque[i]
         if 32 <= b <= 126:  # ASCII imprimible
              #print(f"{b}", end='')
              print(f"{chr(b)}({b})", end=' ')
         else:
              print(f".({b})", end='')
    
    #print("\n\n****VOLCADO CRUDO****")
    #for i in range(1, longitud+1 ):
         #b = bloque[i]
         #print(f"{chr(b)}",end='')
    #print("\n****FIN VOLCADO CRUDO****")
    print("\n")

##############################################################################################
# volcadoBasic(bloque, longSoloProg linea)  Se pasa el bloque, la longitud sin variables  y el posible numero de linea donde se debe iniciar
#       Imprime el listado Basic
#       Para Cada linea: <Numlinea(2)> <long linea (1)> <TOKENS, var, etc>  <0x0D fin linea>
#                        <Tabla de variables>
##############################################################################################
def volcadoBasic(bloque, longSoloProg, linea):
    if linea <= 32768:
         print(f"Volcado del programa BASIC que se iniciaria en la linea: {linea}")
    else:
         print("Volcado del programa BASIC")

    pos = 1
    while pos < longSoloProg:
        num_linea = (bloque[pos] *256 + bloque[pos+1])
        longitud = int.from_bytes(bloque[pos+2:pos+3], 'little')
        # Extraer contenido de la línea
        contenido = bloque[pos+4:pos+longitud+4]
        finlinea = bloque[pos+longitud+3]
        pos = pos + longitud +4
        
        # Imprimir  la linea
        contenidoTexto = convierteATexto(contenido)
        print(f"{num_linea} {contenidoTexto}")

##############################################################################################
# convierteATexto(contenido)  Genera el contenido de la linea a texto sustituyendo TOKENs
##############################################################################################
def convierteATexto(contenido):
     resultado = ""
     i = 0
     while i < len(contenido):
         txt = ""
         b = contenido[i]
         if b >= 165: 
              txt = TOKENS.get(b, f"<UNK:{b}>") + " "
         elif b >= 32  and b <= 126:
              txt =  chr(b)
         elif b == 14:    # Se imprimio un numero y se anula el valor por lo que anulamos 5 bytes
              i += 5
              txt = ""
         elif b<31:    # No imprimibles controles, como ENTER por ejemplo
              txt = ""
         else:
              txt += f"<NOIMP:{b}>"

         resultado += txt
         i += 1

     return resultado

##############################################################################################
# volcadoMatrizN(bloque)
#       Imprime datos de una matrtiz numerica grabada
##############################################################################################
def volcadoMatrizN(bloque):
    tamano = bloque[2]
    print(f"Volcado matriz numerica con dimension {tamano}")

    for i in range(4, len(bloque)-1,5):   # Empezamos en 4 para saltar el FLAG,1,long,0 y quitamos CRC
         numero = bloque[i:i+5]
         valor = convierteNumero(numero)
         #print(f"{numero}", end=', ')
         print(f"{valor}", end=', ')
       

##############################################################################################
# convierteNumero(datos)    Convertimos los 5 bytes pasados a numero, detectando signo y tipo
##############################################################################################
def convierteNumero(datos):
     valor = 0

     exponente = datos[0]
     # Primero miramos si es un entero o coma flotante mirando el exponente
     if exponente == 0: # Se trata de un numero entero
         signo = datos[1]
         valor = int.from_bytes(datos[2:4], 'little')
         if signo == 255:   # Realizamos complemento ya que es negativo
              valor = (65536 - valor) * -1
     else:   # Tiene exponente luego deberemos tratar como punto flotante
         # <1>Primer byte exponete, distinto de 0 que indicaria que es entero
         # <2-5> bytes de mantisa m[1-4]
         #      El bit mas significativo indica el signo (0 positivo y 1 negativo) m[1]&0x80 Recoge signo
         #      m[1]&0x7F Normalizamos para que la más significativa sea siempre 1. 
         #      N = 2^(exponente-128)*mantisa 
         
         signo = 1 if not (datos[1] & 0x80) else -1  # Bit de signo en msb del segundo byte
         # Quitar bit de signo del segundo byte para la mantisa
         bytes_mantisa = [
             datos[1] & 0x7F,
             datos[2],
             datos[3],
             datos[4]
         ]
         mantisa = 0.5  # El valor mínimo de mantisa
         # Calcular la mantisa sumando los bits restantes como fracciones
         for i in range(31):
             byte_idx = i // 8
             bit_idx = 7 - (i % 8)
             if bytes_mantisa[byte_idx] & (1 << bit_idx):
                 mantisa += 1 / (2 ** (i + 1))
         # Calcular valor final con la fórmula clásica
         valor = signo * (2 ** (exponente - 128)) * mantisa

     return valor

##############################################################################################
# volcadoMatrizA(bloque)
#       Imprime datos de una matrtiz alfanumerica grabada
##############################################################################################
def volcadoMatrizA(bloque):
    tamano = bloque[2]
    print(f"Volcado matriz de caracter con dimension {tamano}")

    for i in range(4, len(bloque)-1 ):   # Empezamos en 4 para saltar el FLAG,1,long,0 y quitamos CRC
         b = bloque[i]
         if 32 <= b <= 126:  # ASCII imprimible
              print(f"{chr(b)}", end='')
              #print(f"{chr(b)}({b})", end=' ')
         else:
              print(f".({b})", end='')



##############################################################################################
########## Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)
