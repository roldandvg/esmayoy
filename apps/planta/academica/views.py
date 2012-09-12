#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from horario.models import Dia, Turno
from planta.academica.forms import FormProfesion, FormCondicionProfesor, FormProfesor, FormProfesorCarrera, FormProfesorDisponibilidad
from planta.academica.models import Profesion, Condicion_Profesor, Profesor, Profesor_Carrera, Profesor_Disponibilidad
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("plantaaca")

@login_required
@transaction.commit_on_success
def registrarProfesion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Profesion.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormProfesion(request.POST, auto_id="%s")
        if form.is_valid():
            cod_profesion = form.cleaned_data['cod_profesion']
            profesion = form.cleaned_data['profesion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    pro = Profesion(cod_profesion=cod_profesion, profesion=profesion)
                else:
                    pro = Profesion.objects.get(pk=modificar)
                    pro.profesion
                pro.usuarioreg = usr
                pro.save()
                
                registros = cargarDatosConsulta(Profesion.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Profesión") % (request.user, logreg))
                return render_to_response('planta/academica/regprofesion.html', {'form': FormProfesion(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Profesión por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/academica/regprofesion.html', {'form': form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Profesión por el usuario [%s]") % request.user)
            return render_to_response('planta/academica/regprofesion.html', {'form': form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Profesión desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/academica/regprofesion.html', {'form': FormProfesion(auto_id="%s"), 'planta':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarCondProfesor(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Condicion_Profesor.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormCondicionProfesor(request.POST, auto_id="%s")
        if form.is_valid():
            cod_condicion = form.cleaned_data['cod_condicion']
            des_condicion = form.cleaned_data['des_condicion']
            carga_horaria = form.cleaned_data['carga_horaria']
            observacion = form.cleaned_data['observacion']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    condp = Condicion_Profesor(cod_condicion=cod_condicion, des_condicion=des_condicion, carga_horaria=carga_horaria,
                                               estatus=estatus)
                else:
                    condp = Condicion_Profesor.objects.get(pk=modificar)
                    condp.des_condicion = des_condicion
                    condp.carga_horaria = carga_horaria
                    condp.estatus = estatus
                    
                if observacion!="":
                    condp.observacion = observacion
                condp.usuarioreg = usr
                condp.save()
                
                registros = cargarDatosConsulta(Condicion_Profesor.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Condición del Profesor") % (request.user, logreg))
                return render_to_response('planta/academica/regcondprof.html', {'form': FormCondicionProfesor(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Condición del Profesor por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/academica/regcondprof.html', {'form': form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Condición del Profesor por el usuario [%s]") % request.user)
            return render_to_response('planta/academica/regcondprof.html', {'form': form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Condición del Profesor desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/academica/regcondprof.html', {'form': FormCondicionProfesor(auto_id="%s"), 'planta':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarProfesor(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("profesor")
    registros = cargarDatosConsulta(Profesor.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormProfesor(request.POST, request.FILES, auto_id="%s")
        if form.is_valid():
            cod_profesor = form.cleaned_data['cod_profesor']
            cedula = form.cleaned_data['cedula']
            primerapellido = form.cleaned_data['primerapellido']
            segundoapellido = form.cleaned_data['segundoapellido']
            primernombre = form.cleaned_data['primernombre']
            segundonombre = form.cleaned_data['segundonombre']
            carga_horaria = form.cleaned_data['carga_horaria']
            foto = form.cleaned_data['foto']
            correo = form.cleaned_data['correo']
            telefono = form.cleaned_data['telefono']
            movil = form.cleaned_data['movil']
            profesion = form.cleaned_data['profesion']
            condicion = form.cleaned_data['condicion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                condp = Condicion_Profesor.objects.get(pk=condicion)
                pro = Profesion.objects.get(pk=profesion)
                if modificar=="":
                    profesor = Profesor(cod_profesor=cod_profesor, cedula=cedula, primerapellido=primerapellido, primernombre=primernombre, 
                                        profesion=pro, condicion=condp)
                else:
                    profesor = Profesor.objects.get(pk=modificar)
                    profesor.cedula = cedula
                    profesor.primerapellido = primerapellido
                    profesor.primernombre = primernombre
                    profesor.profesion = pro
                    profesor.condicion = condp
                    
                if segundoapellido!="":
                    profesor.segundoapellido = segundoapellido
                if segundonombre!="":
                    profesor.segundonombre = segundonombre
                if carga_horaria!="":
                    profesor.carga_horaria = carga_horaria
                if foto!="":
                    profesor.foto = foto
                if correo!="":
                    profesor.correo = correo
                if telefono!="":
                    profesor.telefono = telefono
                if movil!="":
                    profesor.movil = movil
                profesor.usuarioreg = usr
                profesor.save()
                
                registros = cargarDatosConsulta(Profesor.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Profesor") % (request.user, logreg))
                return render_to_response('planta/academica/regprofesor.html', {'form': FormProfesor(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Profesor por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/academica/regprofesor.html', {'form': form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Profesor por el usuario [%s]") % request.user)
            return render_to_response('planta/academica/regprofesor.html', {'form': form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Profesor desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/academica/regprofesor.html', {'form': FormProfesor(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarProfCarrera(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("profesorcarr")
    registros = cargarDatosConsulta(Profesor_Carrera.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormProfesorCarrera(request.POST, auto_id="%s")
        if form.is_valid():
            fasignacion = form.cleaned_data['fasignacion']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            profesor = form.cleaned_data['profesor']
            carrsed = form.cleaned_data['carrsed']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                cs = Carrera_Sede.objects.get(pk=carrsed)
                pr = Profesor.objects.get(pk=profesor)
                if modificar=="":
                    pc = Profesor_Carrera(fasignacion=fasignacion, estatus=estatus, profesor=pr, carrera_sede=cs)
                else:
                    pc = Profesor_Carrera.objects.get(pk=modificar)
                    pc.fasignacion = fasignacion
                    pc.estatus = estatus
                    pc.profesor = pr
                    pc.carrera_sede = cs
                    
                if observaciones!="":
                    pc.observaciones = observaciones
                pc.usuarioreg = usr
                pc.save()
                
                registros = cargarDatosConsulta(Profesor_Carrera.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Profesor por Carrera") % (request.user, logreg))
                return render_to_response('planta/academica/regprofcarr.html', {'form': FormProfesorCarrera(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Profesor por Carrera por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/academica/regprofcarr.html', {'form': form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Profesor por Carrera por el usuario [%s]") % request.user)
            return render_to_response('planta/academica/regprofcarr.html', {'form': form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Profesor por Carrera desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/academica/regprofcarr.html', {'form': FormProfesorCarrera(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarProfDisponibilidad(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("profesordisp")
    registros = cargarDatosConsulta(Profesor_Disponibilidad.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormProfesorDisponibilidad(request.POST, auto_id="%s")
        if form.is_valid():
            nro_horas = form.cleaned_data['nro_horas']
            fasignacion = form.cleaned_data['fasignacion']
            observacion = form.cleaned_data['observacion']
            estatus = str2bool(form.cleaned_data['estatus'])
            profesor = form.cleaned_data['profesor']
            dia = form.cleaned_data['dia']
            turno = form.cleaned_data['turno']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                pr = Profesor.objects.get(pk=profesor)
                DIA = Dia.objects.get(pk=dia)
                TURNO = Turno.objects.get(pk=turno)
                if modificar=="":
                    prd = Profesor_Disponibilidad(nro_horas=nro_horas, fasignacion=fasignacion, estatus=estatus, profesor=pr, dia=DIA, 
                                                  turno=TURNO)
                else:
                    prd = Profesor_Disponibilidad.objects.get(pk=modificar)
                    prd.nro_horas = nro_horas
                    prd.fasignacion = fasignacion
                    prd.estatus = estatus
                    prd.profesor = pr
                    prd.dia = DIA
                    prd.turno = TURNO
                    
                if observacion!="":
                    prd.observacion = observacion
                    
                prd.usuarioreg = usr
                prd.save()
                
                registros = cargarDatosConsulta(Profesor_Disponibilidad.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Disponibilidad de Profesor") % (request.user, logreg))
                return render_to_response('planta/academica/regprofdisp.html', {'form': FormProfesorDisponibilidad(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Disponibilidad de Profesor por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/academica/regprofdisp.html', {'form': form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Disponibilidad de Profesor por el usuario [%s]") % request.user)
            return render_to_response('planta/academica/regprofdisp.html', {'form': form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Disponibilidad de Profesor desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/academica/regprofdisp.html', {'form': FormProfesorDisponibilidad(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})