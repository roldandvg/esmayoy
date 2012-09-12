#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from configuracion.models import Parametro

class FormParametro(forms.Form):
    idparametro = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title': _(u'Indique el id del parámetro'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la descripción'), 'tabindex':'2'}))
    vnum = forms.DecimalField(label=_(u"Número:"), widget=forms.TextInput(attrs={'size':'20','maxlength':'20', 'title':_(u'Indique el número de validación'), 'tabindex':'3'}), required=False)
    vdate = forms.DateField(('%d/%m/%Y',), label=_(u"Fecha:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'readonly':'readonly', 'title':_(u'Indique la fecha de validación'), 'tabindex':'4'}), required=False)
    vstring = forms.CharField(label=_(u"Cadena:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique la cadena de validación'), 'tabindex':'5'}), required=False)
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid    = "<div id='ayudaid'    class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En este campo se debe indicar el identificador del parámetro a registrar. La longitud máxima es de 20 carácteres. Este campo es obligatorio.")
    helpdes   = "<div id='ayudades'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique en este campo una descripción detallada del parámetro a registrar. Solo se permiten carácteres alfanuméricos con una longitud máxima de 100. Este campo es obligatorio.")
    helpvnum  = "<div id='ayudavnum'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique en este campo el número de validaciones a realizar. La longitud máxima es de 20 carácteres numéricos. Este campo es opcional.")
    helpvdate = "<div id='ayudavdate' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la fecha de validación. Este campo no es editable y sólo se pueden ingresar datos a través del calendario. Este campo es opcional.")
    helpvstr  = "<div id='ayudavstr'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la cadena de validación con una longitud máxima de 45 carácteres. Este campo es opcional.")
    
    def clean_idparametro(self):
        idparametro = self.cleaned_data['idparametro']
        modificar=self.data['modificar']
        if Parametro.objects.filter(pk=idparametro) and modificar=="":
            raise forms.ValidationError(_(u"El ID ya existe"))
        return self.cleaned_data['idparametro']