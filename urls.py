from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^esmayoy/', include('esmayoy.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^indice/?$','comun.views.inicio'),
    (r'^', include('usuario.urls')),
    (r'^inscripcion/', include('inscripcion.urls')),
    (r'^institucion/', include('institucion.urls')),
    (r'^unidadcurricular/', include('unidadcurricular.urls')),
    (r'^academico/', include('academico.urls')),
    (r'^horario/', include('horario.urls')),
    (r'^planificacion/', include('planificacion.urls')),
    (r'^planta/', include('planta.urls')),
    (r'^config/', include('configuracion.urls')),
    (r'^logs/',include('comun.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), "media")}),
    (r'^tmp/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), "tmp")}),
    #(r'^docs/manualenlinea/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), "docs/manualenlinea")}),
    (r'^docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), "docs/")}),
    (r'^%s/' % settings.DAJAX_MEDIA_PREFIX, include('dajax.urls')),
    (r'^', 'comun.views.inicio'),
)