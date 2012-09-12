#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.models import Carrera
from academico.models import Anualidad_Tri_Carrera
from unidadcurricular.models import Modulo_Curricular
from planta.academica.models import Profesor
from planificacion.forms import FormPlanificacion, FormPlanificacionUnidad
from planificacion.models import Planificacion, Planificacion_Unidad
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("planificacion")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('planificacion/index.html', {'planificacion':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarPlanificacion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("planificacion")
    registros = cargarDatosConsulta(Planificacion.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormPlanificacion(request.POST, auto_id="%s")
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            fregistro = form.cleaned_data['fregistro']
            observaciones = form.cleaned_data['observaciones']
            anualidad_trimestre = form.cleaned_data['anualidad_trimestre']
            carrera = form.cleaned_data['carrera']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                anualtri = Anualidad_Tri_Carrera.objects.get(pk=anualidad_trimestre)
                carr = Carrera.objects.get(pk=carrera)
                if modificar=="":
                    pla = Planificacion(descripcion=descripcion, fregistro=fregistro, anualidad_trimestre=anualtri, carrera=carr)
                else:
                    pla = Planificacion.objects.get(pk=modificar)
                    pla.descripcion = descripcion
                    pla.fregistro = fregistro
                    pla.anualidad_trimestre = anualtri
                    pla.carrera = carr
                
                pla.usuarioreg = usr
                pla.save()
                
                registros = cargarDatosConsulta(Planificacion.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Planificación") % (request.user, logreg))
                return render_to_response('planificacion/regplanificacion.html', {'form':FormPlanificacion(auto_id="%s"), 'exito':True, 'planificacion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Planificación por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planificacion/regplanificacion.html', {'form':form, 'errores':e.message, 'planificacion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Planificación por el usuario [%s]") % request.user)
            return render_to_response('planificacion/regplanificacion.html', {'form':form, 'errores':'formulario inválido', 'planificacion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Planificación desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planificacion/regplanificacion.html', {'form':FormPlanificacion(auto_id="%s"),  'planificacion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarPlanificacionUnidad(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("planificacionunidad")
    registros = cargarDatosConsulta(Planificacion_Unidad.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormPlanificacionUnidad(request.POST, auto_id="%s")
        if form.is_valid():
            seccion = form.cleaned_data['seccion']
            cant_alumnos = form.cleaned_data['cant_alumnos']
            cupo = form.cleaned_data['cupo']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            planificacion = form.cleaned_data['planificacion']
            profesor = form.cleaned_data['profesor']
            modulo = form.cleaned_data['modulo']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                plan = Planificacion.objects.get(pk=planificacion)
                prof = Profesor.objects.get(pk=profesor)
                modcurr = Modulo_Curricular.objects.get(pk=modulo)
                if modificar=="":
                    plau = Planificacion_Unidad(seccion=seccion, cant_alumnos=cant_alumnos, cupo=cupo, estatus=estatus, planificacion=plan,
                                                profesor=prof, modulo=modcurr)
                else:
                    plau = Planificacion_Unidad.objects.get(pk=modificar)
                    plau.seccion = seccion
                    plau.cant_alumnos = cant_alumnos
                    plau.cupo = cupo
                    plau.estatus = estatus
                    plau.planificacion = plan
                    plau.profesor = prof
                    plau.modulo = modcurr
                    
                plau.usuarioreg = usr
                plau.save()
                
                registros = cargarDatosConsulta(Planificacion_Unidad.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Planificación por Unidad Curricular") % (request.user, logreg))
                return render_to_response('planificacion/regplanunidad.html', {'form':FormPlanificacionUnidad(auto_id="%s"), 'exito':True, 'planificacion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Planificación por Unidad Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planificacion/regplanunidad.html', {'form':form, 'errores':e.message, 'planificacion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Planificación por Unidad Curricular por el usuario [%s]") % request.user)
            return render_to_response('planificacion/regplanunidad.html', {'form':form, 'errores':'formulario inválido', 'planificacion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Planificación por Unidad Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planificacion/regplanunidad.html', {'form':FormPlanificacionUnidad(auto_id="%s"), 'planificacion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})