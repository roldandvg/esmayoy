# -*- coding: utf-8 -*-
from dajax.core import Dajax
from academico.models import Alumno, Dato_Academico, DatoSocioeconomico, Documento, Dato_Documento
from comun.funciones import formatoFecha
from comun.models import Pais, Estado, Municipio, Parroquia
from django.utils.translation import ugettext as _

def buscarAlumno(request):
    """
    @note: Función que permite buscar los datos de un alumno
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un mensaje al usuario en caso de no encontrar datos, de lo contrario muestra los datos del alumno
    """
    dajax = Dajax()
    cedula = request.POST['cedula']
    if cedula!="":
        if not Alumno.objects.filter(cedula=cedula):
            dajax.alert(_(u'El alumno no existe. Verifique!!!'))
        else:
            alumno = Alumno.objects.get(cedula=cedula)
            nombre = alumno.primerapellido
            if not alumno.segundoapellido is None:
                nombre = nombre + " " + alumno.segundoapellido
            nombre = nombre + " " + alumno.primernombre
            if not alumno.segundonombre is None:
                nombre = nombre + " " + alumno.segundonombre
            dajax.assign("#nombre", "value", nombre)
    else:
        dajax.alert(_(u"Debe indicar el número de cédula del alumno"))
    return dajax

def mostrarDatosAlumno(request):
    """
    @note: Función que permite mostrar los datos a modificar de un alumno
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    @return: Retorna un objeto dajax que muestra los datos del alumno seleccionado
    """
    dajax = Dajax()
    id = request.POST['alumno']
    est = Alumno.objects.get(pk=id)
    dac = Dato_Academico.objects.get(alumno=est)
    parr = Parroquia.objects.get(pk=dac.parroquia_id)
    mun = Municipio.objects.get(pk=parr.municipio_id)
    edo = Estado.objects.get(pk=mun.estado_id)
    pais = Pais.objects.get(pk=edo.pais_id)
    dse = DatoSocioeconomico.objects.get(alumno=est)
    
    dajax.script("Dajax.comun_cargarEstados({'pais':"+str(pais.id)+"})")
    dajax.script("Dajax.comun_cargarMunicipios({'estado':"+str(edo.id)+"})")
    dajax.script("Dajax.comun_cargarParroquias({'municipio':"+str(mun.id)+"})")
    
    """
    @note: Muestra los datos del alumno en sus respectivos campos
    """
    dajax.assign("#nacionalidad", "value", est.nacionalidad)
    dajax.assign("#cedula","value",est.cedula)
    dajax.assign("#primerapellido","value",est.primerapellido)
    dajax.assign("#segundoapellido","value",est.segundoapellido)
    dajax.assign("#primernombre","value",est.primernombre)
    dajax.assign("#segundonombre","value",est.segundonombre)
    dajax.assign("#sexo","value",est.sexo)
    dajax.assign("#fnacimiento","value",formatoFecha(est.fnacimiento))
    dajax.assign("#direccion","innerHTML",est.direccion)
    dajax.assign("#telefono","innerHTML",est.telefono)
    dajax.assign("#movil","innerHTML",est.movil)
    dajax.assign("#email","value",est.email)
    #falta incluír la foto
    dajax.assign("#ref_personal","innerHTML",est.ref_personal)
    dajax.assign("#tel_ref_personal","innerHTML",est.tel_ref_personal)
    dajax.assign("#lugar_nacimiento","value",est.lugar_nacimiento)
    dajax.assign("#carrsed","value",str(est.carrera_sede.id))
    dajax.assign("#modificar","value",est.cod_alumno)
    
    """
    @note: Muestra los datos académicos del alumno en sus respectivos campos
    """
    dajax.assign("#fingreso","value",formatoFecha(dac.fingreso))
    if dac.observaciones:
        dajax.assign("#obs_dataca", "innerHTML", dac.observaciones)
    if dac.nliceo:
        dajax.assign("#nliceo", "innerHTML", dac.nliceo)
    if dac.tliceo:
        dajax.assign("#tliceo", "value", dac.tliceo)
    if dac.serialtitulo:
        dajax.assign("#serialtitulo", "value", dac.serialtitulo)
    dajax.assign("#profesional", "value", dac.profesional)
    dajax.assign("#pais", "value", pais.id)
    dajax.assign("#estado", "value", edo.id)
    dajax.assign("#municipio", "value", mun.id)
    dajax.assign("#parroquia", "value", parr.id)
    dajax.assign("#trimestre", "value", dac.trimestre.idtrimestre)
    dajax.assign("#condicion_ingreso", "value", dac.condicion_ingreso.cod_ingreso)
    dajax.assign("#sistema_estudio", "value", dac.sistema_estudio.cod_sest)
    dajax.assign("#titulo_bachiller", "value", dac.titulo_bachiller.cod_bachiller)
    
    """
    @note: Muestra los datos socio-económicos del alumno en sus respectivos campos
    """
    dajax.assign("#nhijos", "value", dse.nhijos)
    dajax.assign("#mtraslado", "value", dse.mtraslado)
    dajax.assign("#costeo_est", "value", dse.costeo_est)
    dajax.assign("#tipovivienda", "value", dse.tipovivienda)
    dajax.assign("#cond_alojamiento", "value", dse.cod_alojamiento)
    dajax.assign("#monto_ingreso", "value", dse.monto_ingreso)
    dajax.assign("#nivel_m", "value", dse.nivel_m)
    dajax.assign("#nivel_p", "value", dse.nivel_p)
    dajax.assign("#trabaja", "value", dse.trabaja)
    dajax.assign("#tipo_empresa", "value", dse.tipo_empresa)
    dajax.assign("#empresa", "value", dse.empresa)
    dajax.assign("#direc_empresa", "innerHTML", dse.direccion)
    dajax.assign("#telefonoe", "innerHTML", dse.telefonoe)
    dajax.assign("#obs_datse", "innerHTML", dse.observaciones)
    dajax.assign("#discapacidad", "value", dse.discapacidad)
    dajax.assign("#des_discapacidad", "innerHTML", dse.des_discapacidad)
    dajax.assign("#indigena", "value", dse.indigena)
    
    """
    @note: Muestra los documentos recibidos del alumno
    """
    i=0
    for doc in Documento.objects.all():
        for recdoc in Dato_Documento.objects.filter(alumno=est, documento=doc):
            dajax.assign("#documento_"+str(i), "checked", "true")
        i+=1
    return dajax