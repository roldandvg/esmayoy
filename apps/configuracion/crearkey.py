# -*- coding: utf-8 -*-
"""
Archivo que permite generar un par de claves GPG para el Proyecto Socio Tecnológico ESMAYOY
Requerimientos:
gnupg <http://gnupg.org>
python-gnupg <http://code.google.com/p/python-gnupg/>
"""
#import sys
#sys.path.append('../../')
from gnupg import *
import time
import os
import sys

correo="admin@esmayoy.com"
gpg = GPG(gnupghome="/home/"+os.environ['USER']+"/") #Variable que obtiene la ruta de configuración por defecto de GnuPG

def colorPrint(formato,color='',fondo=False):
    codigo = chr(27) + "["
    
    if formato=='reset':
        return codigo+"0;39m"
    
    A = {0:'normal',1:'negrita',2:'diluir',3:'cursiva',4:'subrayado',5:'parpadeo lento',6:'parpadeo rápido',7:'negativo'}
    COLORC = {0:'Light Grey',1:'Light Red',2:'Light Green',3:'Light Yellow',4:'Light Blue',5:'Light Magenta',6:'Light Cyan',7:'White'}
    COLORN = {0:'Black',1:'Red',2:'Green',3:'Yellow',4:'Blue',5:'Magenta',6:'Cyan',7:'Gray'}
        
    for i in range(8):
        if formato==A[i]:
            F=str(i)+";"
        if color==COLORC[i]:
            if not fondo:
                C="3"+str(i)+"m"
            else:
                C="4"+str(i)+"m"
        elif color==COLORN[i]:
            if not fondo:
                C="9"+str(i)+"m"
            else:
                C="10"+str(i)+"m"
            
    return codigo+F+C

def borrarPantalla():
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt","dos","ce"):
        os.system("CLS")

def generar_pass():
    """
    @note: Función que permite generar una contraseña aleatoriamente
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna una cadena de texto de 20 carácteres con la contraseña aleatoria generada
    """
    import string
    from random import seed, choice

    seed("%d%s" % (os.getpid(), time.ctime()))

    letras = string.letters
    numeros = string.digits
    signos = string.punctuation

    newpass = ''.join(choice([choice(letras),choice(numeros),choice(signos)]) for x in range(20))

    return newpass


def cifrar(nomarchtxt, nomarchcrypt):
    """
    @note: Instrucciones que permiten cifrar un archivo
    """
    try:
        archivo = open(nomarchtxt, "rb")
        data = archivo.read()
        archfirmado = gpg.sign(data,keyid=correo)
        txtcifrado = gpg.encrypt(archfirmado.data,correo)
        archivo.close()
        archcifrado = open(nomarchcrypt,"w")
        archcifrado.write(txtcifrado.data)
        archcifrado.close()
        os.remove(nomarchtxt) #Elimina el archivo te texto plano
        print "El arcivo de conexión a la base de datos fue cifrado con éxito."
    except Exception, e:
        print "No ha sido posible cifrar el archivo de conexión a la Base de Datos. El error generado es: %s" % e
    
def importarKeys():
    try:
        gpg.import_keys("keys/privkey.asc").summary()
        gpg.import_keys("keys/pubkey.asc").summary()
        print 'Se importaron el par de claves'
    except Exception, e:
        print "El par de claves GPG del proyecto ESMAYOY no pudieron ser importadas. Detalles del error: %s" % e

if __name__ == '__main__':
    try:
        if (len(sys.argv)>1):
            for i in range(1,len(sys.argv)):
                if sys.argv[i]=="-m" or sys.argv[i]=="--man":
                    man = open("docs/manconf.txt")
                    lineas = man.readlines()
                    for linea in lineas:
                        if "NOMBRE" in linea or "SINOPSIS" in linea or "DESCRIPCION" in linea or "OPCIONES" in linea or "--help" in linea or "-m" in linea:
                            print "%s%s%s" % (colorPrint('negrita','Black'),linea,colorPrint('reset'))
                            continue;
                        elif "[opciones]" in linea:
                            iniO=linea.find("[")
                            linea=linea[:iniO+1]+colorPrint('subrayado','Black')+linea[iniO+1:len(linea)-2]+colorPrint('reset')+linea[len(linea)-2]
                    
                        print linea
                    man.close()
                    raw_input("Presione <ENTER> para salir...")
                    borrarPantalla()
                    sys.exit(1)
                elif sys.argv[i]=="--help":
                    help = open("helpconf.txt")
                    lineas = help.readlines()
                    for linea in lineas:
                        print linea
                    help.close()
                    raw_input("Presione <ENTER> para salir...")
                    borrarPantalla()
                    sys.exit(1)
                else:
                    if sys.argv[i][:2]=="-h" and sys.argv[i][2:]!="":
                        servidor = sys.argv[i][2:]
                    if sys.argv[i][:2]=="-P" and sys.argv[i][2:]!="":
                        puerto = sys.argv[i][2:]
                    if sys.argv[i][:2]=="-b" and sys.argv[i][2:]!="":
                        basedatos = sys.argv[i][2:]
                    if sys.argv[i][:2]=="-u" and sys.argv[i][2:]!="":
                        usuario = sys.argv[i][2:]
                    if sys.argv[i][:2]=="-p" and sys.argv[i][2:]!="":
                        passwd = sys.argv[i][2:]
        else:
            print "No se han especificado los datos para la conexión de la Base de datos. Utilice la opción --help para obtener ayuda sobre estos datos."
            sys.exit(1)

        
        """
        @note: Instrucciones que permiten generar un par de llaves GnuPG
        """
        #params = {'Key-Type': 'RSA','Key-Length': 1024,'Subkey-Type': 'ELG-E','Subkey-Length': 2048,'Name-Comment': 'Proyecto Socio-Tecnológico para el Departamento de Admisión, Registro y Control de Estudio (D.A.R.C.E.) del Programa Nacional de Formación (PNF)',}
        params = {'key_type': "RSA", 'key_length': 1024, 'subkey_type': "ELG-E", 'subkey_length': 2048, 'name_comment': "Proyecto Socio-Tecnológico para el Departamento de Admisión, Registro y Control de Estudio (D.A.R.C.E.) del Programa Nacional de Formación (PNF)", 'name_real': "PST ESMAYOY", 'name_email':correo}
        #params['Passphrase'] = generar_pass() #descomentar en caso de asignarle una contraseña a la clave privada
        input_key = gpg.gen_key_input(**params)
        keys = gpg.gen_key(input_key)
        """
        @note: Instrucciones que permiten cifrar un archivo
        """
        data = "%s\n%s\n%s\n%s\n%s" % (servidor, puerto, basedatos, usuario, passwd)
        archfirmado = gpg.sign(data,keyid=correo)
        txtcifrado = gpg.encrypt(archfirmado.data,correo)
    
        archcifrado = open("databasesign.txt","w")
        archcifrado.write(txtcifrado.data)
        archcifrado.close()
        """
        @note: Exporta la clave pública
        """
        ascii_public  = gpg.export_keys(correo)
        pubkey = open("keys/pubkey.asc","w")
        pubkey.write(ascii_public)
        pubkey.close()
    
        """
        @note: Exporta la clave privada
        """
        ascii_private = gpg.export_keys(correo, True)
        privkey = open("keys/privkey.asc","w")
        privkey.write(ascii_private)
        privkey.close()

        print 'Se generó un nuevo par de claves para ESMAYOY'
    except Exception, e:
        print "El par de claves no se pudo generar. Detalles del error: %s" % e

    sys.exit(1)
