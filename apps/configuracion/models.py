#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from django.utils.translation import ugettext as _
from comun.disparadores import dispararEvento

class Parametro(models.Model):
    idparametro = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=100)
    vnum = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    vdate = models.DateField(null=False)
    vstring = models.CharField(max_length=45, null=True)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Parámetro")
        verbose_name_plural = _(u"Parámetros")
        
    def datos(self):
        cadena = "idparametro=%s, descripcion=%s, vnum=%s, vdate=%s, vstring=%s" % (self.pk, self.descripcion, self.vnum, self.vdate, self.vstring)
        return [cadena, self.usuarioreg.username, "Parametro"]
    
#Dispara el registro de eventos para el modelo de Parametro
post_save.connect(dispararEvento,Parametro,post_save)
post_delete.connect(dispararEvento, Parametro, post_delete)