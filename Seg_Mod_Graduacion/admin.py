from django.contrib import admin
from .models import InvCientifica, ProyectoFinal, TutorExterno, Materia, Modalidad, ComentarioInvCientifica, ComentarioPerfil, InvSettings, PerfilProyecto

class ProyectoFinalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha', 'estado')
    search_fields = ('titulo', 'usuario__email')
    filter_horizontal = ('tribunales',)
# Registra tus modelos aquí
admin.site.register(InvCientifica)
admin.site.register(ProyectoFinal)
admin.site.register(TutorExterno)
admin.site.register(Materia)
admin.site.register(Modalidad)
admin.site.register(ComentarioInvCientifica)
admin.site.register(ComentarioPerfil)
admin.site.register(InvSettings)
admin.site.register(PerfilProyecto)
