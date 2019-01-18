!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
#  Fco. Javier Rodriguez Navarro 
#
#  info_DNS_WHO.py:  Recoleccion de información de los DNS, Whois y servidores 
#                    de correo, recibe dos parametros que son los dominios a
#                    investigar.
#
#  Historico:
#     - 2 Enero 2019   V1:  Creación como practica CHEE
#
#  Librerias
#       DNSPython 	http://www.dnspython.org/
#       pythonwhois	http://cryto.net/pythonwhois/ (pip install pythonwhois)
################################################################################
import sys
import dns.resolver
import pythonwhois

def main(argv):
   dom = []

   if len(argv) != 3: # Tienen que llegar dos parametros.
      print "Uso: python info_DNS_WHO.py dominio1 dominio2"
   else:
      for dominio in argv[1:]:   # Recorremos los dos dominios de los parametros.
         print '\033[0;32mAnalisis: \033[0;42m%s\033[0;m\033[0;32m ******* \033[0;m' % dominio

         dom = info_dns(dominio)   # Información DNS y Whois de los dominios mx

         for domMX in dom:    # Recorremos para busca WHOIS los dominios encontrados en MX
            info_whois(domMX)      # Se busca la informacion WHOIS de los dominios MX encontrados.

         #info_whois(dominio)  # Información del dominio.
         print '\n\n'
    
################################################################################
#  info_dns(dominio)   Imprime informacion referente a DNS
################################################################################
def info_dns(dominio):
   reg = ['A', 'AAAA', 'CNAME', 'NS', 'MX', 'SOA','TXT','PTR']
   dominios = []
   print '\n\033[4;34mDNS\033[0;m'

   for r in reg:
      print '\033[0;33m%s: \033[0;m' % r
      try:
         respuesta = dns.resolver.query(dominio, r)

         for datos in respuesta:
            if r == "SOA":
               print '   Version: %s ' % datos.serial
               print '   Dominio maestro; %s Responsable: %s' % (datos.mname, datos.rname)
               print '   Actualización: %s sg.  reintentos: %s sg.' % (datos.refresh, datos.retry)
               print '   Caducidad: %s sg.  TTL-Minimo: %ssg. ' % (datos.expire, datos.minimum)
            elif r == "MX":
               print '   Dominio: %s Preferencia: %s' % (datos.exchange,datos.preference)
               
               nombre = datos.exchange.split(3)[1].to_text(True) 
               if not (nombre in dominios):
                  dominios.append(nombre)  #Recoje los dominios de los correos para luego el Whois
            else:
               print "   %s " % datos.to_text()
 
         print '\033[0;33m:%s \033[0;m\n' % r
      except dns.resolver.NoAnswer:
         print "\033[1;31mNo existe registro %s\n\033[0;m" % r
      except:
         print "\033[1;31mError inesperado en %s %s\n\033[0;m" % (r,sys.exc_info()[0])
   return dominios

################################################################################
#  info_whois(dominio)   Imprime informacion referente a WHOIS
################################################################################
def info_whois(dominio):
   print '\n\033[4;34mWHOIS de Registro MX %s\033[0;m' % dominio

   respuesta = pythonwhois.get_whois(dominio,True)


   if respuesta.has_key('id'): print '\033[4;34mID registro de dominio:\033[0;m %s' % respuesta['id'][0]
   if respuesta.has_key('registrar'): print '\033[4;34mRegistrador:\033[0;m %s' % respuesta['registrar'][0]
   if respuesta.has_key('whois_server'): print '\033[4;34mWHOI de nombre:\033[0;m %s\n' % respuesta['whois_server'][0]

   if respuesta.has_key('updated_date'): print '\033[4;34mFecha actualizacion:\033[0;m %s' % respuesta['updated_date']
   if respuesta.has_key('creation_date'): print '\033[4;34mFecha Creacion:\033[0;m %s' % respuesta['creation_date']
   if respuesta.has_key('expiration_date'): print '\033[4;34mFecha caducidad:\033[0;m %s' % respuesta['expiration_date']

   if respuesta.has_key('status'): 
      print '\n\033[4;34mEstado:\033[0;m\n' 
      for i in respuesta['status']:
         print "   %s" % i

   if respuesta.has_key('contacts'): 
      print '\n\033[4;34mContacto:\033[0;m \n' 
      print '   Administrador: %s' % respuesta['contacts']['admin']
      print '   Resp. Tecnico: %s' % respuesta['contacts']['tech']
      print '   Registro: %s' % respuesta['contacts']['registrant']
      if respuesta.has_key('emails'): print '   Correo: %s' % respuesta['emails'][0]

   if respuesta.has_key('nameservers'): 
      print '\n\033[4;34mservidores de nombre:\033[0;m \n' 
      for i in respuesta['nameservers']:
         print "   %s" % i

   
   print '\n       \033[4;34mRespuesta WHOIS\033[0;m \n' 
   for i in respuesta.get('raw'):
      print i


################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)

