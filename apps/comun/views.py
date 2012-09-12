#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from comun.constantes import TIEMPO_SESSION
from comun.models import Imagen
from os.path import abspath, dirname, join
from esmayoy.settings import PATH
from django.utils import simplejson
from django.http import HttpResponse

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('base/index.html', {'username':request.user})

@login_required
def auditoriaLogs(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('auditoria/eventos.html', {'logs':True, 'username':request.user})

@login_required
def auditoriaLogsAcademico(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/academico.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'academico', 'username':request.user})

@login_required
def auditoriaLogsConfiguracion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/configuracion.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'configuracion', 'username':request.user})

@login_required
def auditoriaLogsHorario(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/horario.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'horario', 'username':request.user})

@login_required
def auditoriaLogsInscripcion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/inscripcion.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'inscripcion', 'username':request.user})

@login_required
def auditoriaLogsInstitucion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/institucion.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'institucion', 'username':request.user})

@login_required
def auditoriaLogsPlanificacion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/planificacion.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'planificacion', 'username':request.user})

@login_required
def auditoriaLogsPlantaAca(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/planta_academica.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'planta.academica', 'username':request.user})

@login_required
def auditoriaLogsPlantaFis(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/planta_fisica.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'planta.fisica', 'username':request.user})

@login_required
def auditoriaLogsSeguridad(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/seguridadusr.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'seguridad', 'username':request.user})

@login_required
def auditoriaLogsUnidadCurr(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/unidadcurricular.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'unidadcurricular', 'username':request.user})

@login_required
def auditoriaLogsGeneral(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    archivo = open(join(PATH, "logs")+"/registros.log")
    logs = archivo.readlines()
    archivo.close()
    return render_to_response('auditoria/visorlogs.html', {'logs':logs, 'modulo':'general', 'username':request.user})

@login_required
def setImagen(request):
    print request.POST
    try:
        if 'image' in file:
            """imagen = request.FILES['foto']
            Imagen.imagefield.save(imagen.name, image)"""
            img = Imagen(imagen=request.POST['foto'])
            img.save()
    
    except Exception, e:
        print e
    #if request.is_ajax():
    return