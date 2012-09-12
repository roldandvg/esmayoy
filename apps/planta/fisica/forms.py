#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS, SEMANA
from comun.funciones import cargarTiposEdificios, cargarEdificios, cargarTiposAulas, cargarAulas, cargarCarrerasSede

class FormTipoAula(forms.Form):
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la descripción del tipo de aula'), 'tabindex':'1'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
class FormTipoEdificio(forms.Form):
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la descripción del tipo de edificio'), 'tabindex':'1'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
class FormEdificio(forms.Form):
    cod_edif = forms.CharField(label=_(u"Código edificio:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el código del edificio'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la descripción del edificio'), 'tabindex':'2'}))
    nro_aulas = forms.IntegerField(label=_(u"Nro. de aulas:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique el número de aulas disponibles en el edificio'), 'tabindex':'4'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'250', 'title':_(u'Indique alguna observación'), 'tabindex':'6'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'5'}))
    tipo_edificio = forms.ChoiceField(label=_(u'Tipo de edificio:'), choices=cargarTiposEdificios(), widget=forms.Select(attrs={'title':_(u'Seleccione el tipo de edificio'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnau = "<div id='ayudanau' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpted = "<div id='ayudated' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormEdificio, self).__init__(*args, **kwargs)
        self.fields['tipo_edificio'].choices = cargarTiposEdificios()
        
    def clean_tipo_edificio(self):
        tpedif = self.cleaned_data['tipo_edificio']
        if tpedif=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el tipo de edificio"))
        return self.cleaned_data['tipo_edificio']
        
class FormAula(forms.Form):
    cod_aula = forms.CharField(label=_(u"Código aula:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el código del aula'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la descripción del aula'), 'tabindex':'2'}))
    capacidad = forms.IntegerField(label=_(u"Capacidad:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la capacidad de alumnos del aula'), 'tabindex':'5'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'250', 'title':_(u'Indique alguna observación'), 'tabindex':'7'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'6'}))
    edificio = forms.ChoiceField(label=_(u'Edificio:'), choices=cargarEdificios(), widget=forms.Select(attrs={'title':_(u'Seleccione el edificio'), 'tabindex':'3'}))
    tipo_aula = forms.ChoiceField(label=_(u'Tipo de aula:'), choices=cargarTiposAulas(), widget=forms.Select(attrs={'title':_(u'Seleccione el tipo de aula'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcap = "<div id='ayudacap' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpedi = "<div id='ayudaedi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptau = "<div id='ayudatau' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormAula, self).__init__(*args, **kwargs)
        self.fields['edificio'].choices = cargarEdificios()
        self.fields['tipo_aula'].choices = cargarTiposAulas()
        
    def clean_edificio(self):
        edificio = self.cleaned_data['edificio']
        if edificio == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el edificio"))
        return self.cleaned_data['edificio']
    
    def clean_tipo_aula(self):
        tpaula = self.cleaned_data['tipo_aula']
        if tpaula=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el tipo de aula"))
        return self.cleaned_data['tipo_aula']
        
class FormAulaCarrera(forms.Form):
    observaciones = forms.CharField(label=_(u"Observación:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':'Indique las observaciones del aula', 'tabindex':'6'}), required=False)
    fecha_asignacion = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de asignación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':'Indique la fecha de asignación del aula a la carrera', 'readonly':'readonly', 'tabindex':'1'}))
    semana = forms.MultipleChoiceField(label=_(u"Días:"), choices=SEMANA, widget=forms.CheckboxSelectMultiple(attrs={'title': 'Seleccione los días en los cuales el aula estará asignada a la carrera', 'size':SEMANA.__len__(), 'tabindex':'5'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':'Seleccione el estatus', 'tabindex':'2'}))
    aula = forms.ChoiceField(label=_(u'Aula:'), choices=cargarAulas(), widget=forms.Select(attrs={'title':'Seleccione un aula', 'tabindex':'3'}))
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':'Seleccione una carrera', 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfas = "<div id='ayudafas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpsem = "<div id='ayudasem' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpaul = "<div id='ayudaaul' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcas = "<div id='ayudacas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormAulaCarrera, self).__init__(*args, **kwargs)
        self.fields['aula'].choices = cargarAulas()
        self.fields['carrsed'].choices = cargarCarrerasSede()
        
    def clean_aula(self):
        aula = self.cleaned_data['aula']
        if aula=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el aula"))
        return self.cleaned_data['aula']
    
    def clean_carrsed(self):
        carrsed = self.cleaned_data['carrsed']
        if carrsed=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrsed']