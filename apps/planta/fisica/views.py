#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from planta.fisica.forms import FormTipoAula, FormTipoEdificio, FormEdificio, FormAula, FormAulaCarrera
from planta.fisica.models import Tipo_Aula, Tipo_Edificio, Edificio, Aula, Aula_Carrera
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("plantafis")

@login_required
@transaction.commit_on_success
def registrarTipoAula(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Tipo_Aula.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormTipoAula(request.POST, auto_id="%s")
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tpa = Tipo_Aula(descripcion=descripcion, estatus=estatus)
                else:
                    tpa = Tipo_Aula.objects.get(pk=modificar)
                    tpa.descripcion = descripcion
                    tpa.estatus = estatus
                tpa.usuarioreg = usr
                tpa.save()
                
                registros = cargarDatosConsulta(Tipo_Aula.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Tipo de Aula") % (request.user, logreg))
                return render_to_response('planta/fisica/regtipoaula.html', {'form':FormTipoAula(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Tipo de Aula por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/fisica/regtipoaula.html', {'form':form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Tipo de Aula por el usuario [%s]") % request.user)
            return render_to_response('planta/fisica/regtipoaula.html', {'form':form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Tipo de Aula desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/fisica/regtipoaula.html', {'form':FormTipoAula(auto_id="%s"), 'planta':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarTipoEdificio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Tipo_Edificio.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormTipoEdificio(request.POST, auto_id="%s")
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tpe = Tipo_Edificio(descripcion=descripcion, estatus=estatus)
                else:
                    tpe = Tipo_Edificio.objects.get(pk=modificar)
                    tpe.descripcion = descripcion
                    tpe.estatus = estatus
                tpe.usuarioreg = usr
                tpe.save()
                
                registros = cargarDatosConsulta(Tipo_Edificio.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Tipo de Edificio") % (request.user, logreg))
                return render_to_response('planta/fisica/regtipoedif.html', {'form':FormTipoEdificio(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Tipo de Edificio por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/fisica/regtipoedif.html', {'form':form, 'errores':True, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Tipo de Edificio por el usuario [%s]") % request.user)
            return render_to_response('planta/fisica/regtipoedif.html', {'form':form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Tipo de Edificio desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/fisica/regtipoedif.html', {'form':FormTipoEdificio(auto_id="%s"), 'planta':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarEdificio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("edificio")
    registros = cargarDatosConsulta(Edificio.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormEdificio(request.POST, auto_id="%s")
        if form.is_valid():
            cod_edif = form.cleaned_data['cod_edif']
            descripcion = form.cleaned_data['descripcion']
            nro_aulas = form.cleaned_data['nro_aulas']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            tipo_edificio = form.cleaned_data['tipo_edificio']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                tpe = Tipo_Edificio.objects.get(pk=tipo_edificio)
                if modificar=="":
                    edi = Edificio(cod_edif=cod_edif, descripcion=descripcion, nro_aulas=nro_aulas, estatus=estatus, tipo_edificio=tpe)
                else:
                    edi = Edificio.objects.get(pk=modificar)
                    edi.descripcion = descripcion
                    edi.nro_aulas = nro_aulas
                    edi.estatus = estatus
                    edi.tipo_edificio = tpe
                    
                if observaciones!="":
                    edi.observaciones = observaciones
                    
                edi.usuarioreg = usr
                edi.save()
                
                registros = cargarDatosConsulta(Edificio.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Edificio") % (request.user, logreg))
                return render_to_response('planta/fisica/regedificio.html', {'form':FormEdificio(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Edificio por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/fisica/regedificio.html', {'form':form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Edificio por el usuario [%s]") % request.user)
            return render_to_response('planta/fisica/regedificio.html', {'form':form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Edificio desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/fisica/regedificio.html', {'form':FormEdificio(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarAula(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("aula")
    registros = cargarDatosConsulta(Aula.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormAula(request.POST, auto_id="%s")
        if form.is_valid():
            cod_aula = form.cleaned_data['cod_aula']
            descripcion = form.cleaned_data['descripcion']
            capacidad = form.cleaned_data['capacidad']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            edificio = form.cleaned_data['edificio']
            tipo_aula = form.cleaned_data['tipo_aula']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                edi = Edificio.objects.get(cod_edif=edificio)
                tpa = Tipo_Aula.objects.get(pk=tipo_aula)
                if modificar=="":
                    aul = Aula(cod_aula=cod_aula, descripcion=descripcion, capacidad=capacidad, estatus=estatus, edificio=edi, tipo_aula=tpa)
                else:
                    aul = Aula.objects.get(pk=modificar)
                    aul.descripcion = descripcion
                    aul.capacidad = capacidad
                    aul.estatus = estatus
                    aul.edificio = edi
                    aul.tipo_aula = tpa
                    
                if observaciones!="":
                    aul.observaciones = observaciones
                    
                aul.usuarioreg = usr
                aul.save()
                
                registros = cargarDatosConsulta(Aula.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Aula") % (request.user, logreg))
                return render_to_response('planta/fisica/regaula.html', {'form':FormAula(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Aula por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/fisica/regaula.html', {'form':form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Aula por el usuario [%s]") % request.user)
            return render_to_response('planta/fisica/regaula.html', {'form':form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Aula desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/fisica/regaula.html', {'form':FormAula(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarAulaCarrera(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("aulacarr")
    registros = cargarDatosConsulta(Aula_Carrera.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormAulaCarrera(request.POST, auto_id="%s")
        if form.is_valid():
            observaciones = form.cleaned_data['observaciones']
            fecha_asignacion = form.cleaned_data['fecha_asignacion']
            semana = form.cleaned_data['semana']
            estatus = str2bool(form.cleaned_data['estatus'])
            aula = form.cleaned_data['aula']
            carrsed = form.cleaned_data['carrsed']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                cs = Carrera_Sede.objects.get(pk=carrsed)
                aul = Aula.objects.get(cod_aula=aula)
                if modificar=="":
                    ac = Aula_Carrera(observaciones=observaciones, fecha_asignacion=fecha_asignacion, estatus=estatus, carrera_sede=cs, aula=aul)
                else:
                    ac = Aula_Carrera.objects.get(pk=modificar)
                    ac.observaciones = observaciones
                    ac.fecha_asignacion = fecha_asignacion
                    ac.estatus = estatus
                    ac.carrera_sede = cs
                    
                for dia in semana:
                    if dia=="lu":
                        ac.lu=True
                    elif dia=="ma":
                        ac.ma=True
                    elif dia=="mi":
                        ac.mi=True
                    elif dia=="ju":
                        ac.ju=True
                    elif dia=="vi":
                        ac.vi=True
                    elif dia=="sa":
                        ac.sa=True
                    elif dia=="do":
                        ac.do=True
                        
                ac.usuarioreg = usr
                ac.save()
                
                registros = cargarDatosConsulta(Aula_Carrera.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Aula por Carrera") % (request.user, logreg))
                return render_to_response('planta/fisica/regaulacarr.html', {'form':FormAulaCarrera(auto_id="%s"), 'exito':True, 'planta':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Aula por Carrera por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('planta/fisica/regaulacarr.html', {'form':form, 'errores':e.message, 'planta':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Aula por Carrera por el usuario [%s]") % request.user)
            return render_to_response('planta/fisica/regaulacarr.html', {'form':form, 'errores':'formulario inválido', 'planta':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Aula por Carrera desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('planta/fisica/regaulacarr.html', {'form':FormAulaCarrera(auto_id="%s"), 'planta':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})