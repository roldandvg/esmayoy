# -*- coding: utf-8 -*-
from dajax.core import Dajax
from django.db import transaction, models
from django.utils.translation import ugettext as _
from institucion.models import Sede, Departamento, Carrera, Carrera_Sede
from comun.funciones import formatoFecha

def mostrarDatosSede(request):
    """
    @note: Función que permite mostrar los datos de la sede para su modificación
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax que muestra los datos de la sede seleccionada
    """
    dajax = Dajax()
    id = request.POST['sede']
    sede = Sede.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_sede", "value")
    dajax.clear("#modificar", "value")
    dajax.clear("#descripcion", "value")
    dajax.clear("#direccion", "value")
    dajax.clear("#telefonos", "value")
    dajax.clear("#fcreacion", "value")
    dajax.clear("#contacto", "value")
    dajax.clear("#email", "value")
    
    #--- Se asignan los valores correspondiente de acuerdo a la sede seleccionada
    dajax.assign("#cod_sede", "value", str(sede.cod_sede))
    dajax.assign("#cod_sede","readOnly","readonly")
    dajax.assign("#modificar","value",str(sede.cod_sede))
    dajax.assign("#descripcion", "value", str(sede.descripcion))
    
    if not sede.direccion is None:
        dajax.assign("#direccion", "value", str(sede.direccion))
    if not sede.telefonos is None:
        dajax.assign("#telefonos", "value", str(sede.telefonos))
    if not sede.fcreacion is None:
        fecha = formatoFecha(sede.fcreacion)
        dajax.assign("#fcreacion", "value", str(fecha))
    if not sede.contacto is None:
        dajax.assign("#contacto", "value", str(sede.contacto))
    if not sede.email is None:
        dajax.assign("#email", "value", str(sede.email))
    dajax.script("document.getElementById('estatus').value='"+str(sede.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,9):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosDpto(request):
    """
    @note: Función que permite mostrar los datos de los departamentos
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax que muestra los datos del departamento seleccionado
    """
    dajax = Dajax()
    id = request.POST['dpto']
    dpto = Departamento.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_dep", "value")
    dajax.clear("#modificar", "value")
    dajax.clear("#descripcion", "value")
    dajax.clear("#contacto", "value")
    
    #--- Se asignan los valores del departamento seleccionado
    dajax.assign("#cod_dep", "value", str(dpto.cod_dep))
    dajax.assign("#cod_dep", "readOnly", "readonly")
    dajax.assign("#descripcion", "value", str(dpto.descripcion))
    dajax.assign("#modificar","value",str(dpto.cod_dep))
    if not dpto.contacto is None:
        dajax.assign("#contacto", "value", str(dpto.contacto))
    dajax.script("document.getElementById('estatus').value='"+str(dpto.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,5):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosCarrera(request):
    """
    @note: Función que permite mostrar los datos de las carreras
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax que muestra los datos de la carrera seleccionada
    """
    dajax = Dajax()
    id = request.POST['carrera']
    car = Carrera.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.clear("#cod_carrera", "value")
    dajax.clear("#descripcion", "value")
        
    #--- Se asignan los valores de la carrera seleccionada
    dajax.assign("#cod_carrera", "value", str(car.cod_carrera))
    dajax.assign("#cod_carrera", "readOnly", "readonly")
    dajax.assign("#modificar", "value", str(car.cod_carrera))
    dajax.assign("#descripcion", "value", str(car.descripcion))
    dajax.script("document.getElementById('estatus').value='"+str(car.estatus)+"'")
    dajax.script("document.getElementById('estatus').selected=true")
    dajax.script("document.getElementById('departamento').value='"+str(car.departamento.cod_dep)+"'")
    dajax.script("document.getElementById('departamento').selected=true")
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,5):
        dajax.clear("#e"+str(i), "innerHTML")
    return dajax

def mostrarDatosCarreraSede(request):
    """
    @note: Función que permite mostrar los datos de las carreras por sedes
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna un objeto dajax que muestra los datos de la carrera por sede seleccionada
    """
    dajax = Dajax()
    id = request.POST['carrerasede']
    carxsed = Carrera_Sede.objects.get(pk=id)
    #--- Se inicializan los valores de los campos del formulario
    dajax.script("document.getElementById('sede').value='0'")
    dajax.script("document.getElementById('sede').selected=true")
    dajax.script("document.getElementById('carrera').value='0'")
    dajax.script("document.getElementById('carrera').selected=true")
    dajax.script("document.getElementById('prefijo_sede').value='True'")
    dajax.script("document.getElementById('prefijo_sede').selected=true")
    dajax.script("document.getElementById('prefijo_carrera').value='True'")
    dajax.script("document.getElementById('prefijo_carrera').selected=true")
    dajax.clear("#nro_carnet", "value")
    dajax.assign("#cant_carnet","value","0")
    dajax.clear("#format_carnet","value")
    
    #--- Se asignan los valores del registro seleccionado
    dajax.assign("#modificar", "value", str(carxsed.id))
    dajax.script("document.getElementById('sede').value='"+str(carxsed.sede.cod_sede)+"'")
    dajax.script("document.getElementById('sede').selected=true")
    dajax.script("document.getElementById('carrera').value='"+str(carxsed.carrera.cod_carrera)+"'")
    dajax.script("document.getElementById('carrera').selected=true")
    dajax.script("document.getElementById('prefijo_sede').value='"+str(carxsed.prefijo_sede)+"'")
    dajax.script("document.getElementById('prefijo_sede').selected=true")
    dajax.script("document.getElementById('prefijo_carrera').value='"+str(carxsed.prefijo_carrera)+"'")
    dajax.script("document.getElementById('prefijo_carrera').selected=true")
    dajax.assign("#nro_carnet", "value", str(carxsed.nro_carnet))
    dajax.assign("#cant_carnet", "value", str(carxsed.cant_carnet))
    dajax.assign("#format_carnet", "value", str(carxsed.format_carnet))
    
    #--- Se elimina cualquier mensaje de error producido por eventos anteriores
    for i in range(1,8):
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
    dajax.script("if (confirm('"+_(u"Esta seguro de eliminar este registro")+"?')) Dajax.institucion_eliminarDatos({'opcion':'"+opcion+"', 'id':'"+id+"'})")
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
        if opcion=="sede":
            sede = Sede.objects.get(pk=id)
            sede.delete()
            objetos = Sede.objects.all()
        elif opcion=="dpto":
            dpto = Departamento.objects.get(pk=id)
            dpto.delete()
            objetos = Departamento.objects.all()
        elif opcion=="carrera":
            carr = Carrera.objects.get(pk=id)
            carr.delete()
            objetos = Carrera.objects.all()
        elif opcion=="carrerasede":
            carsed = Carrera_Sede.objects.get(pk=id)
            carsed.delete()
            objetos = Carrera_Sede.objects.all()
        dajax.remove("#"+id)
        if not objetos:
            dajax.clear("#registros","innerHTML")
        dajax.alert(_(u"Registros eliminados con éxito"))
    except Exception, e:
        dajax.alert(_(u"Los registros no se pueden eliminar. Error: ")+e.message)
    return dajax