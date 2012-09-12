#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from unidadcurricular.forms import FormPensum, FormEjeCurricular, FormCondicionUnidad, FormTipoUnidadCurr, FormUnidadCurricular, FormPrelacion, FormModCurricular
from unidadcurricular.models import Pensum, Eje_Curricular, Condicion_Unidad, Tipo_Unidad, Unidad_Curricular, Prelacion, Modulo_Curricular
from comun.funciones import str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
import logging

logger = logging.getLogger("unidadcurr")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('unidadcurricular/index.html', {'unidadcurr':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarPensum(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("pensum")
    registros = cargarDatosConsulta(Pensum.objects.order_by('cod_pensum'),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormPensum(request.POST, auto_id="%s")
        if form.is_valid():
            cod_pensum = form.cleaned_data['cod_pensum']
            descripcion = form.cleaned_data['descripcion']
            finicio = form.cleaned_data['finicio']
            ffinal = form.cleaned_data['ffinal']
            cal_min = form.cleaned_data['cal_min']
            cal_max = form.cleaned_data['cal_max']
            cal_apro = form.cleaned_data['cal_apro']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            carrsed = form.cleaned_data['carrsed']
            modificar=form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                carrerasede = Carrera_Sede.objects.get(pk=carrsed)
                if modificar=="":
                    pen = Pensum(cod_pensum=cod_pensum, descripcion=descripcion, finicio=finicio, ffinal=ffinal, cal_min=cal_min, 
                                 cal_max=cal_max, cal_apro=cal_apro, estatus=estatus, carrerasede=carrerasede)
                else:
                    pen = Pensum.objects.get(pk=modificar)
                    pen.descripcion = descripcion
                    pen.finicio = finicio
                    pen.ffinal = ffinal
                    pen.cal_min = cal_min
                    pen.cal_max = cal_max
                    pen.cal_apro = cal_apro
                    pen.estatus = estatus
                    pen.carrerasede = carrerasede
                if observaciones!="":
                    pen.observaciones = observaciones
                pen.usuarioreg = usr
                pen.save()
                
                registros = cargarDatosConsulta(Pensum.objects.order_by('cod_pensum'),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Pensum de Estudio") % (request.user, logreg))
                return render_to_response('unidadcurricular/regpensum.html', {'form':FormPensum(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Pensum de Estudio por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regpensum.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Pensum de Estudio por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regpensum.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Pensum de Estudio desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regpensum.html', {'form':FormPensum(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarEjeCurr(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Eje_Curricular.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormEjeCurricular(request.POST, auto_id="%s")
        if form.is_valid():
            cod_eje = form.cleaned_data['cod_eje']
            descripcion = form.cleaned_data['descripcion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    eje = Eje_Curricular(cod_eje=cod_eje, descripcion=descripcion)
                else:
                    eje = Eje_Curricular.objects.get(pk=modificar)
                    eje.descripcion = descripcion
                eje.usuarioreg = usr
                eje.save()
                
                registros = cargarDatosConsulta(Eje_Curricular.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Eje Curricular") % (request.user, logreg))
                return render_to_response('unidadcurricular/regejecurr.html', {'form':FormEjeCurricular(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Eje Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regejecurr.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Eje Curricular por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regejecurr.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Eje Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regejecurr.html', {'form':FormEjeCurricular(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarCondUnidad(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Condicion_Unidad.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormCondicionUnidad(request.POST, auto_id="%s")
        if form.is_valid():
            cond_unidad = form.cleaned_data['cond_unidad']
            descripcion = form.cleaned_data['descripcion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    cond = Condicion_Unidad(cond_unidad=cond_unidad, descripcion=descripcion)
                else:
                    cond = Condicion_Unidad.objects.get(pk=modificar)
                    cond.descripcion = descripcion
                cond.usuarioreg = usr
                cond.save()
                
                registros = cargarDatosConsulta(Condicion_Unidad.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Condición de la Unidad Curricular") % (request.user, logreg))
                return render_to_response('unidadcurricular/regcondunid.html', {'form':FormCondicionUnidad(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Condición de la Unidad Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regcondunid.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Condición de la Unidad Curricular por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regcondunid.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Condición de la Unidad Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regcondunid.html', {'form':FormCondicionUnidad(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarTipoUnidCurr(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Tipo_Unidad.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormTipoUnidadCurr(request.POST, auto_id="%s")
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tpu = Tipo_Unidad(descripcion=descripcion)
                else:
                    tpu = Tipo_Unidad.objects.get(pk=modificar)
                    tpu.descripcion = descripcion
                tpu.usuarioreg = usr
                tpu.save()
                
                registros = cargarDatosConsulta(Tipo_Unidad.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Tipo de Unidad Curricular") % (request.user, logreg))
                return render_to_response('unidadcurricular/regtipounicurr.html', {'form':FormTipoUnidadCurr(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Tipo de Unidad Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regtipounicurr.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Tipo de Unidad Curricular por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regtipounicurr.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Tipo de Unidad Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regtipounicurr.html', {'form':FormTipoUnidadCurr(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarUnidadCurr(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("unidadcurr")
    registros = cargarDatosConsulta(Unidad_Curricular.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormUnidadCurricular(request.POST, auto_id="%s")
        if form.is_valid():
            id_unidad = form.cleaned_data['id_unidad']
            cod_unidad = form.cleaned_data['cod_unidad']
            nombre = form.cleaned_data['nombre']
            ucr = form.cleaned_data['ucr']
            pre_ucr = form.cleaned_data['pre_ucr']
            obligatoria = form.cleaned_data['obligatoria']
            trayecto = form.cleaned_data['trayecto']
            trimestre = form.cleaned_data['trimestre']
            cant_mod = form.cleaned_data['cant_mod']
            estatus = str2bool(form.cleaned_data['estatus'])
            hilo = form.cleaned_data['hilo']
            pensum = form.cleaned_data['pensum']
            condicionunidad = form.cleaned_data['condicionunidad']
            ejecurricular = form.cleaned_data['ejecurricular']
            tipounidad = form.cleaned_data['tipounidad']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                pen = Pensum.objects.get(pk=pensum)
                cond = Condicion_Unidad.objects.get(pk=condicionunidad)
                eje = Eje_Curricular.objects.get(pk=ejecurricular)
                tpu = Tipo_Unidad.objects.get(pk=tipounidad)
                if modificar=="":
                    ucur = Unidad_Curricular(id_unidad=id_unidad, cod_unidad=cod_unidad, nombre=nombre, ucr=ucr, pre_ucr=pre_ucr,
                                             obligatoria=obligatoria, trayecto=trayecto, cant_mod=cant_mod, hilo=hilo, pensum=pen,
                                             condicionunidad=cond, ejecurricular=eje, tipounidad=tpu, estatus=estatus)
                else:
                    ucur = Unidad_Curricular.objects.get(pk=modificar)
                    ucur.cod_unidad = cod_unidad
                    ucur.nombre = nombre
                    ucur.ucr = ucr
                    ucur.pre_ucr = pre_ucr
                    ucur.obligatoria = obligatoria
                    ucur.trayecto = trayecto
                    ucur.trimestre = trimestre
                    ucur.cant_mod = cant_mod
                    ucur.hilo = hilo
                    ucur.pensum = pen
                    ucur.condicionunidad = cond
                    ucur.ejecurricular = eje
                    ucur.tipounidad = tpu
                    ucur.estatus = estatus
                if trimestre!="":
                    ucur.trimestre = trimestre
                ucur.usuarioreg = usr
                ucur.save()
                
                registros = cargarDatosConsulta(Unidad_Curricular.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Unidad Curricular") % (request.user, logreg))
                return render_to_response('unidadcurricular/regunicurr.html', {'form':FormUnidadCurricular(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Unidad Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regunicurr.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Unidad Curricular por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regunicurr.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Unidad Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regunicurr.html', {'form':FormUnidadCurricular(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarPrelacion(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("prelacion")
    registros = cargarDatosConsulta(Prelacion.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method == "POST":
        form = FormPrelacion(request.POST, auto_id="%s")
        if form.is_valid():
            cod_prela = form.cleaned_data['cod_prela']
            estatus = str2bool(form.cleaned_data['estatus'])
            unidadcurr = form.cleaned_data['unidadcurr']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                ucur = Unidad_Curricular.objects.get(pk=unidadcurr)
                if modificar=="":
                    pre = Prelacion(cod_prela=cod_prela, estatus=estatus, unidadcurricular=ucur)
                else:
                    pre = Prelacion.objects.get(pk=modificar)
                    pre.estatus = estatus
                    pre.unidadcurricular = ucur
                pre.usuarioreg = usr
                pre.save()
                
                registros = cargarDatosConsulta(Prelacion.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Prelación") % (request.user, logreg))
                return render_to_response('unidadcurricular/regprelacion.html', {'form':FormPrelacion(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Prelación por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regprelacion.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Prelación por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regprelacion.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Prelación desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regprelacion.html', {'form':FormPrelacion(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarModuloCurricular(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("modulocurr")
    registros = cargarDatosConsulta(Modulo_Curricular.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormModCurricular(request.POST, auto_id="%s")
        if form.is_valid():
            cod_modulo = form.cleaned_data['cod_modulo']
            nombre = form.cleaned_data['nombre']
            ucr = form.cleaned_data['ucr']
            trayecto = form.cleaned_data['trayecto']
            trimestre = form.cleaned_data['trimestre']
            porcentaje = form.cleaned_data['porcentaje']
            estatus = str2bool(form.cleaned_data['estatus'])
            unidadcurr = form.cleaned_data['unidadcurr']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                ucur = Unidad_Curricular.objects.get(pk=unidadcurr)
                if modificar=="":
                    mcur = Modulo_Curricular(cod_modulo=cod_modulo, nombre=nombre, ucr=ucr, trayecto=trayecto, trimestre=trimestre,
                                             porcentaje=porcentaje, estatus=estatus, unidadcurricular=ucur)
                else:
                    mcur = Modulo_Curricular.objects.get(pk=modificar)
                    mcur.nombre = nombre
                    mcur.ucr = ucr
                    mcur.trayecto = trayecto
                    mcur.trimestre = trimestre
                    mcur.porcentaje = porcentaje
                    mcur.estatus = estatus
                    mcur.unidadcurricular = ucur
                mcur.usuarioreg = usr
                mcur.save()
                
                registros = cargarDatosConsulta(Modulo_Curricular.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de Módulo Curricular") % (request.user, logreg))
                return render_to_response('unidadcurricular/regmodcurr.html', {'form':FormModCurricular(auto_id="%s"), 'exito':True, 'unidadcurr':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Módulo Curricular por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('unidadcurricular/regmodcurr.html', {'form':form, 'errores':e.message, 'unidadcurr':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Módulo Curricular por el usuario [%s]") % request.user)
            return render_to_response('unidadcurricular/regmodcurr.html', {'form':form, 'errores':'formulario inválido', 'unidadcurr':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Módulo Curricular desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('unidadcurricular/regmodcurr.html', {'form':FormModCurricular(auto_id="%s"), 'unidadcurr':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})