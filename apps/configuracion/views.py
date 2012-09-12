#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from configuracion.forms import FormParametro
from configuracion.models import Parametro
from comun.constantes import TIEMPO_SESSION
from comun.funciones import cargarDatosConsulta
import logging

logger = logging.getLogger("configuracion")

@login_required
def inicio(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('configuracion/index.html', {'configuracion':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarParametro(request):
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Parametro.objects.all(),int(request.GET.get('page', '1')))
    
    if request.method=="POST":
        form = FormParametro(request.POST, auto_id="%s")
        if form.is_valid():
            idparametro = form.cleaned_data['idparametro']
            descripcion = form.cleaned_data['descripcion']
            vnum = form.cleaned_data['vnum']
            vdate = form.cleaned_data['vdate']
            vstring = form.cleaned_data['vstring']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    par = Parametro(idparametro=idparametro, descripcion=descripcion)
                else:
                    par = Parametro.objects.get(pk=modificar)
                    par.descripcion = descripcion
                par.vnum = vnum
                par.vdate = vdate
                par.vstring = vstring
                par.usuarioreg = usr
                par.save()
                
                registros = cargarDatosConsulta(Parametro.objects.all(),int(request.GET.get('page', '1')))
                logger.info(_(u"El usuario [%s] %s datos de parámetros de configuración del sistema") % (request.user, logreg))
                return render_to_response('configuracion/regparametros.html', {'form':FormParametro(auto_id="%s"), 'exito':True, 'configuracion':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de parámetros de configuración del sistema por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,e.message))
                return render_to_response('configuracion/regparametros.html', {'form':form, 'errores':e.message, 'configuracion':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Parámetros de Configuración del Sistema por el usuario [%s]") % request.user)
            return render_to_response('configuracion/regparametros.html', {'form':form, 'errores':'formulario inválido', 'configuracion':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Parámetros de Configuración del Sistema desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('configuracion/regparametros.html', {'form':FormParametro(auto_id="%s"), 'configuracion':True, 'registros':registros, 'username':request.user})