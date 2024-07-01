from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403
from .views import handle_permission_denied
from Seg_Mod_Graduacion import views

urlpatterns = [    
    #segguimiento modalidad de graduacion investigacion cientifica
    path('invcientifica/agregar_investigacion/', views.agregar_investigacion, name='agregar_investigacion'),
    path('invcientifica/vista_investigacion/',views.vista_investigacion, name='vista_investigacion'),
    path('invcientifica/ProyectosParaAprobar/', views.ProyectosParaAprobar.as_view(), name='ProyectosParaAprobar'),
    path('AprobarProyecto/<int:proyecto_id>/', views.AprobarProyecto.as_view(), name='AprobarProyecto'),
    path('RechazarProyecto/<int:proyecto_id>/', views.RechazarProyecto.as_view(), name='RechazarProyecto'),
    path('invcientifica/global_settings/', views.global_settings_view, name='global_settings'),
    
    #seguimiento modalidad de graduacion perfil de proyecto
    path('perfil/agregar_perfil/', views.agregar_perfil, name='agregar_perfil'),
    path('perfil/vista_perfil/',views.vista_perfil, name='vista_perfil'),
    path('perfil/PerfilesParaAprobar/', views.PerfilesParaAprobar.as_view(), name='PerfilesParaAprobar'),
    path('AprobarPerfil/<int:proyecto_id>/', views.AprobarPerfil.as_view(), name='AprobarPerfil'),
    path('RechazarPerfil/<int:proyecto_id>/', views.RechazarPerfil.as_view(), name='RechazarPerfil'),

    #seguimiento modalidad de graduacion proyecto final
    path('proyectofinal/agregar_proyecto_final/', views.agregar_proyecto_final, name='agregar_proyecto_final'),
    path('proyectofinal/RevisarProyectoFinal/', views.RevisarProyectoFinal.as_view(), name='RevisarProyectoFinal'),

]
handler403 = handle_permission_denied