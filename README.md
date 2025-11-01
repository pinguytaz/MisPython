# MisPython

Script de Python, pequeños, que no podemos considerarlos un proyecto pero que nos pueden resolver problemas:

Practicas de python del curso CHEE.  

* **info_PDF.py**:  Script para obtener Metadatos de ficheros PDF, la idea es ir aumentando el tipo de ficheros.
* **info_DNS_WHO.py**:  Script para obtener información del DNS y WHO.
<BR>

Pequeñas herramientas que nos ayudan en nuestros estudios de Pentesting:  

* **busca_Usuario.py**: Nos permite realizar llamadas POST a una pagina introducióndo los usuarios de un fichero y una clave que normalmente no encontrara para localizar usuarios validos.  
<BR>  

**Ejemplo**  


*python busca_Usuario.py http://192.168.56.101/wp-login.php "Invalid username" log pwd usu.txt*

1.- Parametro primero es la URL con el formulario que solicita el usuario y clave.

2.- Segundo un String que aparece cuando el usuario no es valido.

3.- Variable del usuario.

4.- Variable de la clave que se auto rellena.

5.- Fichero con usuarios, es opcional y el fichero por defecto es DicUsu.txt

<BR>

* **info_IP.py**:  Script para obtener información de una lista de IPs y la nuestra.  Preparado para python3

* **VolcadoTAP.py**:  Script para ver información grabada en ficheros .TAP (Cinta ZXSpectrum) y descargar su contenido y sea programas, CODE, SCREE$, DATA (Matrices)

* **/R200_RFIDUHF**:  Clase R200 para la lectura del lector RFID-UHF modelo M100 26dBm 




