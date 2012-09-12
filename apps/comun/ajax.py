# -*- coding: utf-8 -*-
from dajax.core import Dajax
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from comun.models import Estado, Municipio, Parroquia
from institucion.models import Carrera_Sede, Carrera, Sede, Departamento
from academico.models import Alumno, Anualidad, Anualidad_Carrera, Anualidad_Tri_Carrera, Documento, Tipo_Trimestre, Trimestre
from configuracion.models import Parametro
from horario.models import Dia, Hora, Horario, Modalidad_Horario, Turno
from inscripcion.models import Estatus_Inscanual, Estatus_Insctrimestral, Hito, Inscripcion_Anual, Inscripcion_Trimestral
from planificacion.models import Planificacion, Planificacion_Unidad
from planta.academica.models import Profesion, Condicion_Profesor, Profesor, Profesor_Carrera, Profesor_Disponibilidad
from planta.fisica.models import Tipo_Aula, Tipo_Edificio, Edificio, Aula, Aula_Carrera
from unidadcurricular.models import Pensum, Eje_Curricular, Condicion_Unidad, Tipo_Unidad, Unidad_Curricular, Prelacion, Modulo_Curricular
from usuario.models import Seguridad_Ingreso_Alumnos

def cargarEstados(request):
    dajax = Dajax()
    idPais = request.POST['pais']
    option = "<option value='0'>Seleccione...</option>"
    for edo in Estado.objects.filter(pais=idPais):
        option += "<option value='%s'>%s</option>" % (edo.id, edo.nombre)
    dajax.assign("#estado", "innerHTML", option)
    if idPais=="0":
        dajax.assign("#municipio", "innerHTML", option)
        dajax.assign("#parroquia", "innerHTML", option)
    return dajax

def cargarMunicipios(request):
    dajax = Dajax()
    idEstado = request.POST['estado']
    option = "<option value='0'>Seleccione...</option>"
    for mun in Municipio.objects.filter(estado=idEstado):
        option += "<option value='%s'>%s</option>" % (mun.id, mun.nombre)
    dajax.assign("#municipio", "innerHTML", option)
    if idEstado=="0":
        dajax.assign("#parroquia", "innerHTML", option)
    return dajax

def cargarParroquias(request):
    dajax = Dajax()
    idMunicipio = request.POST['municipio']
    option = "<option value='0'>Seleccione...</option>"
    for parr in Parroquia.objects.filter(municipio=idMunicipio):
        option += "<option value='%s'>%s</option>" % (parr.id, parr.nombre)
    dajax.assign("#parroquia", "innerHTML", option)
    return dajax

def eliminarRegistro(request):
    dajax = Dajax()
    opcion = request.POST['opcion']
    id = request.POST['id']
    try:
        if opcion == 'usuario':
            reg = User.objects.get(pk=id)
            sitio = "/usuario/"
        elif opcion == 'seguridad_ingreso_alumno':
            reg = Seguridad_Ingreso_Alumnos.objects.get(pk=id)
            sitio = '/seguridad'
        elif opcion == 'documento':
            reg = Documento.objects.get(pk=id)
            sitio = '/academico/documento/'
        elif opcion == 'tipo_trimestre':
            reg = Tipo_Trimestre.objects.get(pk=id)
            sitio = '/academico/tipotri/'
        elif opcion == 'trimestre':
            reg = Trimestre.objects.get(pk=id)
            sitio = '/academico/trimestre/'
        elif opcion == 'alumno':
            reg = Alumno.objects.get(pk=id)
            sitio = '/academico/alumno/'
        elif opcion == 'anualidad':
            reg = Anualidad.objects.get(pk=id)
            sitio = '/academico/anualidad/'
        elif opcion == 'anualidad_carrera':
            reg = Anualidad_Carrera.objects.get(pk=id)
            sitio = '/academico/anualidad/carrera/'
        elif opcion == 'anualidad_tri_carrera':
            reg = Anualidad_Tri_Carrera.objects.get(pk=id)
            sitio = '/academico/anualidad/trimestre/'
        elif opcion == 'parametro':
            reg = Parametro.objects.get(pk=id)
            sitio = '/config/parametro/'
        elif opcion == 'dia':
            reg = Dia.objects.get(pk=id)
            sitio = '/horario/dia/'
        elif opcion == 'hora':
            reg = Hora.objects.get(pk=id)
            sitio = '/horario/hora/'
        elif opcion == 'horario':
            reg = Horario.objects.get(pk=id)
            sitio = '/horario/horario/'
        elif opcion == 'modalidad_horario':
            reg = Modalidad_Horario.objects.get(pk=id)
            sitio = '/horario/modalidad/'
        elif opcion == 'turno':
            reg = Turno.objects.get(pk=id)
            sitio = '/horario/turno/'
        elif opcion == 'estatus_inscanual':
            reg = Estatus_Inscanual.objects.get(pk=id)
            sitio = '/inscripcion/estatus/anual/'
        elif opcion == 'estatus_insctrim':
            reg = Estatus_Insctrimestral.objects.get(pk=id)
            sitio = '/inscripcion/estatus/trimestral/'
        elif opcion == 'hito':
            reg = Hito.objects.get(pk=id)
            sitio = '/inscripcion/hito/'
        elif opcion == 'inscanual':
            reg = Inscripcion_Anual.objects.get(pk=id)
            sitio = '/inscripcion/anual/'
        elif opcion == 'insctrimestral':
            reg = Inscripcion_Trimestral.objects.get(pk=id)
            sitio = '/inscripcion/trimestral/'
        elif opcion == 'carrera':
            reg = Carrera.objects.get(pk=id)
            sitio = '/institucion/carrera/'
        elif opcion == 'carrera_sede':
            reg = Carrera_Sede.objects.get(pk=id)
            sitio = '/institucion/carrsede/'
        elif opcion == 'departamento':
            reg = Departamento.objects.get(pk=id)
            sitio = '/institucion/dpto/'
        elif opcion == 'sede':
            reg = Sede.objects.get(pk=id)
            sitio = '/institucion/sede/'
        elif opcion == 'planificacion':
            reg = Planificacion.objects.get(pk=id)
            sitio = '/planificacion/planificar/'
        elif opcion == 'planificacion_unidad':
            reg = planificacion_Unidad.objects.get(pk=id)
            sitio = '/planificacion/planificar/unidad/'
        elif opcion == 'condicion_profesor':
            reg = Condicion_Profesor.objects.get(pk=id)
            sitio = '/planta/academica/condprof'
        elif opcion == 'profesor_carrera':
            reg = Profesor_Carrera.objects.get(pk=id)
            sitio = '/planta/academica/profesorcarr'
        elif opcion == 'profesor_disponibilidad':
            reg = Profesor_Disponibilidad.objects.get(pk=id)
            sitio = '/planta/academica/profesordisp'
        elif opcion == 'profesion':
            reg = Profesion.objects.get(pk=id)
            sitio = '/planta/academica/profesion'
        elif opcion == 'profesor':
            reg = Profesor.objects.get(pk=id)
            sitio = '/planta/academica/profesor'
        elif opcion == 'aula':
            reg = Aula.objects.get(pk=id)
            sitio = '/planta/fisica/aula'
        elif opcion == 'aula_carrera':
            reg = Aula_Carrera.objects.get(pk=id)
            sitio = '/planta/fisica/aulacarrera'
        elif opcion == 'edificio':
            reg = Edificio.objects.get(pk=id)
            sitio = '/planta/fisica/edificio'
        elif opcion == 'tipo_aula':
            reg = Tipo_Aula.objects.get(pk=id)
            sitio = '/planta/fisica/tipoaula'
        elif opcion == 'tipo_edificio':
            reg = Tipo_Edificio.objects.get(pk=id)
            sitio = '/planta/fisica/tipoedificio'
        elif opcion == 'unidad_curricular':
            reg = Unidad_Curricular.objects.get(pk=id)
            sitio = '/unidadcurricular/unidadcurr/'
        elif opcion == 'condicion_unidad':
            reg = Condicion_Unidad.objects.get(pk=id)
            sitio = '/unidadcurricular/conduni/'
        elif opcion == 'eje_curricular':
            reg = Eje_Curricular.objects.get(pk=id)
            sitio = '/unidadcurricular/ejecurr/'
        elif opcion == 'modulo_curricular':
            reg = Modulo_Curricular.objects.get(pk=id)
            sitio = '/unidadcurricular/modcurr/'
        elif opcion == 'pensum':
            reg = Pensum.objects.get(pk=id)
            sitio = '/unidadcurricular/pensum/'
        elif opcion == 'prelacion':
            reg = Prelacion.objects.get(pk=id)
            sitio = '/unidadcurricular/prelacion/'
        elif opcion == 'tipo_unidadcurr':
            reg = Tipo_Unidad.objects.get(pk=id)
            sitio = '/unidadcurricular/tipounicurr/'
        
        reg.delete()
        #dajax.redirect(sitio)
        dajax.script("exitoEliminar('"+sitio+"')")
    except Exception, e:
        print e
        dajax.script("errorEliminar()")
    
    return dajax