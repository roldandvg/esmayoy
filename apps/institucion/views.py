#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.forms import FormSede, FormDpto, FormCarrera, FormCarrSede
from institucion.models import Sede, Departamento, Carrera, Carrera_Sede
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("institucion")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('institucion/index.html', {'institucion':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarSede(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Sede.objects.order_by('cod_sede'),int(request.GET.get('page', '1')))

    if request.method == 'POST':
        form = FormSede(request.POST, auto_id="%s")
        if form.is_valid():
            cod_sede = form.cleaned_data["cod_sede"]
            descripcion = form.cleaned_data["descripcion"]
            direccion = form.cleaned_data["direccion"]
            telefonos = form.cleaned_data["telefonos"]
            fcreacion = form.cleaned_data["fcreacion"]
            contacto = form.cleaned_data["contacto"]
            email = form.cleaned_data["email"]
            estatus = str2bool(form.cleaned_data["estatus"])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    sede = Sede(cod_sede=cod_sede, descripcion=descripcion, estatus=estatus)
                else:
                    sede = Sede.objects.get(pk=modificar)
                    sede.descripcion = descripcion
                    sede.estatus = estatus
                    sede.usuarioreg=usr
                if direccion!="":
                    sede.direccion=direccion
                if telefonos!="":
                    sede.telefonos = telefonos
                if fcreacion!="":
                    sede.fcreacion = fcreacion
                if contacto!="":
                    sede.contacto = contacto
                if email!="":
                    sede.email = email
                sede.usuarioreg = usr
                sede.save()
                
                registros = cargarDatosConsulta(Sede.objects.order_by('cod_sede'),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Sede") % (request.user, logreg))
                return render_to_response('institucion/regsede.html', {'form': FormSede(auto_id="%s"), 'exito':True, 'institucion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Sede por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('institucion/regsede.html', {'form': form, 'errores':e.message, 'institucion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Sede por el usuario [%s]") % request.user)
            return render_to_response('institucion/regsede.html', {'form': form, 'institucion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Sede desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('institucion/regsede.html', {'form': FormSede(auto_id="%s"), 'institucion':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarDpto(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Departamento.objects.order_by('cod_dep'),int(request.GET.get('page', '1')))
    
    if request.method == 'POST':
        form = FormDpto(request.POST, auto_id="%s")
        if form.is_valid():
            cod_dep = form.cleaned_data["cod_dep"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            estatus = str2bool(form.cleaned_data["estatus"])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    dpto = Departamento(cod_dep=cod_dep,descripcion=descripcion,estatus=estatus)
                else:
                    dpto = Departamento.objects.get(pk=modificar)
                    dpto.descripcion = descripcion
                    dpto.estatus = estatus
                if contacto!="":
                    dpto.contacto = contacto
                dpto.usuarioreg = usr
                dpto.save()
                
                registros = cargarDatosConsulta(Departamento.objects.order_by('cod_dep'),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Departamento") % (request.user, logreg))
                return render_to_response('institucion/regdpto.html', {'form':FormDpto(auto_id="%s"), 'exito':True, 'institucion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Departamento por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, e.message))
                return render_to_response('institucion/regdpto.html', {'form':form, 'errores':e.message, 'institucion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Departamento por el usuario [%s]") % request.user)
            return render_to_response('institucion/regdpto.html', {'form':form, 'institucion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Departamento desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('institucion/regdpto.html', {'form': FormDpto(auto_id="%s"), 'institucion':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarCarrera(request):
    prerequisito = cargarRequisitosRegistro("carrera")
    registros = cargarDatosConsulta(Carrera.objects.order_by('cod_carrera'),int(request.GET.get('page', '1')))
    
    if request.method == 'POST':
        form = FormCarrera(request.POST, auto_id="%s")
        if form.is_valid():
            cod_carrera = form.cleaned_data["cod_carrera"]
            descripcion = form.cleaned_data["descripcion"]
            estatus = str2bool(form.cleaned_data["estatus"])
            departamento = form.cleaned_data["departamento"]
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                dep = Departamento.objects.get(pk=departamento)
                if modificar=="":
                    carr = Carrera(cod_carrera=cod_carrera, descripcion=descripcion, estatus=estatus, departamento=dep)
                else:
                    carr = Carrera.objects.get(pk=modificar)
                    carr.descripcion = descripcion
                    carr.estatus = estatus
                    carr.departamento = dep
                carr.usuarioreg = usr
                carr.save()
                
                registros = cargarDatosConsulta(Carrera.objects.order_by('cod_carrera'),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Carrera") % (request.user, logreg))
                return render_to_response('institucion/regcarrera.html', {'form':FormCarrera(auto_id="%s"), 'exito':True, 'institucion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al % datos de Carrera por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, e.message))
                return render_to_response('institucion/regcarrera.html', {'form':form, 'errores':e.message, 'institucion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Carrera por el usuario [%s]") % request.user)
            return render_to_response('institucion/regcarrera.html', {'form':form, 'errores':'formulario no válido', 'institucion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Carrera desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('institucion/regcarrera.html', {'form': FormCarrera(auto_id="%s"), 'institucion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarCarrSed(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("carrerasede")
    registros = cargarDatosConsulta(Carrera_Sede.objects.order_by('sede','carrera'),int(request.GET.get('page', '1')))
    
    if request.method == 'POST':
        form = FormCarrSede(request.POST, auto_id="%s")
        if form.is_valid():
            sede = form.cleaned_data["sede"]
            carrera = form.cleaned_data["carrera"]
            nro_carnet = form.cleaned_data["nro_carnet"]
            cant_carnet = form.cleaned_data["cant_carnet"]
            format_carnet = form.cleaned_data["format_carnet"]
            prefijo_sede = str2bool(form.cleaned_data['prefijo_sede'])
            prefijo_carrera = str2bool(form.cleaned_data['prefijo_carrera'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                sed = Sede.objects.get(pk=sede)
                car = Carrera.objects.get(pk=carrera)
                if modificar=="":
                    carrsed = Carrera_Sede(nro_carnet=nro_carnet, cant_carnet=cant_carnet, format_carnet=format_carnet, sede=sed, carrera=car, prefijo_sede=prefijo_sede, prefijo_carrera=prefijo_carrera)
                else:
                    carrsed = Carrera_Sede.objects.get(pk=modificar)
                    carrsed.nro_carnet = nro_carnet
                    carrsed.cant_carnet = cant_carnet
                    carrsed.format_carnet = format_carnet
                    carrsed.sede = sed
                    carrsed.carrera = car
                    carrsed.prefijo_sede = prefijo_sede
                    carrsed.prefijo_carrera = prefijo_carrera
                carrsed.usuarioreg = usr
                carrsed.save()
                
                registros = cargarDatosConsulta(Carrera_Sede.objects.order_by('sede','carrera'),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Carrera por Sede") % (request.user, logreg))
                return render_to_response('institucion/regcarrsed.html', {'form': FormCarrSede(auto_id='%s'), 'exito':True, 'institucion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Carrera por Sede por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, e.message))
                return render_to_response('institucion/regcarrsed.html', {'form':form, 'errores':e.message, 'institucion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Carrera por Sede por el usuario [%s]") % request.user)
            return render_to_response('institucion/regcarrsed.html', {'form':form, 'errores':'formulario no válido', 'institucion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Carrera por Sede desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('institucion/regcarrsed.html', {'form': FormCarrSede(auto_id="%s"), 'institucion':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})