from django.contrib import admin
from .models import Titulado
from .forms import TituladoForm

class TituladoAdmin(admin.ModelAdmin):
    form = TituladoForm
    list_display = ('usuario', 'proyecto_final', 'anio_ingreso', 'periodo_ingreso', 'anio_egreso', 'periodo_egreso', 'numero_acta', 'nota')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'usuario__ru')
    list_filter = ('anio_ingreso', 'anio_egreso')

admin.site.register(Titulado, TituladoAdmin)
