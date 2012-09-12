# -*- coding: utf-8 -*-
from dajax.core import Dajax
from django.utils.translation import ugettext as _
from django.db import transaction
from unidadcurricular.models import Pensum, Eje_Curricular, Condicion_Unidad, Tipo_Unidad, Unidad_Curricular, Prelacion, Modulo_Curricular
from comun.funciones import formatoFecha

def mostrarDatosPensum(request):
    dajax = Dajax()
    id = request.POST['pensum']
    pe = Pensum.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_pensum", "value")
    dajax.clear("#descripcion", "value")
    dajax.clear("#finicio", "value")
    dajax.clear("#ffinal", "value")
    dajax.clear("#cal_min", "value")
    dajax.clear("#cal_max", "value")
    dajax.clear("#cal_apro", "value")
    dajax.clear("#modificar", "value")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#cod_pensum", "value", str(pe.cod_pensum))
    dajax.assign("#cod_pensum","readOnly","readonly")
    dajax.assign("#descripcion", "value", str(pe.descripcion))
    dajax.assign("#finicio", "value", str(formatoFecha(pe.finicio)))
    dajax.assign("#ffinal", "value", str(formatoFecha(pe.ffinal)))
    dajax.assign("#cal_min", "value", str(pe.cal_min))
    dajax.assign("#cal_max", "value", str(pe.cal_max))
    dajax.assign("#cal_apro", "value", str(pe.cal_apro))
    dajax.assign("#modificar", "value", str(pe.id))
    dajax.script("document.getElementById('estatus').value='"+str(pe.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.assign("#carrsed","value",pe.carrerasede.id)
    dajax.assign("#carrsed","selected",True)
    if not pe.observaciones is None:
        dajax.assign("#observaciones", "value", str(pe.observaciones))
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,11):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosEje(request):
    dajax = Dajax()
    id = request.POST['eje']
    eje = Eje_Curricular.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_eje", "value")
    dajax.clear("#descripcion", "value")
    dajax.clear("#modificar", "value")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#cod_eje", "value", str(eje.cod_eje))
    dajax.assign("#cod_eje", "readOnly", "readonly")
    dajax.assign("#descripcion", "value", str(eje.descripcion))
    dajax.assign("#modificar", "value", str(eje.cod_eje))
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,3):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosCondicion(request):
    dajax = Dajax()
    id = request.POST['cond']
    cond = Condicion_Unidad.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cond_unidad", "value")
    dajax.clear("#descripcion", "value")
    dajax.clear("#modificar", "value")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#cond_unidad", "value", str(cond.cond_unidad))
    dajax.assign("#cond_unidad", "readOnly", "readonly")
    dajax.assign("#descripcion", "value", str(cond.descripcion))
    dajax.assign("#modificar", "value", str(cond.cond_unidad))
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,3):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosTipoUnidad(request):
    dajax = Dajax()
    id = request.POST['tpu']
    tpu = Tipo_Unidad.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#descripcion", "value")
    dajax.clear("#modificar", "value")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#descripcion", "value", str(tpu.descripcion))
    dajax.assign("#modificar", "value", str(tpu.id))
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    dajax.clear("#e1", "innerHTML")
    return dajax

def mostrarDatosUnidad(request):
    dajax = Dajax()
    id = request.POST['unidad']
    und = Unidad_Curricular.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#id_unidad", "value")
    dajax.clear("#cod_unidad", "value")
    dajax.clear("#nombre", "value")
    dajax.clear("#ucr", "value")
    dajax.clear("#pre_ucr", "value")
    dajax.clear("#trayecto", "value")
    dajax.clear("#trimestre", "value")
    dajax.clear("#cant_mod", "value")
    dajax.clear("#modificar", "value")
    dajax.script("document.getElementById('obligatoria').value='True'")
    dajax.script("document.getElementById('obligatoria').selected=true")
    dajax.script("document.getElementById('estatus').value='True'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('hilo').value='True'")
    dajax.script("document.getElementById('hilo').selected=true")
    dajax.script("document.getElementById('pensum').value='0'")
    dajax.script("document.getElementById('pensum').selected=true")
    dajax.script("document.getElementById('condicionunidad').value='0'")
    dajax.script("document.getElementById('condicionunidad').selected=true")
    dajax.script("document.getElementById('ejecurricular').value='0'")
    dajax.script("document.getElementById('ejecurricular').selected=true")
    dajax.script("document.getElementById('tipounidad').value='0'")
    dajax.script("document.getElementById('tipounidad').selected=true")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#id_unidad", "value", str(und.id_unidad))
    dajax.assign("#id_unidad", "readOnly", "readonly")
    dajax.assign("#modificar", "value", str(und.id_unidad))
    dajax.assign("#cod_unidad", "value", str(und.cod_unidad))
    dajax.assign("#nombre", "value", str(und.nombre))
    dajax.assign("#ucr", "value", str(und.ucr))
    dajax.assign("#pre_ucr", "value", str(und.pre_ucr))
    dajax.assign("#trayecto", "value", str(und.trayecto))
    dajax.assign("#trimestre", "value", str(und.trimestre))
    dajax.assign("#cant_mod", "value", str(und.cant_mod))
    dajax.script("document.getElementById('obligatoria').value='"+str(und.obligatoria)+"'")
    dajax.script("document.getElementById('obligatoria').selected=true")
    dajax.script("document.getElementById('estatus').value='"+str(und.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('hilo').value='"+str(und.hilo)+"'")
    dajax.script("document.getElementById('hilo').selected=true")
    dajax.script("document.getElementById('pensum').value='"+str(und.pensum.id)+"'")
    dajax.script("document.getElementById('pensum').selected=true")
    dajax.script("document.getElementById('condicionunidad').value='"+str(und.condicionunidad.cond_unidad)+"'")
    dajax.script("document.getElementById('condicionunidad').selected=true")
    dajax.script("document.getElementById('ejecurricular').value='"+str(und.ejecurricular.cod_eje)+"'")
    dajax.script("document.getElementById('ejecurricular').selected=true")
    dajax.script("document.getElementById('tipounidad').value='"+str(und.tipounidad.id)+"'")
    dajax.script("document.getElementById('tipounidad').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,16):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosPrelacion(request):
    dajax = Dajax()
    id = request.POST['pre']
    pre = Prelacion.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_prela", "value")
    dajax.clear("#modificar", "value")
    dajax.script("document.getElementById('estatus').value='True'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('unidadcurr').value='0'")
    dajax.script("document.getElementById('unidadcurr').selected=true")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#cod_prela", "value", str(pre.cod_prela))
    dajax.assign("#cod_prela", "readOnly", "readonly")
    dajax.assign("#modificar", "value", str(pre.cod_prela))
    dajax.script("document.getElementById('estatus').value='"+str(pre.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('unidadcurr').value='"+str(pre.unidadcurricular.id_unidad)+"'")
    dajax.script("document.getElementById('unidadcurr').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,4):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosModulocurr(request):
    dajax = Dajax()
    id = request.POST['modulo']
    mod = Modulo_Curricular.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_modulo", "value")
    dajax.clear("#modificar", "value")
    dajax.clear("#nombre", "value")
    dajax.clear("#ucr", "value")
    dajax.clear("#porcentaje", "value")
    dajax.clear("#trayecto", "value")
    dajax.clear("#trimestre", "value")
    dajax.script("document.getElementById('estatus').value='True'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('unidadcurr').value='0'")
    dajax.script("document.getElementById('unidadcurr').selected=true")
    
    #--- Se asignan los valores correspondiente de acuerdo al registro seleccionado
    dajax.assign("#cod_modulo", "value", str(mod.cod_modulo))
    dajax.assign("#cod_modulo", "readOnly", "readonly")
    dajax.assign("#modificar", "value", str(mod.cod_modulo))
    dajax.assign("#nombre", "value", str(mod.nombre))
    dajax.assign("#ucr", "value", str(mod.ucr))
    dajax.assign("#porcentaje", "value", str(mod.porcentaje))
    dajax.assign("#trayecto", "value", str(mod.trayecto))
    dajax.assign("#trimestre", "value", str(mod.trimestre))
    dajax.script("document.getElementById('estatus').value='"+str(mod.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('unidadcurr').value='"+str(mod.unidadcurricular.id_unidad)+"'")
    dajax.script("document.getElementById('unidadcurr').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,9):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def confirmarEliminar(request):
    """
    @note: Función que permite confirmar si los datos seleccionados serán eliminados
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax con un mensaje de confirmación al usuario. En caso de respuesta afirmativa ejecuta la función de eliminar los datos
    """
    dajax = Dajax()
    opcion = request.POST['opcion']
    id = request.POST['id']
    dajax.script("if (confirm('"+_(u"Esta seguro de eliminar este registro")+"?')) Dajax.unidadcurricular_eliminarDatos({'opcion':'"+opcion+"', 'id':'"+id+"'})")
    return dajax

@transaction.commit_on_success
def eliminarDatos(request):
    """
    @note: Función que permite eliminar los datos del registro seleccionado
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax con un mensaje al usuario que le indica el estatus de la eliminación de los registros
    """
    dajax = Dajax()
    opcion = request.POST['opcion']
    id = request.POST['id']
    objetos = []
    try:
        if opcion=="pensum":
            pe = Pensum.objects.get(pk=id)
            pe.delete()
            objetos = Pensum.objects.all()
        elif opcion=="eje":
            eje = Eje_Curricular.objects.get(pk=id)
            eje.delete()
            objetos = Eje_Curricular.objects.all()
        elif opcion=="cond":
            cond = Condicion_Unidad.objects.get(pk=id)
            cond.delete()
            objetos = Condicion_Unidad.objects.all()
        elif opcion=="tpu":
            tpu = Tipo_Unidad.objects.get(pk=id)
            tpu.delete()
            objetos = Tipo_Unidad.objects.all()
        elif opcion=="unidad":
            und = Unidad_Curricular.objects.get(pk=id)
            und.delete()
            objetos = Unidad_Curricular.objects.all()
        elif opcion=="pre":
            pre = Prelacion.objects.get(pk=id)
            pre.delete()
            objetos = Prelacion.objects.all()
        elif opcion=="modulo":
            mod = Modulo_Curricular.objects.get(pk=id)
            mod.delete()
            objetos = Modulo_Curricular.objects.all()
        dajax.remove("#"+id)
        if not objetos:
            dajax.clear("#registros","innerHTML")
        dajax.alert(_(u"Registros eliminados con éxito"))
    except Exception, e:
        dajax.alert(_(u"Los registros no se pueden eliminar. Error: ")+e.message)
    return dajax