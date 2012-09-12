#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS, DESICION, DEFAULT
from comun.funciones import cargarCarreras, cargarSedes, cargarCarrerasSede, cargarPensums, cargarCondicionUnidades, cargarEjesCurriculares, cargarTiposUnidades, cargarUnidadesCurriculares, compararFechas
from unidadcurricular.models import Pensum, Eje_Curricular, Condicion_Unidad, Unidad_Curricular, Prelacion, Modulo_Curricular

class FormPensum(forms.Form):
    cod_pensum = forms.CharField(label=_(u"Código Pensum:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código del pensum de estudio'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'30','maxlength':'50', 'title':_(u'Indique una descripción para el pensum'), 'tabindex':'2'}))
    finicio = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de inicio:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha en que entró en vigencia el pensum de estudio'), 'readonly':'readonly', 'tabindex':'3'}))
    ffinal = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha final:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title': _(u'Indique la fecha final de la vigencia del pensum de estudio'), 'readonly':'readonly', 'tabindex':'4'}))
    cal_min = forms.IntegerField(label=_(u"Calificación Mínima:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique la calificación mínima'), 'tabindex':'5'}))
    cal_max = forms.IntegerField(label=_(u"Calificación Máxima:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique la calificación máxima'), 'tabindex':'6'}))
    cal_apro = forms.IntegerField(label=_(u"Calificación Aprob.:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique la calificación aprobatoria'), 'tabindex':'7'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique las observaciones del pensum'), 'tabindex':'11'}), required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del pensum de estudio'), 'tabindex':'8'}))
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':_(u'Seleccione una sede'), 'tabindex':'9'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfin = "<div id='ayudafin' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpffi = "<div id='ayudaffi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcmi = "<div id='ayudacmi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcma = "<div id='ayudacma' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcap = "<div id='ayudacap' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcas = "<div id='ayudacas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormPensum, self).__init__(*args, **kwargs)
        self.fields['carrsed'].choices = cargarCarrerasSede()
        
    def clean_carrsed(self):
        carrsed = self.cleaned_data['carrsed']
        if carrsed=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrsed']
        
    def clean_cod_pensum(self):
        cod_pensum = self.cleaned_data['cod_pensum']
        modificar = self.data['modificar']
        if Pensum.objects.filter(pk=cod_pensum) and modificar=="":
            raise forms.ValidationError(_(u"El código ya existe"))
        return self.cleaned_data['cod_pensum']
    
    def clean_finicio(self):
        finicio = self.data['finicio']
        ffinal = self.data['ffinal']
        if not compararFechas(str(finicio),str(ffinal)):
            raise forms.ValidationError(_(u"La fecha de inicio debe ser menor a la fecha final"))
        return self.cleaned_data['finicio']
    
    def clean_ffinal(self):
        finicio = self.data['finicio']
        ffinal = self.data['ffinal']
        hoy = datetime.strftime(datetime.now(), "%d/%m/%Y")
        if not compararFechas(hoy,ffinal):
            raise forms.ValidationError(_(u"La fecha final no puede ser igual a la actual"))
        elif not compararFechas(str(finicio),str(ffinal)):
            raise forms.ValidationError(_(u"La fecha final debe ser mayor a la fecha inicial"))
        return self.cleaned_data['ffinal']
    
        
class FormEjeCurricular(forms.Form):
    cod_eje = forms.CharField(label=_(u"Cód del eje curricular:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el código del eje curricular'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'150', 'title':_(u'Indique la descripcion del eje curricular'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_cod_eje(self):
        cod_eje = self.cleaned_data['cod_eje']
        modificar = self.data['modificar']
        if Eje_Curricular.objects.filter(pk=cod_eje) and modificar=="":
            raise forms.ValidationError(_(u"El código ya existe"))
        return self.cleaned_data['cod_eje']
    
class FormCondicionUnidad(forms.Form):
    cond_unidad = forms.CharField(label=_(u"Condición Unidad:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código de la condición de la unidad curricular'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique la descripcion de la condición de la unidad curricular'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_cond_unidad(self):
        cond_unidad = self.cleaned_data['cond_unidad']
        modificar = self.data['modificar']
        if Condicion_Unidad.objects.filter(pk=cond_unidad) and modificar=="":
            raise forms.ValidationError(_(u"El código ya existe"))
        return self.cleaned_data['cond_unidad']
    
class FormTipoUnidadCurr(forms.Form):
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique la descripcion del tipo de unidad curricular'), 'tabindex':'1'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")

class FormUnidadCurricular(forms.Form):
    id_unidad = forms.IntegerField(label=_(u"ID de Unidad:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique el identificador de la unidad curricular'), 'tabindex':'1'}))
    cod_unidad = forms.CharField(label=_(u"Código de Unidad:"), widget=forms.TextInput(attrs={'size':'15', 'maxlength':'15', 'title':_(u'Indique el código de la unidad curricular'), 'tabindex':'2'}))
    nombre = forms.CharField(label=_(u"Nombre:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'80', 'title':_(u'Indique el nombre de la unidad curricular'), 'tabindex':'3'}))
    ucr = forms.IntegerField(label=_(u"Unidades de Crédito"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique las unidades de crédito para esta unidad curricular'), 'tabindex':'5'}))
    pre_ucr = forms.IntegerField(label=_(u"Pre Unidades de Crédito"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique las unidades de crédito necesarias para cursar esta unidad curricular'), 'tabindex':'6'}))
    obligatoria = forms.ChoiceField(label=_(u'Obligatoria:'), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si la unidad curricular es obligatoria o no'), 'tabindex':'4'}))
    trayecto = forms.IntegerField(label=_(u"Trayecto:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el trayecto al cual pertenece la unidad curricular'), 'tabindex':'7'}))
    trimestre = forms.IntegerField(label=_(u"Trimestre:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el trimestre al cual pertenece la unidad curricular'), 'tabindex':'8'}), required=False)
    cant_mod = forms.IntegerField(label=_(u"Cantidad Modalidad:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la cantidad de modalidades de la unidad curricular'), 'tabindex':'9'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la unidad curricular'), 'tabindex':'10'}))
    hilo = forms.ChoiceField(label=_(u'Hilo:'), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si la unidad curricular es parte de un hilo'), 'tabindex':'11'}))
    pensum = forms.ChoiceField(label=_(u'Pensum:'), choices=cargarPensums(), widget=forms.Select(attrs={'title':_(u'Seleccione un pensum de estudio'), 'tabindex':'12'}))
    condicionunidad = forms.ChoiceField(label=_(u'Condición de Unidad:'), choices=cargarCondicionUnidades(), widget=forms.Select(attrs={'title':_(u'Seleccione una condición de la unidad curricular'), 'tabindex':'13'}))
    ejecurricular = forms.ChoiceField(label=_(u'Eje Curricular:'), choices=cargarEjesCurriculares(), widget=forms.Select(attrs={'title':_(u'Seleccione un eje curricular'), 'tabindex':'14'}))
    tipounidad = forms.ChoiceField(label=_(u'Tipo de Unidad:'), choices=cargarTiposUnidades(), widget=forms.Select(attrs={'title':_(u'Seleccione un tipo de unidad curricular'), 'tabindex':'15'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpidu = "<div id='ayudaidu' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom = "<div id='ayudanom' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpucr = "<div id='ayudaucr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppuc = "<div id='ayudapuc' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobl = "<div id='ayudaobl' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptra = "<div id='ayudatra' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptri = "<div id='ayudatri' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcmo = "<div id='ayudacmo' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helphil = "<div id='ayudahil' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppen = "<div id='ayudapen' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpeje = "<div id='ayudaeje' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptun = "<div id='ayudatun' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormUnidadCurricular, self).__init__(*args, **kwargs)
        self.fields['pensum'].choices = cargarPensums()
        self.fields['condicionunidad'].choices = cargarCondicionUnidades()
        self.fields['ejecurricular'].choices = cargarEjesCurriculares()
        self.fields['tipounidad'].choices = cargarTiposUnidades()
        
    def clean_id_unidad(self):
        id_unidad = self.cleaned_data['id_unidad']
        modificar = self.data['modificar']
        if Unidad_Curricular.objects.filter(pk=id_unidad) and modificar=="":
            raise forms.ValidationError(_(u"El ID de la unidad ya existe"))
        return self.cleaned_data['id_unidad']
    
    def clean_pensum(self):
        pensum = self.cleaned_data['pensum']
        if pensum =="0":
            raise forms.ValidationError(_(u"Debe seleccionar el pensum"))
        return self.cleaned_data['pensum']
    
    def clean_condicionunidad(self):
        cond = self.cleaned_data['condicionunidad']
        if cond == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la condición"))
        return self.cleaned_data['condicionunidad']
    
    def clean_ejecurricular(self):
        eje = self.cleaned_data['ejecurricular']
        if eje=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el eje"))
        return self.cleaned_data['ejecurricular']
    
    def clean_tipounidad(self):
        tpu = self.cleaned_data['tipounidad']
        if tpu == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el tipo de unidad"))
        return self.cleaned_data['tipounidad']
        
class FormPrelacion(forms.Form):
    cod_prela = forms.IntegerField(label=_(u"Código de Prelación:"), widget=forms.TextInput(attrs={'size':'6', 'maxlength':'6', 'title':_(u'Indique el código de prelación de la unidad curricular'), 'tabindex':'1'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la prelación de la unidad curricular'), 'tabindex':'2'}))
    unidadcurr = forms.ChoiceField(label=_(u'Unidad Curricular:'), choices=cargarUnidadesCurriculares(), widget=forms.Select(attrs={'title':_(u'Seleccione una unidad curricular'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpund = "<div id='ayudaund' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormPrelacion, self).__init__(*args, **kwargs)
        self.fields['unidadcurr'].choices = cargarUnidadesCurriculares()
        
    def clean_cod_prela(self):
        cod_prela = self.cleaned_data['cod_prela']
        modificar = self.data['modificar']
        if Prelacion.objects.filter(pk=cod_prela) and modificar=="":
            raise forms.ValidationError(_(u"El código ya existe"))
        elif not str(cod_prela).isdigit():
            raise forms.ValidationError(_(u"El código debe ser un número entero"))
        return self.cleaned_data['cod_prela']
    
    def clean_unidadcurr(self):
        unidad = self.cleaned_data['unidadcurr']
        if unidad == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la unidad"))
        return self.cleaned_data['unidadcurr']
        
class FormModCurricular(forms.Form):
    cod_modulo = forms.CharField(label=_(u"Código del Módulo:"), widget=forms.TextInput(attrs={'size':'15', 'maxlength':'15', 'title':_(u'Indique el código del módulo curricular'), 'tabindex':'1'}))
    nombre = forms.CharField(label=_(u"Nombre:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'250', 'title':_(u'Indique el nombre del módulo curricular'), 'tabindex':'2'}))
    ucr = forms.IntegerField(label=_(u"Unidades de Crédito"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique las unidades de crédito para este módulo curricular'), 'tabindex':'3'}))
    trayecto = forms.IntegerField(label=_(u"Trayecto:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el trayecto al cual pertenece el módulo curricular'), 'tabindex':'5'}))
    trimestre = forms.IntegerField(label=_(u"Trimestre:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el trimestre al cual pertenece el módulo curricular'), 'tabindex':'6'}))
    porcentaje = forms.DecimalField(label=_(u"Porcentaje"), widget=forms.TextInput(attrs={'size':'6', 'maxlength':'8', 'title':_(u'Indique el porcentaje para este módulo curricular'), 'tabindex':'4'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del módulo curricular'), 'tabindex':'8'}))
    unidadcurr = forms.ChoiceField(label=_(u'Unidad Curricular:'), choices=cargarUnidadesCurriculares(), widget=forms.Select(attrs={'title':_(u'Seleccione una unidad curricular'), 'tabindex':'7'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom = "<div id='ayudanom' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpucr = "<div id='ayudaucr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptra = "<div id='ayudatra' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptri = "<div id='ayudatri' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppor = "<div id='ayudapor' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpund = "<div id='ayudaund' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormModCurricular, self).__init__(*args, **kwargs)
        self.fields['unidadcurr'].choices = cargarUnidadesCurriculares()
        
    def clean_cod_modulo(self):
        cod_modulo = self.cleaned_data['cod_modulo']
        modificar = self.data['modificar']
        if Modulo_Curricular.objects.filter(pk=cod_modulo) and modificar=="":
            raise forms.ValidationError(_(u"El código ya existe"))
        return self.cleaned_data['cod_modulo']
    
    def clean_unidadcurr(self):
        unidad = self.cleaned_data['unidadcurr']
        if unidad == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la unidad"))
        return self.cleaned_data['unidadcurr']