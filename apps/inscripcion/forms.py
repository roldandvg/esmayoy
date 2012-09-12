#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import DEFAULT
from comun.funciones import cargarEstatusInscanual, cargarEstatusInsctrimestral, cargarAnualidades, cargarUnidadesCurriculares, cargarModulosCurr, cargarTrimestres, cargarInscripcionAnual

class FormEstatusInscanual(forms.Form):
    estatus = forms.CharField(label=_(u"Estatus:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique un estatus'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique una descripción'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
class FormEstatusInsctrimestral(forms.Form):
    estatus = forms.CharField(label=_(u"Estatus:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique un estatus'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique una descripción'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
class FormInscripcionAnual(forms.Form):
    seccion = forms.CharField(label=_(u"Sección:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique la sección'), 'tabindex':'5'}))
    nota = forms.IntegerField(label=_(u"Nota:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la nota'), 'tabindex':'6'}))
    asistencia = forms.IntegerField(label=_(u"Asistencia:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la asistencia'), 'tabindex':'7'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=cargarEstatusInscanual(), widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la inscripción'), 'tabindex':'8'}))
    cedula = forms.CharField(label=_(u"Cédula:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title': _(u'Indique la cédula de identidad del alumno'), 'tabindex':'1'}), required=False)
    nombre = forms.CharField(label=_(u"Alumno:"), widget=forms.TextInput(attrs={'size':'40', 'readonly':'readonly', 'title':_(u'Nombre y apellido del alumno'), 'tabindex':'2'}), required=False)
    anualidad = forms.ChoiceField(label=_(u"Anualidad:"), choices=cargarAnualidades(), widget=forms.Select(attrs={'title':_(u'Seleccione la anualidad'), 'tabindex':'3'}))
    unidad = forms.ChoiceField(label=_(u"Unidad Curricular:"), choices=cargarUnidadesCurriculares(), widget=forms.Select(attrs={'title':_(u'Seleccione la unidad curricular'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpsec  = "<div id='ayudasec'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnota = "<div id='ayudanota' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpasis = "<div id='ayudasis'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpci   = "<div id='ayudaci'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom  = "<div id='ayudanom'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpanu  = "<div id='ayudaanu'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpund  = "<div id='ayudaund'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormInscripcionAnual, self).__init__(*args, **kwargs)
        self.fields['estatus'].choices = cargarEstatusInscanual()
        self.fields['anualidad'].choices = cargarAnualidades()
        self.fields['unidad'].choices = cargarUnidadesCurriculares()
        
    def clean_estatus(self):
        estatus = self.cleaned_data['estatus']
        if estatus=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el estatus"))
        return self.cleaned_data['estatus']
    
    def clean_anualidad(self):
        anualidad = self.cleaned_data['anualidad']
        if anualidad=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la anualidad"))
        return self.cleaned_data['anualidad']
    
    def clean_unidad(self):
        unidad = self.cleaned_data['unidad']
        if unidad=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la unidad"))
        return self.cleaned_data['unidad']
    
class FormHito(forms.Form):
    seccion = forms.CharField(label=_(u"Sección:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique la sección'), 'tabindex':'7'}))
    nota = forms.IntegerField(label=_(u"Nota:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la nota'), 'tabindex':'8'}))
    cedula = forms.CharField(label=_(u"Cédula:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title': _(u'Indique la cédula de identidad del alumno'), 'tabindex':'1'}), required=False)
    nombre = forms.CharField(label=_(u"Alumno:"), widget=forms.TextInput(attrs={'size':'40', 'readonly':'readonly', 'title':_(u'Nombre y apellido del alumno'), 'tabindex':'2'}), required=False)
    inscripcion_anual = forms.ChoiceField(label=_(u"Inscripción Anual:"), choices=DEFAULT, widget=forms.Select(attrs={'title':_(u'Seleccione la inscripción anual'), 'tabindex':'3'}))
    modulo_curricular = forms.ChoiceField(label=_(u"Módulo Curricular:"), choices=cargarModulosCurr(), widget=forms.Select(attrs={'title':_(u'Seleccione el módulo curricular'), 'tabindex':'4'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=cargarEstatusInscanual(), widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la inscripción'), 'tabindex':'6'}))
    trimestre = forms.ChoiceField(label=_(u"Trimestre:"), choices=cargarTrimestres(), widget=forms.Select(attrs={'title':_(u'Seleccione el trimestre'), 'tabindex':'5'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpsec  = "<div id='ayudasec'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnota = "<div id='ayudanota' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpci   = "<div id='ayudaci'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom  = "<div id='ayudanom'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpins  = "<div id='ayudains'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpmod  = "<div id='ayudamod'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptri  = "<div id='ayudatri'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormHito, self).__init__(*args, **kwargs)
        self.fields['estatus'].choices = cargarEstatusInscanual()
        self.fields['modulo_curricular'].choices = cargarModulosCurr()
        self.fields['trimestre'].choices = cargarTrimestres()
        self.fields['inscripcion_anual'].choices = cargarInscripcionAnual()
        
    def clean_estatus(self):
        estatus = self.cleaned_data['estatus']
        if estatus=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el estatus"))
        return self.cleaned_data['estatus']
    
    def clean_modulo_curricular(self):
        modulo = self.cleaned_data['modulo_curricular']
        if modulo=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el módulo"))
        return self.cleaned_data['modulo_curricular']
    
    def clean_trimestre(self):
        trimestre = self.cleaned_data['trimestre']
        if trimestre=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el trimestre"))
        return self.cleaned_data['trimestre']
        
class FormInscripcionTrimestral(forms.Form):
    seccion = forms.CharField(label=_(u"Sección:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique la sección'), 'tabindex':'7'}))
    nota = forms.IntegerField(label=_(u"Nota:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la nota'), 'tabindex':'8'}))
    asistencia = forms.IntegerField(label=_(u"Asistencia:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la asistencia'), 'tabindex':'9'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=cargarEstatusInsctrimestral(), widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la inscripción'), 'tabindex':'6'}))
    cedula = forms.CharField(label=_(u"Cédula:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title': _(u'Indique la cédula de identidad del alumno'), 'tabindex':'1'}), required=False)
    nombre = forms.CharField(label=_(u"Alumno:"), widget=forms.TextInput(attrs={'size':'40', 'readonly':'readonly', 'title':_(u'Nombre y apellido del alumno'), 'tabindex':'2'}), required=False)
    inscripcion_anual = forms.ChoiceField(label=_(u"Inscripción Anual:"), choices=DEFAULT, widget=forms.Select(attrs={'title':_(u'Seleccione la inscripción anual'), 'tabindex':'3'}))
    modulo_curricular = forms.ChoiceField(label=_(u"Módulo Curricular:"), choices=cargarModulosCurr(), widget=forms.Select(attrs={'title':_(u'Seleccione el módulo curricular'), 'tabindex':'4'}))
    trimestre = forms.ChoiceField(label=_(u"Trimestre:"), choices=cargarTrimestres(), widget=forms.Select(attrs={'title':_(u'Seleccione el trimestre'), 'tabindex':'5'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpsec  = "<div id='ayudasec'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnota = "<div id='ayudanota' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpasis = "<div id='ayudaasis' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpci   = "<div id='ayudaci'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom  = "<div id='ayudanom'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpins  = "<div id='ayudains'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpmod  = "<div id='ayudamod'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptri  = "<div id='ayudatri'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormInscripcionTrimestral, self).__init__(*args, **kwargs)
        self.fields['estatus'].choices = cargarEstatusInsctrimestral()
        self.fields['modulo_curricular'].choices = cargarModulosCurr()
        self.fields['trimestre'].choices = cargarTrimestres()
        self.fields['inscripcion_anual'].choices = cargarInscripcionAnual()
        
    def clean_estatus(self):
        estatus = self.cleaned_data['estatus']
        if estatus=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el estatus"))
        return self.cleaned_data['estatus']
    
    def clean_modulo_curricular(self):
        modulo = self.cleaned_data['modulo_curricular']
        if modulo=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el módulo"))
        return self.cleaned_data['modulo_curricular']
    
    def clean_trimestre(self):
        trimestre = self.cleaned_data['trimestre']
        if trimestre=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el trimestre"))
        return self.cleaned_data['trimestre']