from django.contrib import admin

# Register your models here.
from .models import T_Fase_proyecto, T_Tipo_Proyecto, T_Gestion, T_Proyectos, T_Semestre, T_Materia

# Register interacion social
admin.site.register(T_Fase_proyecto)
admin.site.register(T_Tipo_Proyecto)
admin.site.register(T_Gestion)
admin.site.register(T_Proyectos)
admin.site.register(T_Semestre)
admin.site.register(T_Materia)