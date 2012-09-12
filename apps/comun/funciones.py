#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from institucion.models import Sede, Departamento, Carrera, Carrera_Sede
from unidadcurricular.models import Pensum, Condicion_Unidad, Eje_Curricular, Tipo_Unidad, Unidad_Curricular, Modulo_Curricular
from academico.models import Alumno, Documento, Tipo_Trimestre, Trimestre, Condicion_Ingreso, Sistema_Estudio, Titulo_Bachiller, Anualidad, Anualidad_Carrera, Anualidad_Tri_Carrera
from comun.models import Pais, Estado, Municipio, Parroquia
from horario.models import Modalidad_Horario, Dia, Hora, Horario, Turno
from planta.academica.models import Profesion, Condicion_Profesor, Profesor
from planta.fisica.models import Tipo_Edificio, Edificio, Tipo_Aula, Aula
from planificacion.models import Planificacion, Planificacion_Unidad
from inscripcion.models import Estatus_Inscanual, Estatus_Insctrimestral, Inscripcion_Anual, Inscripcion_Trimestral

def cargarPermisos():
    """
    @note: Función que permite cargar los permisos de acceso a los diferentes módulos del sistema
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los permisos registrados en el sistema
    """
    per = Permission.objects.order_by('name')
    permisos = [(p.id, (p.name).replace('Can add', 'Registrar').replace('Can change','Modificar').replace('Can delete','Eliminar')) for p in per]
    return permisos

def cargarDepartamentos():
    """
    @note: Función que permite cargar los departamentos de la institución
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los departamentos de la institución
    """
    lista = ('0', 'Seleccione...'),
    try:
        for dep in Departamento.objects.all():
            if dep.descripcion.__len__()>30:
                desc = dep.descripcion[:30]+"..."
            else:
                desc = dep.descripcion
            lista += (dep.cod_dep, desc),
    except:
        pass
    return lista

def cargarSedes():
    """
    @note: Función que permite cargar las sedes
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las sedes
    """
    lista = ('0', 'Seleccione...'),
    try:
        for sed in Sede.objects.all():
            if sed.descripcion.__len__()>30:
                desc = sed.descripcion[:30]+"..."
            else:
                desc = sed.descripcion
            lista += (sed.cod_sede, desc),
    except:
        pass
    return lista

def cargarCarreras():
    """
    @note: Función que permite cargar las carreras
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las carreras
    """
    lista = ('0', 'Seleccione...'),
    try:
        for car in Carrera.objects.all():
            if car.descripcion.__len__()>30:
                desc = car.descripcion[:30]+"..."
            else:
                desc = car.descripcion
            lista += (car.cod_carrera, desc),
    except:
        pass
    return lista

def cargarCarrerasSede():
    """
    @note: Función que permite cargar las carreras registradas por sede
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las carreras por sedes
    """
    lista = [('0','Seleccione...')]
    try:
        for se in Sede.objects.all():
            carrerasxsede = []
            carreras = []
            for carrsed in Carrera_Sede.objects.filter(sede=se.cod_sede):
                carreras.append([carrsed.id, carrsed.carrera.descripcion])
            if carreras:
                carrerasxsede = [se.descripcion, carreras]
                lista.append(carrerasxsede)
    except:
        pass
    return lista

def cargarPensums():
    """
    @note: Función que permite cargar los pensums de estudio
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los pensums de estudio
    """
    lista = ('0', 'Seleccione...'),
    try:
        for pen in Pensum.objects.all():
            if pen.descripcion.__len__()>30:
                desc = pen.descripcion[:30]+"..."
            else:
                desc = pen.descripcion
            lista += (pen.id, desc),
    except:
        pass
    return lista

def cargarCondicionUnidades():
    """
    @note: Función que permite cargar las condiciones de las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las condiciones de las unidades curriculares
    """
    lista = ('0', 'Seleccione...'),
    try:
        for con in Condicion_Unidad.objects.all():
            if con.descripcion.__len__()>30:
                desc = con.descripcion[:30]+"..."
            else:
                desc = con.descripcion
            lista += (con.cond_unidad, desc),
    except:
        pass
    return lista

def cargarEjesCurriculares():
    """
    @note: Función que permite cargar los ejes curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los ejes curriculares
    """
    lista = ('0', 'Seleccione...'),
    try:
        for eje in Eje_Curricular.objects.all():
            if eje.descripcion.__len__()>30:
                desc = eje.descripcion[:30]+"..."
            else:
                desc = eje.descripcion
            lista += (eje.cod_eje, desc),
    except:
        pass
    return lista

def cargarTiposUnidades():
    """
    @note: Función que permite cargar los ejes curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los ejes curriculares
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tpu in Tipo_Unidad.objects.all():
            if tpu.descripcion.__len__()>30:
                desc = tpu.descripcion[:30]+"..."
            else:
                desc = tpu.descripcion
            lista += (tpu.id, desc),
    except:
        pass
    return lista

def cargarUnidadesCurriculares():
    """
    @note: Función que permite cargar las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las unidades curriculares
    """
    lista = ('0', 'Seleccione...'),
    try:
        for ucu in Unidad_Curricular.objects.all():
            if ucu.nombre.__len__()>30:
                nombre = ucu.nombre[:30]+"..."
            else:
                nombre = ucu.nombre
            lista += (ucu.id_unidad, nombre),
    except:
        pass
    return lista

def cargarDocumentos():
    """
    @note: Función que permite cargar los documentos solicitados por la institución para las inscripciones de alumnos
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los documentos solicitados por la institución
    """
    docs  = Documento.objects.filter(estatus=True)
    documentos = [(d.id, d.descripcion ) for d in docs]
    return documentos

def cargarTipostrimestres():
    """
    @note: Función que permite cargar los tipos de trimestres
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los tipos de trimestre registrados
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tpt in Tipo_Trimestre.objects.all():
            if tpt.tipotrimestre.__len__()>30:
                nombre = tpt.tipotrimestre[:30]+"..."
            else:
                nombre = tpt.tipotrimestre
            lista += (tpt.cod_tipotri, nombre),
    except:
        pass
    return lista

def cargarPaises():
    """
    @note: Función que permite cargar los países
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los países registrados en el sistema
    """
    lista = ('0', 'Seleccione...'),
    try:
        for pais in Pais.objects.all():
            lista += (pais.id, pais.nombre),
    except:
        pass
    return lista

def cargarEstados(id_pais):
    """
    @note: Función que permite cargar los estados de un pais
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param id_pais: Variable de tipo integer que contiene el identificador del pais seleccionado
    @return: Retorna un listado con todos los estados de un pais seleccionado
    """
    lista = ('0', 'Seleccione...'),
    try:
        for edo in Estado.objects.filter(pais=id_pais):
            lista += (edo.id, edo.nombre),
    except:
        pass
    return lista

def cargarMunicipios(id_estado):
    """
    @note: Función que permite cargar los municipios de un estado
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param id_estado: Variable de tipo integer que contiene el identificador del estado seleccionado
    @return: Retorna un listado con todos los municipios de un estado seleccionado
    """
    lista = ('0', 'Seleccione...'),
    try:
        for mun in Municipio.objects.filter(estado=id_estado):
            lista += (mun.id, mun.nombre),
    except:
        pass
    return lista

def cargarParroquias(id_municipio):
    """
    @note: Función que permite cargar las parroquías de un municipio
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param id_municipio: Variable de tipo integer que contiene el identificador del municipio seleccionado
    @return: Retorna un listado con todas las parroquías de un municipio seleccionado
    """
    lista = ('0', 'Seleccione...'),
    try:
        for par in Parroquia.objects.filter(municipio=id_municipio):
            lista += (par.id, par.nombre),
    except:
        pass
    return lista

def cargarTrimestres():
    """
    @note: Función que permite cargar los trimestres
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los trimestres registrados
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tri in Trimestre.objects.all():
            if tri.descripcion.__len__()>30:
                nombre = tri.descripcion[:30]+"..."
            else:
                nombre = tri.descripcion
            lista += (tri.idtrimestre, nombre),
    except:
        pass
    return lista

def cargarCondicionesingreso():
    """
    @note: Función que permite cargar las condiciones de ingreso del alumno
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las condiciones de ingreso de los alumnos
    """
    lista = ('0', 'Seleccione...'),
    try:
        for cing in Condicion_Ingreso.objects.all():
            if cing.descripcion.__len__()>30:
                nombre = cing.descripcion[:30]+"..."
            else:
                nombre = cing.descripcion
            lista += (cing.cod_ingreso, nombre),
    except:
        pass
    return lista

def cargarSistemasestudio():
    """
    @note: Función que permite cargar los sistemas de estudio
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los sistemas de estudio registrados en el sistema
    """
    lista = ('0', 'Seleccione...'),
    try:
        for sest in Sistema_Estudio.objects.all():
            if sest.descripcion.__len__()>30:
                nombre = sest.descripcion[:30]+"..."
            else:
                nombre = sest.descripcion
            lista += (sest.cod_sest, nombre),
    except:
        pass
    return lista

def cargarTitulosbachiller():
    """
    @note: Función que permite cargar los diferentes títulos de bachiller
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los títulos de bachiller registrados en el sistema
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tib in Titulo_Bachiller.objects.all():
            if tib.descripcion.__len__()>30:
                nombre = tib.descripcion[:30]+"..."
            else:
                nombre = tib.descripcion
            lista += (tib.cod_bachiller, nombre),
    except:
        pass
    return lista

def cargarModalidades():
    """
    @note: Función que permite cargar las modalidades de estudio
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las modalidades de estudio disponibles
    """
    lista = ('0', 'Seleccione...'),
    try:
        for mod in Modalidad_Horario.objects.filter(estatus=True):
            lista += (mod.idmodalidad_horario, mod.des_modalidad),
    except:
        pass
    return lista

def cargarProfesiones():
    """
    @note: Función que permite cargar las diferentes profesiones
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las profesiones registradas
    """
    lista = ('0', 'Seleccione...'),
    try:
        for pro in Profesion.objects.all():
            if pro.profesion.__len__()>30:
                nombre = pro.profesion[:30]+"..."
            else:
                nombre = pro.profesion
            lista += (pro.cod_profesion, nombre),
    except:
        pass
    return lista

def cargarCondicionesProf():
    """
    @note: Función que permite cargar las condiciones de profesores
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las condiciones de los profesores
    """
    lista = ('0', 'Seleccione...'),
    try:
        for cdp in Condicion_Profesor.objects.filter(estatus=True):
            if cdp.des_condicion.__len__()>30:
                nombre = cdp.des_condicion[:30]+"..."
            else:
                nombre = cdp.des_condicion
            lista += (cdp.cod_condicion, nombre),
    except:
        pass
    return lista

def cargarProfesores():
    """
    @note: Función que permite cargar los profesores de la institución
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los profesores de la institución
    """
    sapel = ""
    snom = ""
    lista = ('0', 'Seleccione...'),
    try:
        for pro in Profesor.objects.all():
            if not pro.segundoapellido is None:
                sapel = pro.segundoapellido
            if not pro.segundonombre is None:
                snom = pro.segundonombre
            nombre = "%s %s %s %s" % (pro.primerapellido, sapel, pro.primernombre, snom)
            lista += (pro.cod_profesor, nombre),
    except:
        pass
    return lista

def cargarDias():
    """
    @note: Función que permite cargar los días de la semana
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los días de la semana
    """
    lista = ('0', 'Seleccione...'),
    try:
        for dia in Dia.objects.filter(estatus=True):
            lista += (dia.id_dia, dia.des_dia),
    except:
        pass
    return lista

def cargarHoras():
    """
    @note: Función que permite cargar las horas para los horarios
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las horas registradas para los horarios de clase
    """
    lista = ('0', 'Seleccione...'),
    try:
        for hr in Hora.objects.filter(estatus=True):
            lista += (hr.id_hora, hr.des_hora),
    except:
        pass
    return lista

def cargarTurnos():
    """
    @note: Función que permite cargar los turnos para los horarios
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los turnos registrados para los horarios de clase
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tr in Turno.objects.filter(estatus=True):
            lista += (tr.id_turno, tr.des_turno),
    except:
        pass
    return lista

def cargarHorario():
    """
    @note: Función que permite cargar los horarios de clase
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los horarios de clase
    """
    lista = ('0', 'Seleccione...'),
    """
    listaDias = ()
    listaHoras = ()
    for dia in Dia.objects.filter(estatus=True):
        listaDias += (dia.id_dia, dia.des_dia)
    for hr in Hora.objects.filter(estatus=True):
        listaHoras += (hr.id_hora, hr.des_hora)
    
    return listaDias, listaHoras
    """
    return lista 

def asignarCarnet(nro,formato,prefixsede="",prefixcarrera=""):
    """
    @note: Función que permite cargar asignar el número de carnet
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param nro: Variable de tipo string que contiene el número de carnet disponible a ser asignado
    @param formato: Variable de tipo string que contiene el formato del carnet
    @param prefixsede: Variable de tipo string que contiene el prefijo de la sede a ser asignado al número de carnet
    @param prefixcarrera: Variable de tipo string que contiene el prefijo de la carrera a ser asignado al número de carnet
    @return: Retorna una variable que contiene el número de carnet asignado
    """
    carnet = "%s%s%s" % (prefixsede,prefixcarrera,nro)
    return carnet

def cargarTiposEdificios():
    """
    @note: Función que permite cargar los tipos de edificio de la planta física
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los tipos de edificio registrados
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tpe in Tipo_Edificio.objects.filter(estatus=True):
            if tpe.descripcion.__len__()>30:
                desc = tpe.descripcion[:30]+"..."
            else:
                desc = tpe.descripcion
            lista += (str(tpe.id), desc),
    except:
        pass
    return lista

def cargarEdificios():
    """
    @note: Función que permite cargar los edificios de la planta física
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los edificios registrados
    """
    lista = ('0', 'Seleccione...'),
    try:
        for edi in Edificio.objects.filter(estatus=True):
            if edi.descripcion.__len__()>30:
                desc = edi.descripcion[:30]+"..."
            else:
                desc = edi.descripcion
            lista += (edi.cod_edif, desc),
    except:
        pass
    return lista

def cargarTiposAulas():
    """
    @note: Función que permite cargar los tipos de aula
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los tipos de aula disponibles
    """
    lista = ('0', 'Seleccione...'),
    try:
        for tpa in Tipo_Aula.objects.filter(estatus=True):
            if tpa.descripcion.__len__()>30:
                desc = tpa.descripcion[:30]+"..."
            else:
                desc = tpa.descripcion
            lista += (str(tpa.id), desc),
    except:
        pass
    return lista

def cargarAulas():
    """
    @note: Función que permite cargar las aulas de clase
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las aulas de clase disponibles
    """
    lista = ('0', 'Seleccione...'),
    try:
        for aul in Aula.objects.filter(estatus=True):
            if aul.descripcion.__len__()>30:
                desc = aul.descripcion[:30]+"..."
            else:
                desc = aul.descripcion
            lista += (aul.cod_aula, desc),
    except:
        pass
    return lista

def cargarAnualidades():
    """
    @note: Función que permite cargar las anualidades
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las anualidades
    """
    lista = ('0', 'Seleccione...'),
    try:
        for anu in Anualidad.objects.filter(estatus='A'):
            if anu.descripcion.__len__()>30:
                desc = anu.descripcion[:30]+"..."
            else:
                desc = anu.descripcion
            lista += (anu.idanualidad, desc),
    except:
        pass
    return lista

def cargarAnualidadesCarreras():
    """
    @note: Función que permite cargar las anualidades por carrera
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las anualidades registradas por carrera
    """
    lista = ('0', 'Seleccione...'),
    try:
        for anuc in Anualidad_Carrera.objects.filter(estatus='A'):
            if anuc.observaciones.__len__()>30:
                desc = anuc.observaciones[:30]+"..."
            else:
                desc = anuc.observaciones
            lista += (anuc.idanualidad_carrera, desc),
    except:
        pass
    return lista

def cargarAnualidadTriCarreras():
    """
    @note: Función que permite cargar las anualidades trimestrales por carrera
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las anualidades trimestrales por carrera
    """
    lista = ('0', 'Seleccione...'),
    try:
        for atc in Anualidad_Tri_Carrera.objects.filter(estatus='A'):
            if atc.observaciones.__len__()>30:
                desc = atc.observaciones[:30]+"..."
            else:
                desc = atc.observaciones
            lista += (atc.idanualidadtrimestre, desc),
    except:
        pass
    return lista

def cargarPlanificaciones():
    """
    @note: Función que permite cargar las planificaciones académicas
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las planificaciones académicas
    """
    lista = ('0', 'Seleccione...'),
    try:
        for pla in Planificacion.objects.all():
            if pla.descripcion.__len__()>30:
                desc = pla.descripcion[:30]+"..."
            else:
                desc = pla.descripcion
            lista += (str(pla.id), desc),
    except:
        pass
    return lista

def cargarModulosCurr():
    """
    @note: Función que permite cargar los módulos curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los módulos curriculares registrados
    """
    lista = ('0', 'Seleccione...'),
    try:
        for mod in Modulo_Curricular.objects.filter(estatus=True):
            if mod.nombre.__len__()>30:
                desc = mod.nombre[:30]+"..."
            else:
                desc = mod.nombre
            lista += (mod.cod_modulo, desc),
    except:
        pass
    return lista

def cargarEstatusInscanual():
    """
    @note: Función que permite cargar los estatus de inscripción anual
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los estatus de inscripción anual disponibles
    """
    lista = ('0', 'Seleccione...'),
    try:
        for eia in Estatus_Inscanual.objects.all():
            lista += (eia.estatus, eia.descripcion),
    except:
        pass
    return lista

def cargarEstatusInsctrimestral():
    """
    @note: Función que permite cargar los estatus de inscripción trimestral
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los estatus de inscripción trimestral
    """
    lista = ('0', 'Seleccione...'),
    try:
        for eit in Estatus_Insctrimestral.objects.all():
            lista += (eit.estatus, eit.descripcion),
    except:
        pass
    return lista

def cargarPlanificacionUnidades():
    """
    @note: Función que permite cargar las planificaciones de las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todas las planificaciones de las unidades curriculares 
    """
    lista = ('0', 'Seleccione...'),
    try:
        for plu in Planificacion_Unidad.objects.filter(estatus=True):
            if plu.planificacion.descripcion.__len__()>30:
                desc = plu.planificacion.descripcion[:30]+"..."
            else:
                desc = plu.planificacion.descripcion
            lista += (str(plu.id), desc),
    except:
        pass
    return lista

def cargarInscripcionAnual():
    lista = ('0', 'Seleccione...'),
    try:
        for inscan in Inscripcion_Anual.objects.all():
            if inscan.anualidad.descripcion.__len__()>30:
                desc = inscan.anualidad.descripcion[:30]+"..."
            else:
                desc = inscan.anualidad.descripcion
            lista += (str(inscan.id), desc),
    except:
        pass
    return lista

def cargarUsuarios():
    """
    @note: Función que permite cargar los usuarios del sistema
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un listado con todos los usuarios con acceso autorizado al sistema
    """
    lista = ('0', 'Seleccione...'),
    try:
        for usr in User.objects.all():
            lista += (str(usr.id), usr.first_name+" "+usr.last_name+" ["+usr.username+"] "),
    except:
        pass
    return lista

def formatoFecha(fecha):
    """
    @note: Función que permite establecer el formato de las fechas
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param fecha: Variable de tipo string que contiene la fecha a ser formateada
    @return: Retorna una fecha formateada
    """
    fechaformat = str(fecha)[8:10]+"/"+str(fecha)[5:7]+"/"+str(fecha)[:4]
    return fechaformat

def str2bool(cadena):
    """
    @note: Función que permite convertir una cadena de texto en un valor booleano
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param cadena: Variable de tipo string que contiene la cadena de texto a ser convertida a un valor booleano
    @return: Retorna una variable booleana (Verdadero, Falso) de acuerdo a la cadena de texto introducida
    """
    if cadena == 'True':
        booleano = bool(cadena)
    else:
        booleano = bool("")
    return booleano

def compararFechas(fechaini, fechafin):
    """
    @note: Función que permite comparar dos fechas y determinar cual de ellas es mayor o menor
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param fechaini: Variable de tipo date que contiene la fecha inicial a ser evaluada
    @param fechafin: Variable de tipo date que contiene la fecha final a ser evaluada
    @return: Retorna falso si la fecha inicial es mayor a la final, de lo contrario retorna verdadero
    """
    if datetime.strptime(fechaini, "%d/%m/%Y") < datetime.strptime(fechafin, "%d/%m/%Y"):
        return True
    elif datetime.strptime(fechaini, "%d/%m/%Y") > datetime.strptime(fechafin, "%d/%m/%Y"):
        return False
    else:
        return None
    
def cargarDatosConsulta(modelo,get):
    """
    @note: Función que permite cargar la consulta paginada de un módelo dado
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @param modelo: Variable de tipo object que contiene el módelo de la base de datos a consultar
    @param get: Variable de tipo string que contiene el número de la página en la consulta
    @return: Retorna la consulta paginada del módelo indicado
    """
    numero_paginas = 5

    lista = modelo
    if not lista:
        registros=[]
    else:
        paginator = Paginator(lista, numero_paginas)
        
        try:
            page = int(get)
        except ValueError:
            page = 1
    
        try:
            registros = paginator.page(page)
        except (EmptyPage, InvalidPage):
            registros = paginator.page(paginator.num_pages)
    
    return registros

def cargarRequisitosRegistro(modelo):
    modulos = []
    inicio = ''
    
    """
    @note: condiciones para el módulo de institucion
    """
    if modelo=="carrera":
        if not Departamento.objects.all():
            modulos.append('Departamento')
        if modulos:
            inicio='/institucion/inicio/'
    elif modelo=="carrerasede":
        if not Sede.objects.all():
            modulos.append('Sede')
        if not Carrera.objects.all():
            modulos.append('Carrera')
        if modulos:
            inicio = '/institucion/inicio/'
            
    """
    @note:condiciones para el módulo de unidad curricular
    """
    if modelo=="pensum":
        if not Carrera_Sede.objects.all():
            modulos.append('Carrera por sede')
        if modulos:
            inicio='/unidadcurricular/inicio/'
    elif modelo=="unidadcurr":
        if not Pensum.objects.all():
            modulos.append('Pensum')
        if not Condicion_Unidad.objects.all():
            modulos.append('Condición de la Unidad')
        if not Eje_Curricular.objects.all():
            modulos.append('Eje Curricular')
        if not Tipo_Unidad.objects.all():
            modulos.append('Tipo de Unidad')
        if modulos:
            inicio = '/unidadcurricular/inicio/'
    elif modelo=="prelacion" or modelo=="modulocurr":
        if not Unidad_Curricular.objects.all():
            modulos.append("Unidad Curricular")
        if modulos:
            inicio = "/unidadcurricular/inicio/"
    
    """
    @note: condiciones para el módulo academico
    """
    if modelo=="trimestre":
        if not Tipo_Trimestre.objects.all():
            modulos.append("Tipo de Trimestre")
        if modulos:
            inicio = '/academico/inicio/'
    elif modelo=="alumno":
        if not Carrera_Sede.objects.all():
            modulos.append('Carrera por sede')
        if not Condicion_Ingreso.objects.all():
            modulos.append('Condición de Ingreso')
        if not Sistema_Estudio.objects.all():
            modulos.append('Sistema de Estudio')
        if not Titulo_Bachiller.objects.all():
            modulos.append('Titulo de Bachiller')
        if not Trimestre.objects.all():
            modulos.append('Trimestre')
        if not Documento.objects.all():
            modulos.append('Documentos')
        if modulos:
            inicio='/academico/inicio/'
    elif modelo=="anualidadcarr":
        if not Anualidad.objects.all():
            modulos.append("Anualidad")
        if not Carrera_Sede.objects.all():
            modulos.append("Carrera por Sede")
        if modulos:
            inicio='/academico/inicio/'
    elif modelo=="anualidadtricarr":
        if not Anualidad_Carrera.objects.all():
            modulos.append("Anualidad por Carrera")
        if not Trimestre.objects.all():
            modulos.append("Trimestre")
        if modulos:
            inicio='/academico/inicio/'
            
    """
    @note: condiciones para el módulo de horario
    """
    if modelo=="horario":
        if not Dia.objects.all():
            modulos.append("Día")
        if not Hora.objects.all():
            modulos.append("Hora")
        if not Modalidad_Horario.objects.all():
            modulos.append("Modalidad de Horario")
        if modulos:
            inicio='/horario/inicio/'
            
    """
    @note: condiciones para el módulo de planta académica y física
    """
    if modelo=="profesor":
        if not Profesion.objects.all():
            modulos.append("Profesión")
        if not Condicion_Profesor.objects.all():
            modulos.append("Condición del Profesor")
        if modulos:
            inicio='/planta/inicio/'
    elif modelo=="profesorcarr":
        if not Profesor.objects.all():
            modulos.append("Profesor")
        if not Carrera_Sede.objects.all():
            modulos.append("Carrera por Sede")
        if modulos:
            inicio ='/planta/inicio/'
    elif modelo=="profesordisp":
        if not Profesor.objects.all():
            modulos.append("Profesor")
        if not Dia.objects.all():
            modulos.append("Día")
        if not Turno.objects.all():
            modulos.append("Turno")
        if modulos:
            inicio='/planta/inicio/'
    elif modelo=="edificio":
        if not Tipo_Edificio.objects.all():
            modulos.append("Tipo de Edificio")
        if modulos:
            inicio='/planta/inicio/'
    elif modelo=="aula":
        if not Edificio.objects.all():
            modulos.append("Edificio")
        if not Tipo_Aula.objects.all():
            modulos.append("Tipo de Aula")
        if modulos:
            inicio='/planta/inicio/'
    elif modelo=="aulacarr":
        if not Aula.objects.all():
            modulos.append("Aula")
        if not Carrera_Sede.objects.all():
            modulos.append("Carrera por Sede")
        if modulos:
            inicio='/planta/inicio/'
            
    """
    @note: condición para el módulo de seguridad de ingreso de alumnos
    """
    if modelo=="seguridadingalumno":
        if not Carrera_Sede.objects.all():
            modulos.append("Carrera por Sede")
        if modulos:
            inicio='/seguridad/inicio/'
            
    """
    @note: condición para el módulo de planificación
    """
    if modelo=="planificacion":
        if not Anualidad_Tri_Carrera.objects.all():
            modulos.append("Anualidad por Trimestre y Carrera")
        if not Carrera.objects.all():
            modulos.append("Carrera")
        if modulos:
            inicio='/planificacion/inicio/'
    elif modelo=="planificacionunidad":
        if not Planificacion.objects.all():
            modulos.append("Planificación")
        if not Profesor.objects.all():
            modulos.append("Profesor")
        if not Modulo_Curricular.objects.all():
            modulos.append("Módulo Curricular")
        if modulos:
            inicio='/planificacion/inicio/'
            
    """
    @note: condición para el módulo de inscripción
    """
    if modelo=="inscanual":
        if not Estatus_Inscanual.objects.all():
            modulos.append("Estatus de Inscripción Anual")
        if not Alumno.objects.all():
            modulos.append("Alumno")
        if not Anualidad.objects.all():
            modulos.append("Anualidad")
        if not Unidad_Curricular.objects.all():
            modulos.append("Unidad Curricular")
        if modulos:
            inicio='/inscripcion/inicio/'
    elif modelo=="insctrimestral":
        if not Estatus_Insctrimestral.objects.all():
            modulos.append("Estatus de Inscripción Trimestral")
        if not Alumno.objects.all():
            modulos.append("Alumno")
        if not Inscripcion_Anual.objects.all():
            modulos.append("Inscripción Anual")
        if not Modulo_Curricular.objects.all():
            modulos.append("Módulo Curricular")
        if not Trimestre.objects.all():
            modulos.append("Trimestre")
        if modulos:
            inicio='/inscripcion/inicio/'
    elif modelo=="hito":
        if not Alumno.objects.all():
            modulos.append("Alumno")
        if not Inscripcion_Anual.objects.all():
            modulos.append("Inscripción Anual")
        if not Modulo_Curricular.objects.all():
            modulos.append("Módulo Curricular")
        if not Estatus_Inscanual.objects.all():
            modulos.append("Estatus de Inscripción Anual")
        if not Trimestre.objects.all():
            modulos.append("Trimestre")
        if modulos:
            inicio='/inscripcion/inicio/' 
            
    return modulos,inicio