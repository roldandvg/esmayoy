#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
from inscripcion.forms import FormEstatusInscanual, FormEstatusInsctrimestral, FormInscripcionAnual, FormInscripcionTrimestral, FormHito
from inscripcion.models import Estatus_Inscanual, Estatus_Insctrimestral, Inscripcion_Anual, Historico_Inscanual, Hito, Historico_Hito, Inscripcion_Trimestral, Historico_Insctrimestral
from academico.models import Anualidad, Trimestre, Alumno
from unidadcurricular.models import Unidad_Curricular, Modulo_Curricular
import logging

logger = logging.getLogger("inscripcion")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('inscripcion/index.html', {'inscripcion':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarEstatusInscAnual(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Estatus_Inscanual.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormEstatusInscanual(request.POST, auto_id="%s")
        if form.is_valid():
            estatus = form.cleaned_data['estatus']
            descripcion = form.cleaned_data['descripcion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    eia = Estatus_Inscanual(estatus=estatus, descripcion=descripcion)
                else:
                    eia = Estatus_Inscanual.objects.get(pk=modificar)
                    eia.descripcion = descripcion
                eia.usuarioreg = usr
                eia.save()
                
                registros = cargarDatosConsulta(Estatus_Inscanual.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos en Estatus de Inscripción Anual") % (request.user, logreg))
                return render_to_response('inscripcion/regestatusinscanual.html', {'form':FormEstatusInscanual(auto_id="%s"), 'exito':True,  'inscripcion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al % datos en Estatus de Inscripción Anual por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, e.message))
                return render_to_response('inscripcion/regestatusinscanual.html', {'form':form, 'errores':e.message,  'inscripcion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Estatus de Inscripión Anual por el usuario [%s]") % request.user)
            return render_to_response('inscripcion/regestatusinscanual.html', {'form':form, 'errores':'formulario inválido',  'inscripcion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Estatus de Inscripción Anual desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('inscripcion/regestatusinscanual.html', {'form':FormEstatusInscanual(auto_id="%s"),  'inscripcion':True, 'registros':registros, 'username':request.user})    

@login_required
@transaction.commit_on_success
def registrarEstatusInscTrimestral(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Estatus_Insctrimestral.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormEstatusInsctrimestral(request.POST, auto_id="%s")
        if form.is_valid():
            estatus = form.cleaned_data['estatus']
            descripcion = form.cleaned_data['descripcion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    eit = Estatus_Insctrimestral(estatus=estatus, descripcion=descripcion)
                else:
                    eit = Estatus_Insctrimestral.objects.get(pk=modificar)
                    eit.descripcion = descripcion
                eit.usuarioreg = usr
                eit.save()
                
                registros = cargarDatosConsulta(Estatus_Insctrimestral.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos en el Estatus de Inscripción Trimestral") % (request.user, logreg))
                return render_to_response('inscripcion/regestatusinsctrim.html', {'form':FormEstatusInsctrimestral(auto_id="%s"), 'exito':True, 'inscripcion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos en el Estatus de Inscripción Trimestral por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('inscripcion/regestatusinsctrim.html', {'form':form, 'errores':e.message, 'inscripcion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Estatus de Inscripción Trimestral por el usuario [%s]") % request.user)
            return render_to_response('inscripcion/regestatusinsctrim.html', {'form':form, 'errores':'formulario inválido', 'inscripcion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Estatus de Inscripción Trimestral desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('inscripcion/regestatusinsctrim.html', {'form':FormEstatusInsctrimestral(auto_id="%s"),  'inscripcion':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarInscripcionAnual(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("inscanual")
    registros = cargarDatosConsulta(Inscripcion_Anual.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormInscripcionAnual(request.POST, auto_id="%s")
        if form.is_valid():
            seccion = form.cleaned_data['seccion']
            nota = form.cleaned_data['nota']
            asistencia = form.cleaned_data['asistencia']
            estatus = form.cleaned_data['estatus']
            cedula = form.cleaned_data['cedula']
            anualidad = form.cleaned_data['anualidad']
            unidad = form.cleaned_data['unidad']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                est = Estatus_Inscanual.objects.get(pk=estatus)
                alumno = Alumno.objects.get(cedula=cedula)
                an = Anualidad.objects.get(pk=anualidad)
                und = Unidad_Curricular.objects.get(pk=unidad)
                if modificar=="":
                    insa = Inscripcion_Anual(seccion=seccion, nota=nota, asistencia=asistencia, estatus=est, alumno=alumno, 
                                             anualidad=an, unidad=und)
                else:
                    insa = Inscripcion_Anual.objects.get(pk=modificar)
                    insa.seccion = seccion
                    insa.nota = nota
                    insa.asistencia = asistencia
                    insa.estatus = est
                    insa.anualidad = an
                    insa.unidad = und
                
                insa.usuarioreg = usr
                insa.save()
                #INCORPORAR EL INGRESO DE LOS HISTÓRICOS
                
                registros = cargarDatosConsulta(Inscripcion_Anual.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Inscripción Anual") % (request.user, logreg))
                return render_to_response('inscripcion/reginscanual.html', {'form':FormInscripcionAnual(auto_id="%s"), 'exito':True,  'inscripcion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Inscripción Anual por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('inscripcion/reginscanual.html', {'form':form, 'errores':e.message,  'inscripcion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Inscripción Anual por el usuario [%s]") % request.user)
            return render_to_response('inscripcion/reginscanual.html', {'form':form, 'errores':'formulario inválido',  'inscripcion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Inscripción Anual desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('inscripcion/reginscanual.html', {'form':FormInscripcionAnual(auto_id="%s"),  'inscripcion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarInscripcionTrimestral(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("insctrimestral")
    registros = cargarDatosConsulta(Inscripcion_Trimestral.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormInscripcionTrimestral(request.POST, auto_id="%s")
        if form.is_valid():
            seccion = form.cleaned_data['seccion']
            nota = form.cleaned_data['nota']
            asistencia = form.cleaned_data['asistencia']
            estatus = form.cleaned_data['estatus']
            cedula = form.cleaned_data['cedula']
            inscripcion_anual = form.cleaned_data['inscripcion_anual']
            modulo_curricular = form.cleaned_data['modulo_curricular']
            trimestre = form.cleaned_data['trimestre']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                est = Estatus_Insctrimestral.objects.get(pk=estatus)
                alumno = Alumno.objects.get(cedula=cedula)
                insa = Inscripcion_Anual.objects.get(pk=inscripcion_anual)
                modcurr = Modulo_Curricular.objects.get(pk=modulo_curricular)
                tri = Trimestre.objects.get(pk=trimestre)
                if modificar=="":
                    inst = Inscripcion_Trimestral(seccion=seccion, nota=nota, asistencia=asistencia, estatus=est, alumno=alumno, 
                                                  inscripcion_anual=insa, modulo_curricular=modcurr, trimestre=tri)
                else:
                    inst = Inscripcion_Trimestral.objects.get(pk=modificar)
                    inst.seccion = seccion
                    inst.nota = nota
                    inst.asistencia = asistencia
                    inst.estatus = est
                    inst.alumno = alumno
                    inst.inscripcion_anual = insa
                    inst.modulo_curricular = modcurr
                    inst.trimestre = tri
                
                inst.usuarioreg = usr
                inst.save()
                #INCORPORAR EL INGRESO DE LOS HISTÓRICOS
                
                registros = cargarDatosConsulta(Inscripcion_Trimestral.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Inscripción Trimestral") % (request.user, logreg))
                return render_to_response('inscripcion/reginsctrim.html', {'form':FormInscripcionTrimestral(auto_id="%s"), 'exito':True,  'inscripcion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Inscripción Trimestral por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('inscripcion/reginsctrim.html', {'form':form, 'errores':e,  'inscripcion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Inscripción Trimestral por el usuario [%s]") % request.user)
            return render_to_response('inscripcion/reginsctrim.html', {'form':form, 'errores':'formulario inválido',  'inscripcion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Inscripción Trimestral desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('inscripcion/reginsctrim.html', {'form':FormInscripcionTrimestral(auto_id="%s"),  'inscripcion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarHito(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("hito")
    registros = cargarDatosConsulta(Hito.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormHito(request.POST, auto_id="%s")
        if form.is_valid():
            seccion = form.cleaned_data['seccion']
            nota = form.cleaned_data['nota']
            cedula = form.cleaned_data['cedula']
            inscripcion_anual = form.cleaned_data['inscripcion_anual']
            modulo_curricular = form.cleaned_data['modulo_curricular']
            estatus = form.cleaned_data['estatus']
            trimestre = form.cleaned_data['trimestre']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                alumno = Alumno.objects.get(cedula=cedula)
                insa = Inscripcion_Anual.objects.get(pk=inscripcion_anual)
                modcurr = Modulo_Curricular.objects.get(pk=modulo_curricular)
                est = Estatus_Inscanual.objects.get(pk=estatus)
                tri = Trimestre.objects.get(pk=trimestre)
                if modificar=="":
                    hito = Hito(seccion=seccion, nota=nota, alumno=alumno, inscripcion_anual=insa, modulo_curricular=modcurr, estatus=est,
                                trimestre=tri)
                else:
                    hito = Hito.objects.get(pk=modificar)
                    hito.seccion = seccion
                    hito.nota = nota
                    hito.alumno = alumno
                    hito.inscripcion_anual = insa
                    hito.modulo_curricular = modcurr
                    hito.estatus = est
                    hito.trimestre = tri
                
                hito.usuarioreg = usr
                hito.save()
                
                registros = cargarDatosConsulta(Hito.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Hito") % (request.user, logreg))
                return render_to_response('inscripcion/reghito.html', {'form':FormHito(auto_id="%s"), 'exito':True, 'registros':registros, 'inscripcion':True})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Hito por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('inscripcion/reghito.html', {'form':form, 'errores':e.message, 'inscripcion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Hito por el usuario [%s]") % request.user)
            return render_to_response('inscripcion/reghito.html', {'form':form, 'errores':'formulario inválido', 'inscripcion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Hito desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('inscripcion/reghito.html', {'form':FormHito(auto_id="%s"),  'inscripcion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})