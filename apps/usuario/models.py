#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento

class Seguridad_Ingreso_Alumnos(models.Model):
    validar_seg = models.BooleanField()
    validar_fecha = models.BooleanField()
    finicio = models.DateField(null=True)
    ffinal = models.DateField(null=True)
    validar_cantalumn = models.BooleanField()
    cant_alumnos = models.IntegerField(null=True)
    contador_cantidad = models.IntegerField(null=True)
    fecha_operacion = models.DateField()
    #usuario = models.ForeignKey(User, db_column='id_usuario_sia') #Usuario que puede registrar alumnos
    carrera_sede = models.ForeignKey(Carrera_Sede, db_column='id_carrerasede')
    username = models.CharField(max_length=45)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Seguridad para el Ingreso de Alumno")
        verbose_name_plural = _(u"Seguridad para los Ingresos de Alumnos")
        ordering = ["finicio","ffinal"]
        
    def datos(self):
        cadena = "id=%s, validar_seg=%s, validar_fecha=%s, finicio=%s, ffinal=%s, " % (self.pk, self.validar_seg, self.validar_fecha, self.finicio, self.ffinal)
        cadena+= "validar_cantalumn=%s, cant_alumnos=%s, contador_cantidad=%s, " % (self.validar_cantalumn, self.cant_alumnos, self.contador_cantidad)
        cadena+= "fecha_operacion=%s, carrera_sede=%s, username=%s" % (self.fecha_operacion, self.carrera_sede.id, self.username.id)
        return [cadena, self.usuarioreg.username, "Seguridad_Ingreso_Alumnos"]

#Agrega un campo de modificación de contraseñas para establecer la expiración de las mismas
User.add_to_class('fecha_modpass',models.DateTimeField(null=True))
    
#Dispara el registro de eventos para el modelo de Seguridad_Ingreso_Alumnos
post_save.connect(dispararEvento,Seguridad_Ingreso_Alumnos,post_save)
post_delete.connect(dispararEvento, Seguridad_Ingreso_Alumnos, post_delete)