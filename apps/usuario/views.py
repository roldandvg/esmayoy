# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.models import User, Permission
from django.utils.translation import ugettext as _
from usuario.forms import FormAcceso, FormSegIngAlumn, FormPermisoUsuario, FormModContrasenha, FormUsuario
from usuario.models import Seguridad_Ingreso_Alumnos
from institucion.models import Carrera_Sede
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import INTENTOS_ACCESO, TIEMPO_SESSION
from datetime import *
from Captcha.Visual.Tests import PseudoGimpy
import random, time, tempfile
import hashlib
import time
import os
import logging

logger = logging.getLogger("usuario")

def _generateId(solution):
    """
    @note: Función que permite generar un identificador aleatorio
    @note: Se modificó la librería sha por hashlib por estar descontinuada en versiones posteriores a python 2.5
    @author: David McNab <david@rebirthing.co.nz> | http://svn.navi.cx/misc/trunk/pycaptcha/contrib/ezcaptcha.py
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna una cadena de texto única
    """
    random.seed("%d%s" % (os.getpid(), time.ctime()))
    return hashlib.sha1("%s%s%s" % (settings.SECRET_KEY, solution, random.random())).hexdigest()[:10]

def generarCaptcha():
    """
    @note: Función que permite generar la imagen del captcha y su correspondiente hash para su verificación
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna una lista con las variables a ser utilizadas para la generación del captcha
    """
    random.seed("%d%s" % (os.getpid(), time.ctime()))
    g = PseudoGimpy()
    g.__init__()
    answer = g.solutions[0]
    id = _generateId(answer)
    i = g.render()
    captchaFile = os.path.join(settings.PATH, "tmp")+"/"+id+"Image.png"
    i.save(captchaFile)

    img = "<img src='/tmp/"+id+"Image.png' border='0' width='140px' height='40px' />  <img src='/media/images/base/reload.png' width='20px' height='20px' style='cursor:pointer' title='"+_(u"Pulse sobre el botón si desea recargar la imagen")+"' onclick='Dajax.usuario_reloadCaptcha();' />"
    SALT = settings.SECRET_KEY[:20]
    imgtext = answer
    imghash = hashlib.sha1(SALT+imgtext).hexdigest()

    Lista = [img,imghash,id]
    #logging.info(u"Nueva imagen de captcha generada")
    return Lista

def inicio(request):
    """
    @note: Función que permite mostrar la página de inicio del sistema
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna la página de inicio del sistema
    """
    return render_to_response('usuario/index.html', {'seguridad':True, 'username':request.user})

def acceso(request):
    """
    @note: Función que permite mostrar el formulario de acceso a la aplicación
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna un mensaje de error si el usuario no puede ser logueado en el sistema, en caso contrario ejecuta la función de inicio de la aplicación 
    """
    now = datetime.now()
    datosCaptcha = generarCaptcha()
    contador=0
    if request.method == "POST":
        if (request.POST['usuario']!="" or request.POST['contrasenha']!="" or (request.POST['usuario']=="" and request.POST['contrasenha']=="")) and not 'contador_acceso' in request.session:
            request.session['contador_acceso'] = "0"
        else:
            contador = int(request.session['contador_acceso']) + 1
            request.session['contador_acceso'] = str(contador)
        form = FormAcceso(data=request.POST, auto_id="%s", request=request)
        archivo = os.path.join(settings.PATH, "tmp")+"/"+request.POST['tmp']+"Image.png"
        if form.is_valid():
            request.session['contador_acceso'] = "0"
            if User.objects.filter(username=str(request.POST['usuario'])):
                usr = User.objects.get(username=str(request.POST['usuario']))
            else:
                usr = False

            if usr and usr.is_active:
                Usuario = authenticate(username=str(request.POST['usuario']), password=str(request.POST['contrasenha']))
                login(request, Usuario)
                logger.info(_(u"El usuario [%s] a ingresado al sistema desde la IP [%s]") % (usr,request.META['REMOTE_ADDR']))
                os.remove(archivo) #Elimina el archivo temporal de la imagen del captcha
                request.session.set_expiry(300) #Tiempo de expiración de la sesión
                return HttpResponseRedirect(urlresolvers.reverse("comun.views.inicio"))
            else:
                return render_to_response('usuario/acceso.html', {'form': form, 'usrexiste': "el usuario no existe o esta inactivo",'imagen': datosCaptcha[0], 'imghash': datosCaptcha[1], 'valor': datosCaptcha[2]})
        else:
            if int(request.session['contador_acceso'])>(INTENTOS_ACCESO-1):
                del request.session['contador_acceso']
                if User.objects.filter(username=str(request.POST['usuario'])):
                    usr = User.objects.get(username=str(request.POST['usuario']))
                    usr.is_active=False
                    usr.save()
                    logger.warning(_(u"El usuario [%s] intento acceder al sistema desde la IP [%s] con más de 3 intentos. El suario fue bloqueado") % (usr, request.META['REMOTE_ADDR']))
            else:
                logger.warning(_(u"Error al introducir datos en el formulario de acceso"))
            return render_to_response('usuario/acceso.html', {'form': form,'imagen': datosCaptcha[0], 'imghash': datosCaptcha[1], 'valor': datosCaptcha[2]})
    else:
        logger.info(_(u"Acceso al sistema desde la IP [%s]") % request.META['REMOTE_ADDR'])
        return render_to_response('usuario/acceso.html', {'form': FormAcceso(auto_id="%s"),'imagen': datosCaptcha[0], 'imghash': datosCaptcha[1], 'valor': datosCaptcha[2]})
    
@login_required
def salir(request):
    """
    @note: Función que permite terminar la sesión del usuario
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna la URL de inicio del sistema
    """
    user = request.user
    if user.is_authenticated():
        logger.info(_(u"El usuario [%s] salio del sistema") % user)
        logout(request)
    return HttpResponseRedirect(settings.LOGOUT_URL)

@login_required
@transaction.commit_on_success
def registrarSeguridadIngAlumnos(request):
    """
    @note: Función que permite registrar los parámetros de seguridad aplicados a usuarios para la Inscripción de Alumnos
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna el formulario de registro de seguriudad para la Inscripción de Alumnos 
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    now = datetime.now()
    prerequisito = cargarRequisitosRegistro("seguridadingalumno")
    registros = cargarDatosConsulta(Seguridad_Ingreso_Alumnos.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormSegIngAlumn(request.POST, auto_id="%s")
        if form.is_valid():
            validar_seg = str2bool(form.cleaned_data['validar_seg'])
            validar_fecha = str2bool(form.cleaned_data['validar_fecha'])
            finicio = form.cleaned_data['finicio']
            ffinal = form.cleaned_data['ffinal']
            validar_cantalumn = str2bool(form.cleaned_data['validar_cantalumn'])
            cant_alumnos = form.cleaned_data['cant_alumnos']
            usuario = form.cleaned_data['usuario']
            carrsed = form.cleaned_data['carrsed']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                USR = User.objects.get(pk=int(usuario))
                cs = Carrera_Sede.objects.get(pk=carrsed)
                print USR
                if modificar=="":
                    contador = 0
                    seg = Seguridad_Ingreso_Alumnos(validar_seg=validar_seg, validar_fecha=validar_fecha, validar_cantalumn=validar_cantalumn,
                                                    contador_cantidad=contador, fecha_operacion=now, carrera_sede=cs,username=USR)
                else:
                    seg = Seguridad_Ingreso_Alumnos.objects.get(pk=modificar)
                    contador = int(seg.contador_cantidad) + 1
                    seg.validar_seg = validar_seg
                    seg.validar_fecha = validar_fecha
                    seg.validar_cantalumn = validar_cantalumn
                    seg.contador_cantidad = contador
                    seg.fecha_operacion = now
                    seg.carrera_sede = cs
                    seg.username = USR
                if finicio!="":
                    seg.finicio = finicio
                if ffinal!="":
                    seg.ffinal = ffinal
                if cant_alumnos!="":
                    seg.cant_alumnos = cant_alumnos
                seg.usuarioreg = usr
                seg.save()
                
                registros = cargarDatosConsulta(Seguridad_Ingreso_Alumnos.objects.all(),int(request.GET.get('page', '1')))
                #Variable que permite identificar que registros realizó el usuario para mostrarlo en el archivo log del sistema
                datosing = "validar_seg=%s, validar_fecha=%s, validar_cantalumn=%s, contador_cantidad=%s, fecha_operacion=%s, usuario=%s,carrera_sede=%s" % (str(validar_seg), str(validar_fecha), str(validar_cantalumn), str(contador), str(now), str(request.user), str(cs))
                logger.info(_(u"El usuario [%s] %s datos de seguridad para el ingreso de alumnos desde la IP [%s]. Los datos que %s son: %s") % (request.user, logreg, request.META['REMOTE_ADDR'], logreg, datosing))
                return render_to_response('usuario/regsegingalumn.html', {'form':FormSegIngAlumn(auto_id="%s"),'seguridad':True, 'exito':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de seguridad para el ingreso de alumnos por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e))
                return render_to_response('usuario/regsegingalumn.html', {'form':form, 'errores':e, 'seguridad':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Seguridad de Ingreso de Alumnos por el usuario [%s]") % request.user)
            return render_to_response('usuario/regsegingalumn.html', {'form':form, 'errores':'formulario inválido', 'seguridad':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingreso al módulo de Registro de Seguridad para Inscripción de Alumnos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('usuario/regsegingalumn.html', {'form':FormSegIngAlumn(auto_id="%s"), 'seguridad':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarUsuario(request):
    """
    @note: Función que permite registrar permisos de usuario
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna el formulario de registro de permisos de usuario
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(User.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormUsuario(request.POST, auto_id="%s")
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            correo = form.cleaned_data['correo']
            contrasenha = form.cleaned_data['contrasenha']
            activo = str2bool(form.cleaned_data['activo'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                now = datetime.now()
                if modificar=="":
                    usr = User(username=usuario, first_name=nombre, last_name=apellido, email=correo, is_active=activo, date_joined=now, last_login=now, fecha_modpass=now)
                else:
                    usr = User.objects.get(pk=modificar)
                    usr.username = usuario
                    usr.first_name = nombre
                    usr.last_name = apellido
                    usr.email = correo
                    usr.is_active = activo
                    usr.date_joined = now
                    usr.last_login = now
                    usr.fecha_modpass = now
                usr.set_password(contrasenha)
                usr.save()
                
                registros = cargarDatosConsulta(User.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s un nuevo usuario con el login [%s] desde la IP [%s]") % (request.user, logreg, usuario,request.META['REMOTE_ADDR']))
                return render_to_response('usuario/regusuario.html', {'form':FormUsuario(auto_id="%s"), 'seguridad':True, 'username':request.user, 'exito':True, 'registros':registros})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de usuario por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, e.message))
                return render_to_response('usuario/regusuario.html', {'form':form, 'seguridad':True, 'username':request.user, 'registros':registros})
        else:
            logger.warning(_(u"Errores al procesar el formulario de registro de usuario"))
            return render_to_response('usuario/regusuario.html', {'form':form, 'seguridad':True, 'username':request.user, 'registros':registros})
    else:
        logger.info(_(u"El usuario [%s] ingreso al módulo de registro de usuarios desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('usuario/regusuario.html', {'form':FormUsuario(auto_id="%s"), 'seguridad':True, 'username':request.user, 'registros':registros})
    
@login_required
@transaction.commit_on_success
def registrarPermisosUsuario(request):
    """
    @note: Función que permite registrar permisos de usuario
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna el formulario de registro de permisos de usuario
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    if request.method=="POST":
        form = FormPermisoUsuario(request.POST, auto_id="%s")
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            permiso = form.cleaned_data['permiso']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                guardar = False
                usr = User.objects.get(pk=usuario)
                usr.user_permissions.clear()
                #PRIMERO COLOCAR UNA LINEA PARA ELIMINAR TODOS LOS PERMISOS ANTES DE AGREGAR NUEVOS
                for per in permiso:
                    usr.user_permissions.add(per)
                    guardar = True
                
                if guardar:
                    logger.info(_(u"El usuario [%s] asigno permisos al usuario [%s]") % (request.user, usr.username))
                    return render_to_response('usuario/regpermisos.html', {'form':FormPermisoUsuario(auto_id="%s"), 'exito':True, 'seguridad':True, 'username':request.user})
                else:
                    logger.info(_(u"El usuario [%s] no seleccionó permisos en el módulo de registro de permisos de usuario") % request.user)
                    return render_to_response('usuario/regpermisos.html', {'form':FormPermisoUsuario(auto_id="%s"), 'seguridad':True, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Ocurrió un error al registrar permisos de usuario por el usuario [%s]. Detalles del error: %s") % (request.user, e.message))
                return render_to_response('usuario/regpermisos.html', {'form':form, 'errores':e.message, 'seguridad':True, 'username':request.user})
        else:
            logger.warning(_(u"Errores al procesar el formulario de registro de permisos de usuario"))
            return render_to_response('usuario/regpermisos.html', {'form':form, 'errores':'formulario inválido', 'seguridad':True, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de registro de permisos de usuario desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('usuario/regpermisos.html', {'form':FormPermisoUsuario(auto_id="%s"), 'seguridad':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarModContrasenha(request):
    """
    @note: Función que permite mostrar el formulario de modificación de contraseñas
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@cenditel.gob.ve
    @return: Retorna el formulario de modificación de contraseñas
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    if request.method=="POST":
        form = FormModContrasenha(request.POST, auto_id="%s")
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            contrasenha = form.cleaned_data['contrasenha']
            contrasenhanva = form.cleaned_data['contrasenhanva']
            contrasenhaconfirm = form.cleaned_data['contrasenhaconfirm']
            try:
                usr = Usuario.objects.get(username=usuario)
                usr.set_password(contrasenhanva)
                usr.save()
                logger.info(_(u"El usuario [%s] modificó su contraseña") % request.user)
                return render_to_response('usuario/regmodpass.html', {'form':FormModContrasenha(auto_id="%s"), 'exito':True, 'seguridad':True, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al modificar contraseña del usuario [%s]. Detalles del error: %s") % (request.user, e.message))
                return render_to_response('usuario/regmodpass.html', {'form':form, 'errores':e.message, 'seguridad':True, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de modificación de contraseñas"))
            return render_to_response('usuario/regmodpass.html', {'form':form, 'errores':'formulario inválido', 'seguridad':True, 'username':request.user})
    else:
        usuario = request.user
        logger.info(_(u"El usuario [%s] ingresó al módulo de modificación de contraseñas desde la IP [%s]") % (usuario,request.META['REMOTE_ADDR']))
        return render_to_response('usuario/regmodpass.html', {'form':FormModContrasenha(auto_id="%s"), 'usuario':usuario, 'seguridad':True, 'username':request.user})