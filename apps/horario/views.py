#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from horario.forms import FormTurno, FormHora, FormDia, FormModalidadHorario, FormHorario, FormHorarioTrimestral
from horario.models import Turno, Hora, Dia, Modalidad_Horario, Horario, Horario_Trimestral
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("horario")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('horario/index.html', {'horario':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarTurno(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Turno.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormTurno(request.POST, auto_id="%s")
        if form.is_valid():
            id_turno = form.cleaned_data['id_turno']
            des_turno = form.cleaned_data['des_turno']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tur = Turno(id_turno=id_turno, des_turno=des_turno, estatus=estatus)
                else:
                    tur = Turno.objects.get(pk=modificar)
                    tur.des_turno = des_turno
                    tur.estatus = estatus
                if observaciones!="":
                    tur.observaciones = observaciones
                tur.usuarioreg = usr
                tur.save()
                
                registros = cargarDatosConsulta(Turno.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Turno") % (request.user, logreg))
                return render_to_response('horario/regturno.html', {'form':FormTurno(auto_id="%s"), 'exito':True, 'horario':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de turno por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('horario/regturno.html', {'form':form, 'errores':e.message, 'horario':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Turnos por el usuario [%s]") % request.user)
            return render_to_response('horario/regturno.html', {'form':form, 'horario':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Turnos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('horario/regturno.html', {'form':FormTurno(auto_id="%s"), 'horario':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarHora(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Hora.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormHora(request.POST, auto_id="%s")
        if form.is_valid():
            id_hora = form.cleaned_data['id_hora']
            des_hora = form.cleaned_data['des_hora']
            observacion = form.cleaned_data['observacion']
            estatus = str2bool(form.cleaned_data['estatus'])
            horaini = form.cleaned_data['horaini']
            horafin = form.cleaned_data['horafin']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    hr = Hora(id_hora=id_hora, des_hora=des_hora, estatus=estatus, horaini=horaini, horafin=horafin)
                else:
                    hr = Hora.objects.get(pk=modificar)
                    hr.des_hora = des_hora
                    hr.estatus = estatus
                    hr.horaini = horaini
                    hr.horafin = horafin
                if observacion!="":
                    hr.observacion = observacion
                    hr.usuarioreg = usr
                hr.save()
                
                registros = cargarDatosConsulta(Hora.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Horas") % (request.user, logreg))
                return render_to_response('horario/reghora.html', {'form':FormHora(auto_id="%s"), 'exito':True, 'horario':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Horas por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('horario/reghora.html', {'form':form, 'errores':e.message, 'horario':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Horas por el usuario [%s]") % request.user)
            return render_to_response('horario/reghora.html', {'form':form, 'horario':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Horas desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('horario/reghora.html', {'form':FormHora(auto_id="%s"), 'horario':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarDia(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Dia.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormDia(request.POST, auto_id="%s")
        if form.is_valid():
            id_dia = form.cleaned_data['id_dia']
            des_dia = form.cleaned_data['des_dia']
            observacion = form.cleaned_data['observacion']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    di = Dia(id_dia=id_dia, des_dia=des_dia, estatus=estatus)
                else:
                    di = Dia.objects.get(pk=modificar)
                    di.des_dia = des_dia
                    di.estatus = estatus
                    
                if observacion!="":
                    di.observacion = observacion
                di.usuarioreg = usr
                di.save()
                
                registros = cargarDatosConsulta(Dia.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Día") % (request.user, logreg))
                return render_to_response('horario/regdia.html', {'form':FormDia(auto_id="%s"), 'exito':True, 'horario':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Día por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('horario/regdia.html', {'form':form, 'errores':e.message, 'horario':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Días por el usuario [%s]") % request.user)
            return render_to_response('horario/regdia.html', {'form':form, 'horario':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Días desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('horario/regdia.html', {'form':FormDia(auto_id="%s"), 'horario':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarModhorario(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Modalidad_Horario.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormModalidadHorario(request.POST, auto_id="%s")
        if form.is_valid():
            idmodalidad_horario = form.cleaned_data['idmodalidad_horario']
            des_modalidad = form.cleaned_data['des_modalidad']
            observacion = form.cleaned_data['observacion']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    modh = Modalidad_Horario(idmodalidad_horario=idmodalidad_horario, des_modalidad=des_modalidad, estatus=estatus)
                else:
                    modh = Modalidad_Horario.objects.get(pk=modificar)
                    modh.des_modalidad = des_modalidad
                    modh.estatus = estatus
                if observacion!="":
                    modh.observacion = observacion
                modh.usuarioreg = usr
                modh.save()
                
                registros = cargarDatosConsulta(Modalidad_Horario.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Modalidad de Horario") % (request.user, logreg))
                return render_to_response('horario/regmodhorario.html', {'form':FormModalidadHorario(auto_id="%s"), 'exito':True, 'horario':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Modalidad de Horario por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('horario/regmodhorario.html', {'form':form, 'errores':e.message, 'horario':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Modalidades de Horario por el usuario [%s]") % request.user)
            return render_to_response('horario/regmodhorario.html', {'form':form, 'horario':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Modalidad de Horario desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('horario/regmodhorario.html', {'form':FormModalidadHorario(auto_id="%s"), 'horario':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarHorario(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("horario")
    return render_to_response('horario/reghorario.html', {'form':FormHorario(auto_id="%s"), 'horario':True, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarHorarioTrimestral(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('horario/reghorariotri.html', {'form':FormHorarioTrimestral(auto_id="%s"), 'planificacion':True, 'username':request.user})