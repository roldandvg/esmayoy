# -*- coding: utf-8 -*-
from django.db.models.signals import post_syncdb
from django.db import transaction
from django.utils.translation import ugettext as _
import comun.models as comunmodels
import os

@transaction.commit_on_success
def triggerGeo(sender, **kwargs):
    from comun.models import Pais, Estado, Municipio, Parroquia
    from django.contrib.auth.models import User
    
    if not User.objects.filter(is_staff=True):
        print _(u"Para ingresar datos al sistema debe existir un usuario válido con permisos administrativos")
    else:
        try:
            usr = User.objects.filter(is_staff=True)
            
            print _(u"Por favor espere, se están ingresando los datos básicos de países, estados, municipios y parroquías")
            f = open(os.path.dirname(__file__)+"/datos/paises.txt", "r")
            paises = [valor.replace("\n","") for valor in f]
            f.close()
            
            f = open(os.path.dirname(__file__)+"/datos/estados.txt", "r")
            estados = [valor.replace("\n","") for valor in f]
            f.close()
            
            f = open(os.path.dirname(__file__)+"/datos/municipios.txt", "r")
            municipios = [valor.replace("\n","") for valor in f]
            f.close()
            
            f = open(os.path.dirname(__file__)+"/datos/parroquias.txt", "r")
            parroquias = [valor.replace("\n","") for valor in f]
            f.close()
            
            for pais in paises:
                if not Pais.objects.filter(nombre=pais):
                    Pais(nombre=pais,usuarioreg=usr[0]).save()
                    
            getPais = Pais.objects.get(nombre='Venezuela')
            
            for edo in estados:
                datos = edo.split(",")
                if not Estado.objects.filter(nombre=datos[1],pais=getPais):
                    Estado(id=datos[0],nombre=datos[1],pais=getPais,usuarioreg=usr[0]).save()
                    
            for mun in municipios:
                datos = mun.split(",")
                getEstado = Estado.objects.get(id=datos[2])
                if not Municipio.objects.filter(nombre=datos[1],estado=getEstado):
                    Municipio(id=datos[0],nombre=datos[1],estado=getEstado,usuarioreg=usr[0]).save()
                    
            for parr in parroquias:
                datos = parr.split(",")
                getMunicipio = Municipio.objects.get(id=datos[2])
                if not Parroquia.objects.filter(nombre=datos[1],municipio=getMunicipio):
                    Parroquia(id=datos[0],nombre=datos[1],municipio=getMunicipio,usuarioreg=usr[0]).save()
                    
            print _(u"Se ingresaron los datos de países, estados, municipios y parroquías")
                    
        except Exception, e:
            print _(u"Error al registrar los datos de países, estados, municipios y parroquías. Detalles del error: %s" % e)
            
post_syncdb.connect(triggerGeo,sender=comunmodels)