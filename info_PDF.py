#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
#  Fco. Javier Rodriguez Navarro 
#
#  info_PDF.py:  Programa que recoge todos los ficheros(PDF) del directorio 
#                actual, si van si parametros y sino el directorio marcado en 
#                el parametro y saca los metadatos de esos ficheros PDF.
#                La busqueda es no recursiva, si se quiere recursiva quitar Break.
#
#  Historico:
#     - 4 Enero 2019    V1: Creación para curso CHEE.
#
#  Librerias
#       PyPDF2		https://pythonhosted.org/PyPDF2/ (pip install PyPDF2
#
################################################################################
import sys
import os 
import datetime 
from PyPDF2 import PdfFileReader, PdfFileWriter

def main(argv):
   directorio = '.'
   ficheros = []   # Tendra los ficheros a analizar

   argumentos = len(argv)-1
   if argumentos > 1:
      print "Uso: python %s [directorio]" % argv[0]
      exit(-1)
   elif argumentos == 1:
      directorio = argv[1]


   # Recogemos los ficheros PDF del directorio y es sobre los que realizaremos analisis    
   for dirpath, dirnames, files in os.walk(directorio): 
      for nombre in files: # Recorremos ficheros
         ext = nombre.lower().rsplit('.', 1)[-1]
         if ext in ['pdf']:  
            ficheros.append(dirpath+os.path.sep+nombre)
      break;  ## Evita el recursivo  COmentando esta linea la busqueda es recursiva hacia abajo.

   # COmenzamos el analisis de los fichero
   for fichero in ficheros:
      campo = {}
      campo["Fichero"] = fichero # Nombre del fichero.

      pdfFile = PdfFileReader(file(fichero, 'rb'))  # Abrimos el fichero.
      campo["Paginas"] = pdfFile.getNumPages()
      campo["TamPagina"] = pdfFile.getPageLayout()

      docInfo = pdfFile.getDocumentInfo() # Diccionario con la informacion

      campo["Titulo"] = docInfo.get("/Title")
      campo["Autor"] = docInfo.get("/Author")
      campo["Resumen"] = docInfo.get("/Subject")
      campo["Claves"] = docInfo.get("/Keyword")

      if docInfo.get("/CreationDate") is not None:
         campo["FCreacion"] = docInfo.get("/CreationDate").get_original_bytes() # A Cadena 
      else:
         campo["FCreacion"] = ""

      if docInfo.get("/ModDate") is not None:
         campo["FModificacion"] = docInfo.get("/ModDate").get_original_bytes() # A Cadena  
      else:
         campo["FModificacion"] = ""

      campo["Aplicacion"] = docInfo.get("/Producer")
      campo["Creador"] = docInfo.get("/Creator")
   
      info_PDF(campo) # Imprime datos. 

################################################################################
#  info_PDF(docInfo) Imprime por pantalla la información recogida llega
#                    por parametro en un diccionario.
################################################################################
def info_PDF(docInfo):
   print "\033[4;32mMETADATOS fichero:\033[0;32m %s\033[0;m" % docInfo.get("Fichero")
   print "\033[4;34mTitulo:\033[0;m %s" % docInfo.get("Titulo")
   print "\033[4;34mAutor:\033[0;m %s" % docInfo.get("Autor")
   print "\033[4;34mResumen:\033[0;m %s" % docInfo.get("Resumen")
   print "\033[4;34mPalabras clave:\033[0;m %s" % docInfo.get("Claves")
   print "\033[4;34mNumero de paginas:\033[0;m %s\n" % docInfo.get("Paginas")

   if docInfo.get("FCreacion") != "":
      print "\033[4;34mFecha Creacion:\033[0;m %s" % fechaPDF(docInfo.get("FCreacion"))
   if docInfo.get("FModificacion") != "":
      print "\033[4;34mUltima Modificacion:\033[0;m %s\n" % fechaPDF(docInfo.get("FModificacion"))

   print "\033[4;34mAplicacion:\033[0;m %s" % docInfo.get("Aplicacion")
   print "\033[4;34mCreado:\033[0;m %s\n" % docInfo.get("Creador")


################################################################################
#  fechaPDF(fecha) Descompone formato de fecha PDF "D:YYYYMMDDHHmmSSOHH'mmOHH'mm"
#                  y retorna cadema "dd/mm/aaaa hh:mm"
################################################################################
def fechaPDF(fecha):
   
   #Fecha
   dia =  fecha[8:10]
   mes =  fecha[6:8]
   ano = fecha[2:6]
   #Hora:Min
   hora = fecha[10:12]
   minutos = fecha[12:14]
   segundos = fecha[14:16]

   res = dia+"/"+mes+"/"+ano+" "+hora+":"+minutos+":"+segundos
   return res


################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)

