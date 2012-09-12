# -*- coding: utf-8 -*-
from dajax.core import Dajax
from usuario.views import generarCaptcha
from django.contrib.auth.models import User

def habilitarFechas(request):
    dajax = Dajax()
    opcion = request.POST["opcion"]
    if opcion=="True":
        dajax.script("document.getElementById('finicio').disabled=false")
        dajax.script("document.getElementById('ffinal').disabled=false")
        dajax.script("document.getElementById('calfinicio').style.display='block'")
        dajax.script("document.getElementById('calffinal').style.display='block'")
    else:
        dajax.script("document.getElementById('finicio').disabled=true")
        dajax.script("document.getElementById('ffinal').disabled=true")
        dajax.script("document.getElementById('calfinicio').style.display='none'")
        dajax.script("document.getElementById('calffinal').style.display='none'")
    return dajax

def habilitarCant(request):
    dajax = Dajax()
    opcion = request.POST["opcion"]
    if opcion == "True":
        dajax.script("document.getElementById('cant_alumnos').disabled=false")
    else:
        dajax.script("document.getElementById('cant_alumnos').disabled=true")
        dajax.assign("#cant_alumnos","value","")
    return dajax

def reloadCaptcha(request):
    """
    @note: Función que permite cargar una nueva imagen captcha
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    @return: Retorna una nueva imagen captcha
    """
    dajax = Dajax()
    datosCaptcha = generarCaptcha()
    dajax.assign('#divImgcaptcha','innerHTML',datosCaptcha[0])
    dajax.assign('#imghash','value',datosCaptcha[1])
    dajax.assign("#tmp","value",datosCaptcha[2])
    return dajax

def mostrarDatosUsuario(request):
    dajax = Dajax()
    id = request.POST['usuario']
    usr = User.objects.get(pk=id)
    if not usr.first_name:
        nombre = "Administrador"
    else:
        nombre = usr.first_name
    if not usr.last_name:
        apellido = "Administrador"
    else:
        apellido = usr.last_name
    dajax.assign("#modificar","value",str(id))
    dajax.assign("#nombre", "value", nombre)
    dajax.assign("#apellido", "value", apellido)
    dajax.assign("#correo", "value", str(usr.email))
    dajax.assign("#usuario", "value", str(usr.username))
    dajax.assign("#activo", "value", str(usr.is_active))
    dajax.assign("#activo","selected",True)
    for i in range(1,8):
        dajax.clear("e"+str(i), "innerHTML")
    return dajax