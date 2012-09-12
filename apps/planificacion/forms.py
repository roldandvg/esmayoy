#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS
from comun.funciones import cargarAnualidadTriCarreras, cargarCarreras, cargarPlanificaciones, cargarProfesores, cargarModulosCurr

class FormPlanificacion(forms.Form):
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique la descripción de la planificación'), 'tabindex':'3'}))
    fregistro = forms.DateField(('%d/%m/%Y',), label=_(u"Fecha de registro:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de registro'), 'readonly':'readonly', 'tabindex':'5'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones'), 'tabindex':'4'}), required=False)
    anualidad_trimestre = forms.ChoiceField(label=_(u"Anualidad por Trimestre:"), choices=cargarAnualidadTriCarreras(), widget=forms.Select(attrs={'title':_(u'Seleccione la anualidad de acuerdo a la carrera a planificar'), 'tabindex':'1'}))
    carrera = forms.ChoiceField(label=_(u"Carrera:"), choices=cargarCarreras(), widget=forms.Select(attrs={'title':_(u'Seleccione la carrera'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfre = "<div id='ayudafre' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpanu = "<div id='ayudaanu' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcar = "<div id='ayudacar' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormPlanificacion, self).__init__(*args, **kwargs)
        self.fields['anualidad_trimestre'].choices = cargarAnualidadTriCarreras()
        self.fields['carrera'].choices = cargarCarreras()
        
    def clean_anualidad_trimestre(self):
        anualtri = self.cleaned_data['anualidad_trimestre']
        if anualtri=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la anualidad"))
        return self.cleaned_data['anualidad_trimestre']
    
    def clean_carrera(self):
        carrera = self.cleaned_data['carrera']
        if carrera=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrera']
        
class FormPlanificacionUnidad(forms.Form):
    seccion = forms.CharField(label=_(u"Sección:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title': _(u'Indique la sección'), 'tabindex':'4'}))
    cant_alumnos = forms.IntegerField(label=_(u"Cant. Alumnos:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la cantidad de alumnos'), 'tabindex':'5'}))
    cupo = forms.IntegerField(label=_(u"Cupos:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique los cupos disponibles'), 'tabindex':'6'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones'), 'tabindex':'8'}), required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'7'}))
    planificacion = forms.ChoiceField(label=_(u"Planificación:"), choices=cargarPlanificaciones(), widget=forms.Select(attrs={'title':_(u'Seleccione una planificación'), 'tabindex':'1'}))
    profesor = forms.ChoiceField(label=_(u"Profesor:"), choices=cargarProfesores(), widget=forms.Select(attrs={'title':_(u'Seleccione un profesor'), 'tabindex':'3'}))
    modulo = forms.ChoiceField(label=_(u"Módulo curricular:"), choices=cargarModulosCurr(), widget=forms.Select(attrs={'title':_(u'Seleccione un módulo curricular'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpsec = "<div id='ayudasec' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcal = "<div id='ayudacal' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcup = "<div id='ayudacup' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppla = "<div id='ayudapla' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppro = "<div id='ayudapro' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpmod = "<div id='ayudamod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormPlanificacionUnidad, self).__init__(*args, **kwargs)
        self.fields['planificacion'].choices = cargarPlanificaciones()
        self.fields['profesor'].choices = cargarProfesores()
        self.fields['modulo'].choices = cargarModulosCurr()
        
    def clean_planificacion(self):
        plan = self.cleaned_data['planificacion']
        if plan=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la planificación"))
        return self.cleaned_data['planificacion']
    
    def clean_profesor(self):
        profesor = self.cleaned_data['profesor']
        if profesor=="0":
            raise forms.ValidationError(_(u"Debe seleccionar al profesor"))
        return self.cleaned_data['profesor']
    
    def clean_modulo(self):
        modulo = self.cleaned_data['modulo']
        if modulo=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el módulo"))
        return self.cleaned_data['modulo']