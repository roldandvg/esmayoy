#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _
from academico.forms import FormAlumno, FormDatoSocioEcon, FormDocumento, FormRecDoc, FormTipoTrimestre, FormTrimestre, FormDatoAcademico, FormAnualidad, FormAnualidadCarrera, FormAnualidadTriCarrera
from academico.models import Alumno, DatoSocioeconomico, Documento, Dato_Documento, Tipo_Trimestre, Trimestre, Dato_Academico, Anualidad, Anualidad_Carrera, Anualidad_Tri_Carrera, Condicion_Ingreso, Sistema_Estudio, Titulo_Bachiller
from institucion.models import Carrera_Sede
from comun.funciones import asignarCarnet, str2bool, cargarDatosConsulta, cargarRequisitosRegistro
from comun.constantes import TIEMPO_SESSION
from comun.models import Parroquia
from os.path import join
import logging

logger = logging.getLogger("academico")

@login_required
def inicio(request):
    """
    @note: Función que muestra la página de inicio del módulo académico
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página de inicio del módulo académico
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    return render_to_response('academico/index.html', {'academico':True, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarAlumno(request):
    """
    @note: Función que muestra el formulario de registro de alumnos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de alumnos
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("alumno")
    registros = cargarDatosConsulta(Alumno.objects.all(),int(request.GET.get('page', '1')))

    if request.method == "POST":
        form = FormAlumno(request.POST, auto_id="%s")
        form2 = FormDatoAcademico(request.POST, auto_id="%s")
        form3 = FormDatoSocioEcon(request.POST, auto_id="%s")
        form4 = FormRecDoc(request.POST, auto_id="%s")

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            """
            @note: variables utilizadas por el formulario de datos del alumno
            """
            nacionalidad = form.cleaned_data['nacionalidad']
            cedula = form.cleaned_data['cedula']
            primerapellido = form.cleaned_data['primerapellido']
            segundoapellido = form.cleaned_data['segundoapellido']
            primernombre = form.cleaned_data['primernombre']
            segundonombre = form.cleaned_data['segundonombre']
            sexo = form.cleaned_data['sexo']
            fnacimiento = form.cleaned_data['fnacimiento']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            movil = form.cleaned_data['movil']
            email = form.cleaned_data['email']
            foto = form.cleaned_data['foto']
            ref_personal = form.cleaned_data['ref_personal']
            tel_ref_personal = form.cleaned_data['tel_ref_personal']
            lugar_nacimiento = form.cleaned_data['lugar_nacimiento']
            carrsed = form.cleaned_data['carrsed']
            
            """
            @note: variables utilizadas por los datos académicos del alumno
            """
            fingreso = form2.cleaned_data['fingreso']
            obs_dataca = form2.cleaned_data['obs_dataca']
            nliceo = form2.cleaned_data['nliceo']
            tliceo = form2.cleaned_data['tliceo']
            serialtitulo = form2.cleaned_data['serialtitulo']
            profesional = form2.cleaned_data['profesional']
            parroquia = form2.cleaned_data['parroquia']
            trimestre = form2.cleaned_data['trimestre']
            condicion_ingreso = form2.cleaned_data['condicion_ingreso']
            sistema_estudio = form2.cleaned_data['sistema_estudio']
            titulo_bachiller = form2.cleaned_data['titulo_bachiller']
            
            """
            @note: variables utilizadas por los datos socio económicos del alumno 
            """
            nhijos = form3.cleaned_data['nhijos']
            mtraslado = form3.cleaned_data['mtraslado']
            costeo_est = form3.cleaned_data['costeo_est']
            tipovivienda = form3.cleaned_data['tipovivienda']
            cond_alojamiento = form3.cleaned_data['cond_alojamiento']
            nivel_m = form3.cleaned_data['nivel_m']
            nivel_p = form3.cleaned_data['nivel_p']
            monto_ingreso = form3.cleaned_data['monto_ingreso']
            trabaja = form3.cleaned_data['trabaja']
            tipo_empresa = form3.cleaned_data['tipo_empresa']
            empresa = form3.cleaned_data['empresa']
            direc_empresa = form3.cleaned_data['direc_empresa']
            telefonoe = form3.cleaned_data['telefonoe']
            discapacidad = form3.cleaned_data['discapacidad']
            des_discapacidad = form3.cleaned_data['des_discapacidad']
            indigena = form3.cleaned_data['indigena']
            obs_datse = form3.cleaned_data['obs_datse']
            
            """
            @note: variable utilizada para la recepción de documentos
            """
            documento = form4.cleaned_data['documento']
            
            """
            @note: variable utilizada para la modificación de datos en caso de existir
            """
            modificar = form.cleaned_data['modificar']
            
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                CS = Carrera_Sede.objects.get(pk=carrsed)
                usr = User.objects.get(username=str(request.user))
                parr = Parroquia.objects.get(pk=parroquia)
                tri = Trimestre.objects.get(pk=trimestre)
                coi = Condicion_Ingreso.objects.get(pk=condicion_ingreso)
                ses = Sistema_Estudio.objects.get(pk=sistema_estudio)
                tba = Titulo_Bachiller.objects.get(pk=titulo_bachiller)

                prefixsede=""
                prefixcarrera=""
                if CS.prefijo_sede:
                    prefixsede = CS.sede.cod_sede
                if CS.prefijo_carrera:
                    prefixcarrera = CS.carrera.cod_carrera
                
                if modificar=="":
                    cod_alumno = asignarCarnet(CS.nro_carnet, CS.format_carnet, prefixsede, prefixcarrera)
                    est = Alumno(cod_alumno=cod_alumno, nacionalidad=nacionalidad, cedula=cedula, primerapellido=primerapellido,
                                 primernombre=primernombre, sexo=sexo, fnacimiento=fnacimiento, direccion=direccion, carrera_sede=CS)
                else:
                    est = Alumno.objects.get(pk=modificar)
                    est.nacionalidad = nacionalidad
                    est.primerapellido = primerapellido
                    est.primernombre = primernombre
                    est.sexo = sexo
                    est.fnacimiento = fnacimiento
                    est.direccion = direccion
                    est.carrera_sede=CS
                    
                if segundoapellido!="":
                    est.segundoapellido=segundoapellido
                if segundonombre!="":
                    est.segundonombre=segundonombre
                if telefono!="":
                    est.telefono=telefono
                if movil!="":
                    est.movil=movil
                if email!="":
                    est.email=email
                if foto!="":
                    est.foto=foto
                if ref_personal!="":
                    est.ref_personal=ref_personal
                if tel_ref_personal!="":
                    est.tel_ref_personal=tel_ref_personal
                if lugar_nacimiento!="":
                    est.lugar_nacimiento=lugar_nacimiento
                est.usuarioreg=usr
                est.save()
                
                """
                @note: Registra los datos académicos del alumno
                """
                if modificar=="":
                    datoa = Dato_Academico(fingreso=fingreso, profesional=profesional, parroquia=parr, alumno=est, trimestre=tri,condicion_ingreso=coi,
                                           sistema_estudio=ses, titulo_bachiller=tba)
                else:
                    datoa = Dato_Academico.objects.get(pk=modificar)
                    datoa.fingreso = fingreso
                    datoa.profesional = profesional
                    datoa.parroquia = parr
                    datoa.alumno = alumno
                    datoa.trimestre = tri
                    datoa.condicion_ingreso = coi
                    datoa.sistema_estudio = ses
                    datoa.titulo_bachiller = tba
                    
                if obs_dataca!="":
                    datoa.observaciones = obs_dataca
                if nliceo!="":
                    datoa.nliceo = nliceo
                if tliceo!="":
                    datoa.tliceo = tliceo
                if serialtitulo!="":
                    datoa.serialtitulo = serialtitulo
                datoa.usuarioreg = usr
                datoa.save()
                
                """
                @note: Registra los datos socio económicos del alumno
                """
                if modificar=="":
                    datse = DatoSocioeconomico(nhijos=nhijos, trabaja=trabaja, discapacidad=discapacidad, indigena=indigena, alumno=est)
                else:
                    datse = DatoSocioeconomico.objects.get(pk=modificar)
                    datse.nhijos = nhijos
                    datse.trabaja = trabaja
                    datse.discapacidad = discapacidad
                    datse.indigena = indigena
                    
                if mtraslado!="":
                    datse.mtraslado = mtraslado
                if costeo_est!="":
                    datse.costeo_est = costeo_est
                if tipovivienda!="":
                    datse.tipovivienda = tipovivienda
                if cond_alojamiento!="":
                    datse.cod_alojamiento = cond_alojamiento
                if nivel_m!="":
                    datse.nivel_m = nivel_m
                if nivel_p!="":
                    datse.nivel_p = nivel_p
                if monto_ingreso!="":
                    datse.monto_ingreso = monto_ingreso
                if tipo_empresa!="":
                    datse.tipo_empresa = tipo_empresa
                if empresa!="":
                    datse.empresa = empresa
                if direccion!="":
                    datse.direccion = direccion
                if telefonoe!="":
                    datse.telefonoe = telefonoe
                if des_discapacidad!="":
                    datse.des_discapacidad = des_discapacidad
                if obs_datse!="":
                    datse.observaciones = obs_datse
                datse.usuarioreg=usr
                datse.save()
                
                """
                @note: Registra los documentos entregados por el alumno
                """
                if Dato_Documento.objects.filter(alumno=est):
                    dd = Dato_Documento.objects.filter(alumno=est)
                    dd.delete()
                for doc in Documento.objects.all():
                    if str(doc.id) in documento:
                        d = Documento.objects.get(pk=doc.id)
                        datdoc = Dato_Documento(entregado=True, documento=d, alumno=est)
                        datdoc.usuarioreg = usr
                        datdoc.save()
                
                """
                @note: Actualiza la numeración de los carnets de la carrea
                """
                nro_carnet = CS.nro_carnet + 1
                cant_carnet = CS.cant_carnet + 1
                
                CS.nro_carnet=nro_carnet
                CS.cant_carnet=cant_carnet
                CS.save()
                
                registros = cargarDatosConsulta(Alumno.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s los datos del alumno con C.I. %s.") % (request.user, logreg, cedula))
                return render_to_response('academico/regalumno.html', {'form':FormAlumno(auto_id="%s"), 'form2':FormDatoAcademico(auto_id="%s"), 'form3':FormDatoSocioEcon(auto_id="%s"), 'form4':FormRecDoc(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s los datos del alumno con C.I. %s por el usuario [%s]. Detalles del error: %s.") % (logreg[:7]+"ar",cedula,request.user,str(e)))
                return render_to_response('academico/regalumno.html', {'form':form, 'form2':form2, 'form3':form3, 'form4':form4, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar los datos de registro de Alumnos por el usuario [%s]") % request.user)
            return render_to_response('academico/regalumno.html', {'form':form, 'form2':form2, 'form3':form3, 'form4':form4, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] accedio al módulo de Registro de Alumnos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regalumno.html', {'form':FormAlumno(auto_id="%s"), 'form2':FormDatoAcademico(auto_id="%s"), 'form3':FormDatoSocioEcon(auto_id="%s"), 'form4':FormRecDoc(auto_id="%s"), 'academico':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarDatosocioecon(request):
    """
    @note: Función que muestra el formulario de los datos socio-económicos del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de los datos socio-económicos del alumno
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(DatoSocioeconomico.objects.all(),request.GET.get('page', '1'))

    if request.method == "POST":
        form = FormDatoSocioEcon(request.POST, auto_id="%s")
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            nhijos = form.cleaned_data['nhijos']
            mtraslado = form.cleaned_data['mtraslado']
            costeo_est = form.cleaned_data['costeo_est']
            tipovivienda = form.cleaned_data['tipovivienda']
            cond_alojamiento = form.cleaned_data['cond_alojamiento']
            nivel_m = form.cleaned_data['nivel_m']
            nivel_p = form.cleaned_data['nivel_p']
            monto_ingreso = form.cleaned_data['monto_ingreso']
            trabaja = form.cleaned_data['trabaja']
            tipo_empresa = form.cleaned_data['tipo_empresa']
            empresa = form.cleaned_data['empresa']
            direccion = form.cleaned_data['direccion']
            telefonoe = form.cleaned_data['telefonoe']
            discapacidad = form.cleaned_data['discapacidad']
            des_discapacidad = form.cleaned_data['des_discapacidad']
            indigena = form.cleaned_data['indigena']
            observaciones = form.cleaned_data['observaciones']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                alumno = Alumno.objects.get(cedula=cedula)
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    datse = DatoSocioeconomico(nhijos=nhijos, trabaja=trabaja, discapacidad=discapacidad, indigena=indigena, alumno=alumno)
                else:
                    datse = DatoSocioeconomico.objects.get(pk=modificar)
                    datse.nhijos = nhijos
                    datse.trabaja = trabaja
                    datse.discapacidad = discapacidad
                    datse.indigena = indigena
                    
                if mtraslado!="":
                    datse.mtraslado = mtraslado
                if costeo_est!="":
                    datse.costeo_est = costeo_est
                if tipovivienda!="":
                    datse.tipovivienda = tipovivienda
                if cond_alojamiento!="":
                    datse.cod_alojamiento = cond_alojamiento
                if nivel_m!="":
                    datse.nivel_m = nivel_m
                if nivel_p!="":
                    datse.nivel_p = nivel_p
                if monto_ingreso!="":
                    datse.monto_ingreso = monto_ingreso
                if tipo_empresa!="":
                    datse.tipo_empresa = tipo_empresa
                if empresa!="":
                    datse.empresa = empresa
                if direccion!="":
                    datse.direccion = direccion
                if telefonoe!="":
                    datse.telefonoe = telefonoe
                if des_discapacidad!="":
                    datse.des_discapacidad = des_discapacidad
                if observaciones!="":
                    datse.observaciones = observaciones
                datse.usuarioreg=usr
                datse.save()

                registros = cargarDatosConsulta(DatoSocioeconomico.objects.all(),request.GET.get('page', '1'))
                
                logger.info(_(u"El usuario [%s] %s los datos socioeconómicos del alumno con C.I. %s") % (request.user, logreg, cedula))
                return render_to_response('academico/regdatosoceco.html', {'form':FormDatoSocioEcon(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s los datos socioeconómicos del alumno con C.I. %s por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", cedula, request.user, str(e)))
                return render_to_response('academico/regdatosoceco.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Datos Socio Económicos por el usuario [%s]") % request.user)
            return render_to_response('academico/regdatosoceco.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingreso al módulo de Registro de Datos Socio Económicos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regdatosoceco.html', {'form':FormDatoSocioEcon(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarDocumento(request):
    """
    @note: Función que muestra el formulario de registro de documentos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de documentos
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Documento.objects.all(),request.GET.get('page', '1'))

    if request.method == "POST":
        form = FormDocumento(request.POST, auto_id="%s")
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    docs = Documento(descripcion=descripcion, estatus=estatus)
                else:
                    docs = Documento.objects.get(pk=modificar)
                    docs.descripcion=descripcion
                    docs.estatus = estatus
                    
                if observaciones!="":
                    docs.observaciones = observaciones
                docs.usuarioreg=usr
                docs.save()
                
                registros = cargarDatosConsulta(Documento.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de documentos") % (request.user, logreg))
                return render_to_response('academico/regdoc.html', {'form':FormDocumento(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s documentos por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, str(e)))
                return render_to_response('academico/regdoc.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de registro de Documentos por el usuario [%s]") % request.user)
            return render_to_response('academico/regdoc.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Documentos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regdoc.html', {'form':FormDocumento(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarRecdoc(request):
    """
    @note: Función que muestra el formulario de registro para la recepción de documentos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro para la recepción de documentos entregados por el alumno
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Dato_Documento.objects.all(),request.GET.get('page', '1'))
    
    if request.method == "POST":
        form = FormRecDoc(request.POST, auto_id="%s")
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            documento = form.cleaned_data['documento']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                guardado = False
                alumno = Alumno.objects.get(cedula=cedula)
                usr = User.objects.get(username=str(request.user))
                if modificar!="":
                    dd = Dato_Documento.objects.filter(alumno=alumno)
                    dd.delete()
                for doc in Documento.objects.all():
                    if str(doc.id) in documento:
                        d = Documento.objects.get(pk=doc.id)
                        datdoc = Dato_Documento(entregado=True, documento=d, alumno=alumno)
                        datdoc.usuarioreg = usr
                        datdoc.save()
                        guardado = True
                registros = cargarDatosConsulta(Dato_Documento.objects.all(),request.GET.get('page', '1'))
                if guardado:
                    logger.info(_(u"El usuario [%s] %s datos en la recepción de documentos para el alumno con C.I. %s") % (request.user, logreg, cedula))
                    return render_to_response('academico/regrecdoc.html', {'form':FormRecDoc(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
                else:
                    logger.info(_(u"El usuario [%s] no seleccionó documentos a recibir por el alumno con C.I. %s") % (request.user, cedula))
                    return render_to_response('academico/regrecdoc.html', {'form':FormRecDoc(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s recepción de documentos para el alumno con C.I. %s por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",cedula,request.user, str(e)))
                return render_to_response('academico/regrecdoc.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Recepción de Documentos por el usuario [%s]") % request.user)
            return render_to_response('academico/regrecdoc.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Recepción de Documentos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regrecdoc.html', {'form':FormRecDoc(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarTipotrime(request):
    """
    @note: Función que muestra el formulario de registro de tipos de trimestre
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de tipos de trimestre
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Tipo_Trimestre.objects.all(),request.GET.get('page', '1'))
    
    if request.method == "POST":
        form = FormTipoTrimestre(request.POST, auto_id="%s")
        if form.is_valid():
            cod_tipotri = form.cleaned_data['cod_tipotri']
            tipotrimestre = form.cleaned_data['tipotrimestre']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tpt = Tipo_Trimestre(cod_tipotri=cod_tipotri, tipotrimestre=tipotrimestre)
                else:
                    tpt = Tipo_Trimestre.objects.get(pk=modificar)
                    tpt.tipotrimestre = tipotrimestre
                tpt.usuarioreg = usr
                tpt.save()
                registros = cargarDatosConsulta(Tipo_Trimestre.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de Tipo de Trimestre") % (request.user, logreg))
                return render_to_response('academico/regtipotri.html', {'form':FormTipoTrimestre(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Tipo de Trimestre por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user, str(e)))
                return render_to_response('academico/regtipotri.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Tipo de Trimestre por el usuario [%s]") % request.user)
            return render_to_response('academico/regtipotri.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro para Tipo de Trimestre desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regtipotri.html', {'form':FormTipoTrimestre(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarTrimestre(request):
    """
    @note: Función que muestra el formulario de registro de trimestres
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de trimestres
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("trimestre")
    registros = cargarDatosConsulta(Trimestre.objects.all(),request.GET.get('page', '1'))
    
    if request.method=="POST":
        form = FormTrimestre(request.POST, auto_id="%s")
        if form.is_valid():
            idtrimestre = form.cleaned_data['idtrimestre']
            descripcion = form.cleaned_data['descripcion']
            finicio = form.cleaned_data['finicio']
            fculmina = form.cleaned_data['fculmina']
            observaciones = form.cleaned_data['observaciones']
            estatus = str2bool(form.cleaned_data['estatus'])
            tipotrimestre = form.cleaned_data['tipotrimestre']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                tpt = Tipo_Trimestre.objects.get(pk=tipotrimestre)
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    tri = Trimestre(idtrimestre=idtrimestre, descripcion=descripcion, finicio=finicio, observaciones=observaciones,
                                    estatus=estatus, tipotrimestre=tpt)
                else:
                    tri = Trimestre.objects.get(pk=modificar)
                    tri.descripcion = descripcion
                    tri.finicio = finicio
                    tri.observaciones = observaciones
                    tri.estatus = estatus
                    tri.tipotrimestre = tpt
                if fculmina!="":
                    tri.fculmina = fculmina
                tri.usuarioreg = usr
                tri.save()
                registros = cargarDatosConsulta(Trimestre.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de Trimestre") % (request.user, logreg))
                return render_to_response('academico/regtrimestre.html', {'form': FormTrimestre(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Trimestre por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar", request.user, str(e)))
                return render_to_response('academico/regtrimestre.html', {'form': form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Trimestre por el usuario [%s]") % request.user)
            return render_to_response('academico/regtrimestre.html', {'form': form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Trimestre desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regtrimestre.html', {'form': FormTrimestre(auto_id="%s"), 'academico':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success
def registrarDatosaca(request):
    """
    @note: Función que muestra el formulario de registro de los datos académicos del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de los datos académicos del alumno
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Dato_Academico.objects.all(),request.GET.get('page', '1'))
    
    if request.method == "POST":
        form = FormDatoAcademico(request.POST, auto_id="%s")
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            fingreso = form.cleaned_data['fingreso']
            observaciones = form.cleaned_data['observaciones']
            nliceo = form.cleaned_data['nliceo']
            tliceo = form.cleaned_data['tliceo']
            serialtitulo = form.cleaned_data['serialtitulo']
            profesional = form.cleaned_data['profesional']
            parroquia = form.cleaned_data['parroquia']
            trimestre = form.cleaned_data['trimestre']
            condicion_ingreso = form.cleaned_data['condicion_ingreso']
            sistema_estudio = form.cleaned_data['sistema_estudio']
            titulo_bachiller = form.cleaned_data['titulo_bachiller']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                parr = Parroquia.objects.get(pk=parroquia)
                alumno = Alumno.objects.get(cedula=cedula)
                tri = Trimestre.objects.get(pk=trimestre)
                coi = Condicion_Ingreso.objects.get(pk=condicion_ingreso)
                ses = Sistema_Estudio.objects.get(pk=sistema_estudio)
                tba = Titulo_Bachiller.objects.get(pk=titulo_bachiller)
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    datoa = Dato_Academico(fingreso=fingreso, profesional=profesional, parroquia=parr, alumno=alumno, trimestre=tri,
                                           condicion_ingreso=coi, sistema_estudio=ses, titulo_bachiller=tba)
                else:
                    datoa = Dato_Academico.objects.get(pk=modificar)
                    datoa.fingreso = fingreso
                    datoa.profesional = profesional
                    datoa.parroquia = parr
                    datoa.alumno = alumno
                    datoa.trimestre = tri
                    datoa.condicion_ingreso = coi
                    datoa.sistema_estudio = ses
                    datoa.titulo_bachiller = tba
                    
                if observaciones!="":
                    datoa.observaciones = observaciones
                if nliceo!="":
                    datoa.nliceo = nliceo
                if tliceo!="":
                    datoa.tliceo = tliceo
                if serialtitulo!="":
                    datoa.serialtitulo = serialtitulo
                datoa.usuarioreg = usr
                datoa.save()
                registros = cargarDatosConsulta(Dato_Academico.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos académicos del alumno con C.I. %s") % (request.user, logreg, cedula))
                return render_to_response('academico/regdatosaca.html', {'form': FormDatoAcademico(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos académicos del alumno con C.I. %s. Detalles del error: %s") % (logreg[:7]+"ar",cedula,str(e)))
                return render_to_response('academico/regdatosaca.html', {'form': form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de registro de datos académicos por el usuario [%s]") % request.user)
            return render_to_response('academico/regdatosaca.html', {'form': form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Datos Académicos desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/regdatosaca.html', {'form': FormDatoAcademico(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success    
def registrarAnualidad(request):
    """
    @note: Función que muestra el formulario de registro de anualidades
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de anualidades
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    registros = cargarDatosConsulta(Anualidad.objects.all(),request.GET.get('page', '1'))
    
    if request.method == "POST":
        form = FormAnualidad(request.POST, auto_id="%s")
        if form.is_valid():
            idanualidad = form.cleaned_data['idanualidad']
            descripcion = form.cleaned_data['descripcion']
            finicio = form.cleaned_data['finicio']
            fculmina = form.cleaned_data['fculmina']
            observaciones = form.cleaned_data['observaciones']
            estatus = form.cleaned_data['estatus']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                if modificar=="":
                    anu = Anualidad(idanualidad=idanualidad, descripcion=descripcion, estatus=estatus)
                else:
                    anu = Anualidad.objects.get(pk=modificar)
                    anu.descripcion = descripcion
                    anu.estatus = estatus
                if finicio!="":
                    anu.finicio = finicio
                if fculmina!="":
                    anu.fculmina = fculmina
                if observaciones!="":
                    anu.observaciones = observaciones
                anu.usuarioreg = usr
                anu.save()
                registros = cargarDatosConsulta(Anualidad.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de Anualidad") % (request.user, logreg))
                return render_to_response('academico/reganualidad.html', {'form':FormAnualidad(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Anualidad por el usuario [%s]. Detalles del error: %s") % (logreg[:7]+"ar",request.user,str(e)))
                return render_to_response('academico/reganualidad.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Anualidad por el usuario [%s]") % request.user)
            return render_to_response('academico/reganualidad.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Anualidad desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/reganualidad.html', {'form':FormAnualidad(auto_id="%s"), 'academico':True, 'registros':registros, 'username':request.user})

@login_required
@transaction.commit_on_success    
def registrarAnualidadCarrera(request):
    """
    @note: Función que muestra el formulario de registro de anualidades por carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de anualidades por carrera
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("anualidadcarr")
    registros = cargarDatosConsulta(Anualidad_Carrera.objects.all(),request.GET.get('page', '1'))
    
    if request.method == "POST":
        form = FormAnualidadCarrera(request.POST, auto_id="%s")
        if form.is_valid():
            idanualidad_carrera = form.cleaned_data['idanualidad_carrera']
            observaciones = form.cleaned_data['observaciones']
            estatus = form.cleaned_data['estatus']
            carrsed = form.cleaned_data['carrsed']
            anualidad = form.cleaned_data['anualidad']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                cs = Carrera_Sede.objects.get(pk=carrsed)
                an = Anualidad.objects.get(pk=anualidad)
                if modificar=="":
                    ac = Anualidad_Carrera(idanualidad_carrera=idanualidad_carrera, estatus=estatus, anualidad=an, carrerasede=cs)
                else:
                    ac = Anualidad_Carrera.objects.get(pk=modificar)
                    ac.estatus = estatus
                    ac.anualidad = an
                    ac.carrerasede = cs
                    
                if observaciones!="":
                    ac.observaciones = observaciones
                ac.usuarioreg = usr
                ac.save()
                registros = cargarDatosConsulta(Anualidad_Carrera.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de Anulidad de la Carrera [%s]") % (request.user, logreg, cs.carrera.cod_carrera))
                return render_to_response('academico/reganualidadcarr.html', {'form':FormAnualidadCarrera(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Anualidad de la Carrera [%s]. Detalles del error: %s") % (logreg[:7]+"ar",cs.carrera.cod_carrera,str(e)))
                return render_to_response('academico/reganualidadcarr.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Anualidad por el usuario [%s]") % request.user)
            return render_to_response('academico/reganualidadcarr.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Anualidad por Carrera desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/reganualidadcarr.html', {'form':FormAnualidadCarrera(auto_id="%s"), 'academico':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})

@login_required
@transaction.commit_on_success    
def registrarAnualidadTriCarrera(request):
    """
    @note: Función que muestra el formulario de registro de anualidades trimestrales por carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un response con la página que contiene el formulario de registro de anualidades trimestrales por carrera
    """
    request.session.set_expiry(TIEMPO_SESSION) #Tiempo de expiración de la sesión
    prerequisito = cargarRequisitosRegistro("anualidadtricarr")
    registros = cargarDatosConsulta(Anualidad_Tri_Carrera.objects.all(),request.GET.get('page', '1'))

    if request.method == "POST":
        form = FormAnualidadTriCarrera(request.POST, auto_id="%s")
        if form.is_valid():
            idanualidadtrimestre = form.cleaned_data['idanualidadtrimestre']
            fregistro = form.cleaned_data['fregistro']
            observaciones = form.cleaned_data['observaciones']
            estatus = form.cleaned_data['estatus']
            trimestre = form.cleaned_data['trimestre']
            anualidad_carrera = form.cleaned_data['anualidad_carrera']
            modificar = form.cleaned_data['modificar']
            logreg = "registro"
            if modificar!="":
                logreg = "modifico"
            try:
                usr = User.objects.get(username=str(request.user))
                ac = Anualidad_Carrera.objects.get(pk=anualidad_carrera)
                tri = Trimestre.objects.get(pk=trimestre)
                if modificar=="":
                    atc = Anualidad_Tri_Carrera(idanualidadtrimestre=idanualidadtrimestre, fregistro=fregistro, estatus=estatus, 
                                                anualidad_carrera=ac, trimestre=tri)
                else:
                    atc = Anualidad_Tri_Carrera.objects.get(pk=modificar)
                    atc.fregistro = fregistro
                    atc.estatus = estatus
                    atc.anualidad_carrera = ac
                    atc.trimestre = tri
                    
                if observaciones!="":
                    atc.observaciones = observaciones
                atc.usuarioreg = usr
                atc.save()
                registros = cargarDatosConsulta(Anualidad_Tri_Carrera.objects.all(),request.GET.get('page', '1'))
                logger.info(_(u"El usuario [%s] %s datos de Anualidad por Trimestre de la Carrera [%s]") % (request.user, logreg, ac.carrerasede.carrera.cod_carrera))
                return render_to_response('academico/reganualidadtricarr.html', {'form':FormAnualidadTriCarrera(auto_id="%s"), 'exito':True, 'academico':True, 'registros':registros, 'username':request.user})
            except Exception, e:
                logger.warning(_(u"Error al %s datos de Anualidad por Trimestre de la Carrera [%s]. Detalles del error: %s") % (logreg[:7]+"ar",ac.carrerasede.carrera.cod_carrera, str(e)))
                return render_to_response('academico/reganualidadtricarr.html', {'form':form, 'errores':str(e), 'academico':True, 'registros':registros, 'username':request.user})
        else:
            logger.warning(_(u"Error al procesar el formulario de Registro de Anualidad por Trimestre por el usuario [%s]") % request.user)
            return render_to_response('academico/reganualidadtricarr.html', {'form':form, 'academico':True, 'registros':registros, 'username':request.user})
    else:
        logger.info(_(u"El usuario [%s] ingresó al módulo de Registro de Anualidad por Trimestre desde la IP [%s]") % (request.user,request.META['REMOTE_ADDR']))
        return render_to_response('academico/reganualidadtricarr.html', {'form':FormAnualidadTriCarrera(auto_id="%s"), 'academico':True, 'registros':registros, 'prerequisito':prerequisito[0], 'inicio':prerequisito[1], 'username':request.user})