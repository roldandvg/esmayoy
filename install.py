# -*- coding: utf-8 -*-

"""
@note: Script de instalación del Proyecto Socio Tecnológico Esmayoy
"""
import sys
import os
import getpass

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

def verDep():
    """
    @note: Función verifica las dependencias necesarias para la instalación del sistema Esmayoy
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt","dos","ce"):
        os.system("CLS")
    print "%sVerificando existencia de la librería GnuPG...%s\n" % (colorPrint('negrita','Blue'),colorPrint('reset'))
    gpg = os.system("gpg --version")
    print "\n%sVerificando existencia del servidor de base de datos PostgreSQL...%s\n" % (colorPrint('negrita','Blue'),colorPrint('reset'))
    postgre = os.system("psql --version")
    
    try:
        print "\n%sVerificando existencia de la librería python-imaging...%s\n" % (colorPrint('negrita','Blue'),colorPrint('reset'))
        import PIL.Image
        pil = PIL.Image.VERSION
    except:
        pil=""
    
    print "\n"
    
    if gpg==0 or postgre==0 or pil=="":
        GnuPG=""
        PostgreSQL=""
        pilimage=""
        if gpg!=0:
            GnuPG = "\n- GnuPG"
        if postgre!=0:
            PostgreSQL = "\n- PostgreSQL"
        if pil=="":
            pilimage="\n- python-imaging"
        
        if GnuPG!="" or PostgreSQL!="" or pilimage!="": 
            raw_input("%sSu sistema no cuenta con los prerequisito mínimos para la instalación del PST ESMAYOY.\nDebe instalar la(s) siguiente(s) dependencia(s):%s%s%s\n\nPresione <ENTER> para continuar..." % (colorPrint('normal','Red'),GnuPG,PostgreSQL,colorPrint('reset')))
            instalar = raw_input("%sDesea instalar las dependencias necesaria para ejecutar el Proyecto Esmayoy [s/n]? %s" % (colorPrint('normal','Blue'),colorPrint('reset')))
            if instalar=="s" or instalar=="S":
                aptget=os.system("apt-get install gnupg python-imaging postgresql")
                if aptget!=0:
                    raw_input("%sLas dependencias no pudieron ser instaladas. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(aptget),colorPrint('reset')))
                else:
                    raw_input("%sInstalación de dependencia(s) exitosa. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
        else:
            raw_input("%sDependencias comprobadas satisfactoriamente. Presione <ENTER> para continuar...%s" % (colorPrint('negrita','Green'),colorPrint('reset')))
    else:
        raw_input("%sDependencias comprobadas satisfactoriamente. Presione <ENTER> para continuar...%s" % (colorPrint('negrita','Green'),colorPrint('reset')))
    return menuppal()

def fwkDjango(continuar=False):
    """
    @note: Función que permite instalar el framework utilizado en el desarrollo del sistema Esmayoy
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name in ("nt","dos","ce"):
        raw_input("%sSistema Operativo actualmente no soportado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        return False
    elif os.name == "posix":
        #instalación del framework django
        frameworkinstaled = os.system("python -c 'import django'")
        if frameworkinstaled!=0:
            admin = raw_input("Para instalar el framework Django debe poseer permisos administrativos del sistema. Es usted un usuario Administrador [s/n]? ")
            if admin=="s" or admin=="S":
                raw_input("%sSe instalará el framework Django. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
                os.system("tar -xzvf extapps/django-1.2.5.tar.gz")
                os.system("su && cd django-1.2.5 && python setup.py install")
                frameworkinstaled = os.system("python -c 'import django'")
                os.system("rm -r django-1.2.5")
                if frameworkinstaled!=0:
                    raw_input("%sError al instalar el framework Django. Posible causa: %s%s. Presione <ENTER> para continuar..." % str(colorPrint('normal','Red'),frameworkinstaled,colorPrint('reset')))
                else:
                    raw_input("%sEl framework Django se instaló correctamente. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
            else:
                raw_input("Debe comunicarse con un usuario administrador que le permita ejecutar este proceso de instalación.\nPresione <ENTER> para continuar...")
        else:
            raw_input("%sEl framework Django ya se encuentra instalado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
    return menuppal()
        
def libDajax():
    """
    @note: Función que permite instalar la librería AJAX para Django (DAJAX)
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name in ("nt","dos","ce"):
        raw_input("%sSistema Operativo actualmente no soportado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        return False
    elif os.name == "posix":
        libdajaxinstaled = os.system("python -c 'import dajax'")
        if libdajaxinstaled!=0:
            admin = raw_input("Para instalar el framework Django debe poseer permisos administrativos del sistema. Es usted un usuario Administrador [s/n]? ")
            if admin=="s" or admin=="S":
                raw_input("%sSe instalará la librería dajax. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
                os.system("tar -xzvf extapps/dajax-0.7.5.0.tar.gz")
                os.system("su && cd dajax-0.7.5.0 && python setup.py install")
                libdajaxinstaled = os.system("python -c 'import dajax'")
                os.system("rm -r dajax-0.7.5.0")
                if libdajaxinstaled!=0:
                    raw_input("%sError al instalar la librería dajax. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(libdajaxinstaled),colorPrint('reset')))
                else:
                    raw_input("%sLa librería Dajax se instaló correctamente. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
            else:
                raw_input("Debe comunicarse con un usuario administrador que le permita ejecutar este proceso de instalación.\nPresione <ENTER> para continuar...")
        else:
            raw_input("%sLa librería Dajax ya se encuentra instalada. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
        return menuppal()
    
def libpyCaptcha():
    """
    @note: Función que permite instala la librería para el uso de captcha (pyCaptcha)
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name in ("nt","dos","ce"):
        raw_input("%sSistema Operativo actualmente no soportado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        return False
    elif os.name == "posix":
        libpycaptchainstaled = os.system("python -c 'import Captcha'")
        if libpycaptchainstaled!=0:
            admin = raw_input("Para instalar el framework Django debe poseer permisos administrativos del sistema. Es usted un usuario Administrador [s/n]? ")
            if admin=="s" or admin=="S":
                raw_input("%sSe instalará la librería pyCaptcha. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
                os.system("tar -xzvf extapps/pycaptcha-0.4.tar.gz")
                os.system("su && cd pycaptcha-0.4 && python setup.py install")
                libpycaptchainstaled = os.system("python -c 'import Captcha'")
                os.system("rm -r pycaptcha-0.4")
                if libpycaptchainstaled!=0:
                    raw_input("%sError al instalar la librería pycaptcha. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(libpycaptchainstaled),colorPrint('reset')))
                else:
                    raw_input("%sLa librería pyCaptcha se instaló correctamente. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
            else:
                raw_input("Debe comunicarse con un usuario administrador que le permita ejecutar este proceso de instalación.\nPresione <ENTER> para continuar...")
        else:
            raw_input("%sLa librería pyCaptcha ya se encuentra instalada. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
        return menuppal()
            
def libGnuPG():
    """
    @note: Función que permite instalar la librería de cifrado python-gnupg
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name in ("nt","dos","ce"):
        raw_input("%sSistema Operativo actualmente no soportado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        return False
    elif os.name == "posix":
        libpygpginstaled = os.system("python -c 'import gnupg'")
        if libpygpginstaled!=0:
            admin = raw_input("Para instalar el framework Django debe poseer permisos administrativos del sistema. Es usted un usuario Administrador [s/n]? ")
            if admin=="s" or admin=="S":
                raw_input("%sSe instalará la librería para python GnuPG. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
                os.system("tar -xzvf extapps/python-gnupg-0.3.1.tar.gz")
                os.system("cd python-gnupg-0.3.1 && python setup.py install")
                libpygpginstaled = os.system("python -c 'import gnupg'")
                os.system("rm -r python-gnupg-0.3.1")
                if libpygpginstaled!=0:
                    raw_input("%sError al instalar la librería para python GnuPG. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(libpygpginstaled),colorPrint('reset')))
                else:
                    raw_input("%sLa librería python-gnupg se instaló correctamente. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
            else:
                raw_input("Debe comunicarse con un usuario administrador que le permita ejecutar este proceso de instalación.\nPresione <ENTER> para continuar...")
        else:
            raw_input("%sLa librería python-gnupg ya se encuentra instalada. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),colorPrint('reset')))
        return menuppal()
    
def createDB():
    """
    @note: Función que permite crear la estructura de la base de datos a ser utilizada por el proyecto Esmayoy
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    if os.name in ("nt","dos","ce"):
        raw_input("%sSistema Operativo actualmente no soportado. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        return False
    elif os.name == "posix":
        debian_psycopg2 = os.system("apt-get install python-psycopg2")
        if debian_psycopg2!=0:
            raw_input("%sError al instalar la librería de conexión a base de datos PostgreSQL. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(debian_psycopg2),colorPrint('reset')))
            return menuppal()
        
        servidorbd = raw_input("%sIndique el nombre o dirección IP del servidor de Base de Datos. Si no se especifica se usara el servidor por defecto (localhost): " % colorPrint('normal','Blue'))
        puertobd = raw_input("Indique el puero de conexión al servidor de Base de Datos. Si no se especifica se usara el puerto por defecto (5432): ")
        nombrebd = raw_input("Indique el nombre de la Base de Datos: ")
        usuariobd = raw_input("Indique el nombre del usuario de Base de Datos: ")
        print colorPrint('reset')
        if servidorbd=="":
            servidorbd="localhost"
        if puertobd=="":
            puertobd="5432"
            
        crearbd = os.system("createdb %s -h %s -p %s -U %s -O %s -E 'UTF-8' 'Base de Datos para el Sistema Esmayoy, para la gestión de procesos del Departamento de Admisión, Registro y Control de Estudio (D.A.R.C.E.) de los Programas Nacionales de Formación (P.N.F.)'" % (nombrebd,servidorbd, puertobd,usuariobd,usuariobd))
        if crearbd!=0:
            raw_input("%sError al crear la base de datos. La Base de Datos indicada ya existe o no fue posible crearla. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(crearbd),colorPrint('reset')))
            return menuppal()
        raw_input("%sBase de Datos %s creada correctamente. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),nombrebd,colorPrint('reset')))
        passbd = getpass.getpass("%sIndique nuevamente la contraseña de conexión a la base de datos: %s" % (colorPrint('normal','Blue'),colorPrint('reset')))
        raw_input("%sCreando estructura de la Base de Datos. Presione <ENTER> para continuar. Por favor espere, este procedimiento puedo tomar algún tiempo...%s" % (colorPrint('normal','Blue'),colorPrint('reset')))
        archcifrar = open("apps/configuracion/servidorbd.txt","w")
        archcifrar.write("%s\n%s\n%s\n%s\n%s" % (nombrebd, usuariobd, passbd, servidorbd, puertobd))
        archcifrar.close()
        os.system("cp apps/configuracion/servidorbd.txt apps/configuracion/servidorbd.txt.backup")
        syncdb = os.system("cd apps/configuracion && python crearkey.py && cd ../.. && python manage.py syncdb")
        if syncdb!=0:
            raw_input("%sError al crear la estructura de la Base de Datos. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(syncdb),colorPrint('reset')))
        else:
            raw_input("%sEstructura de la Base de Datos creada correctamente. Solo el usuario [%s] puede ejecutar la aplicación. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Green'),os.getlogin(),colorPrint('reset')))
        return menuppal()

def installAll():
    """
    @note: Función que permite realizar el proceso de instalación del proyecto Esmayoy en un solo paso
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    #asignar todos los permisos a las carpetas tmp, logs y uploads
    chmod = os.system("chmod 777 -R tmp logs uploads")
    if chmod!=0:
        raw_input("%sError al conceder permisos de escritura y lectura para las carpetas tmp/, logs/ y uploads/. Posible causa: %s. Presione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),str(chmod),colorPrint('reset')))
        return menuppal()
    
    for i in range(6):
        menuppal(i+1)
    """
    verDep()
    fwkDjango()
    libDajax()
    libpyCaptcha()
    libGnuPG()
    createDB()
    """
    return menuppal()

def menuppal(opcion=0):
    """
    @note: Función qeneral que muestra el menú de instalación del sistema Esmayoy
    @license: GPLv2
    @author: Ing. Roldan D. Vargas G.
    @organization: Universidad Politécnica Territorial de Mérida (U.P.T.M.)
    @status: BETA
    """
    while int(opcion)<1 or int(opcion)>8:
        borrarPantalla()
        menu = "==================================\n"
        menu+= "Menú de Instalación\n"
        menu+= "==================================\n\n"
        menu+= "(1) Verificar dependencias\n"
        menu+= "(2) Instalar framework Django\n"
        menu+= "(3) Instalar librería Dajax\n"
        menu+= "(4) Instalar librería pyCaptcha\n"
        menu+= "(5) Instalar librería python-gnupg\n"
        menu+= "(6) Crear estructura BD\n"
        menu+= "(7) Instalación completa\n"
        menu+= "(8) Salir\n"
        menu+= "==================================\n"
        print colorPrint('normal','Blue')+menu
        opcion= raw_input("indique la opción de instalación: "+colorPrint('negrita','Blue'))
        print colorPrint('reset')
        if int(opcion)<1 or int(opcion)>8:
            raw_input("\n%sopción inválida, pulse <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
            
    eventos = {
        1: verDep,
        2: fwkDjango,
        3: libDajax,
        4: libpyCaptcha,
        5: libGnuPG,
        6: createDB,
        7: installAll,
    }
    
    try:
        if not eventos[int(opcion)]():
            if int(opcion)==8:
                raw_input("%sSaliendo de la instalación del sistema Esmayoy. Pulse <ENTER> para continuar...%s" % (colorPrint('normal','Magenta'),colorPrint('reset')))
                borrarPantalla()
            sys.exit(1)
        else:
            borrarPantalla()
            eventos[int(opcion)]()
            borrarPantalla()
    except KeyError:
        raw_input("%sSaliendo de la instalación del sistema Esmayoy. Pulse <ENTER> para continuar...%s" % (colorPrint('normal','Magenta'),colorPrint('reset')))
        borrarPantalla()
        sys.exit(1)
         

if __name__ == '__main__':
    borrarPantalla()
    if (len(sys.argv)>1):
        for i in range(1,len(sys.argv)):
            if sys.argv[i]=="-m" or sys.argv[i]=="--man":
                man = open("docs/MAN.txt")
                lineas = man.readlines()
                for linea in lineas:
                    if "NOMBRE" in linea or "SINOPSIS" in linea or "DESCRIPCION" in linea or "OPCIONES" in linea or "-h" in linea or "-m" in linea or "-p" in linea or "-l" in linea or "-v" in linea or "-c" in linea:
                        print "%s%s%s" % (colorPrint('negrita','Black'),linea,colorPrint('reset'))
                        continue;
                    elif "[opciones]" in linea:
                        iniO=linea.find("[")
                        linea=linea[:iniO+1]+colorPrint('subrayado','Black')+linea[iniO+1:len(linea)-2]+colorPrint('reset')+linea[len(linea)-2]
                    
                    print linea
                man.close()
            elif sys.argv[i]=="-h" or sys.argv[i]=="--help":
                help = open("docs/HELP.txt")
                lineas = help.readlines()
                for linea in lineas:
                    print linea
                help.close()
            elif sys.argv[i]=="-p" or sys.argv[i]=="--pasos-install":
                pasos = open("docs/how-to.txt")
                lineas = pasos.readlines()
                for linea in lineas:
                    print linea
                pasos.close()
            elif sys.argv[i]=="-l":
                leame = open("docs/LEAME.txt")
                lineas = leame.readlines()
                for linea in lineas:
                    print linea
                leame.close()
            elif sys.argv[i]=="-v" or sys.argv[i]=="--VERSION":
                version = open("docs/VERSION.txt")
                print version.readline()
                version.close()
            elif sys.argv[i]=="-c" or sys.argv[i]=="--copyright":
                licencia = open("docs/LICENCIA.txt")
                lineas = licencia.readlines()
                for linea in lineas:
                    print linea
                licencia.close()
        raw_input("Presione <ENTER> para salir...")
        borrarPantalla()
        sys.exit(1)
        
    
    """if os.environ['USER']!="root":
        raw_input("%sPara instalar la aplicación debe poseer privilegios administrativos.\nDebe ejecutar el script de instalación como usuario administrador.\nPresione <ENTER> para continuar...%s" % (colorPrint('normal','Red'),colorPrint('reset')))
        borrarPantalla()
        sys.exit(1)"""
    
    borrarPantalla()
    menuppal()
else:
    raw_input("Este módulo no puede ser importado.\nSi desea conocer el funcionamiento de la instalación del proyecto Esmayoy, por favor ingrese el siguiente comando desde una consola:\npython install.py -h\nPulse <ENTER> para continuar...")
    sys.exit(1)
