#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comun.models import HistoricoRegistros
from django.contrib.auth.models import User

def dispararEvento(sender, signal, **kwargs):
    datos = kwargs['instance'].datos()[0] #Obtiene los datos que se van a registrar o eliminar
    usuario = kwargs['instance'].datos()[1] #Obtiene el nombre del usuario que esta realizando el registro o eliminación
    modelo = kwargs['instance'].datos()[2] #Obtiene el nombre del modelo que se esta ejecutando
    if 'created' in kwargs.keys(): 
        if not kwargs['created']:
            operacion = "UPDATE"
        else:
            operacion = "INSERT"
    else:
        operacion = "DELETE"
    try:
        usr = User.objects.get(username=str(usuario))
        hostreg = HistoricoRegistros(modelo=modelo, operacion=operacion, datos=datos, usuario=usr)
        hostreg.save()
        #colocar aqui la instruccion para almacenar en el log
        #print "Registros de histórico almacenados"
    except Exception, e:
        #colocar aqui la instruccion para almacenar en el log
        print e.message