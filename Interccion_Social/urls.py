from django.urls import path 
from . import views
from django.conf.urls import handler403
from .views import handle_permission_denied
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('hometrabajos', views.hometrabajos, name='hometrabajos'),
    path('repoin', views.repoin, name='repoin'),
    #proyectos de interacion social
    path('homesocial/proyecto_detail/', views.proyecto_detail, name='proyecto_detail'),
    path('homesocial/clasificar_proyectos/', views.clasificar_proyectos, name='clasificar_proyectos'),
    path('homesocial/inv_soc_settings/', views.inv_soc_settings, name='inv_soc_settings'),
    path('homesocial/proyectosin_so/', views.proyectosin_so, name='proyectosin_so'),
    
    #####    tareas admin Inv. Soc.   #####
    path('Tareas/Tipo/listart/', views.listart, name='listart'),
    path('Tareas/Tipo/listart/creart/', views.creart, name='creart'),
    path('Tareas/Tipo/listart/editart/<int:pk>/', views.editart, name='editart'),
    path('Tareas/Tipo/listart/eliminart/<int:pk>/', views.eliminart, name='eliminart'),
    
    path('Tareas/FaseEtapa/listarf/', views.listarf, name='listarf'),
    path('Tareas/FaseEtapa/listarf/crearf/', views.crearf, name='crearf'),
    path('Tareas/FaseEtapa/listarf/editarf/<int:pk>/', views.editarf, name='editarf'),
    path('Tareas/FaseEtapa/listarf/eliminarf/<int:pk>/', views.eliminarf, name='eliminarf'),
    
    path('Tareas/Gestion/listarg/', views.listarg, name='listarg'),
    path('Tareas/Gestion/listarg/crearg/', views.crearg, name='crearg'),
    path('Tareas/Gestion/listarg/editarg/<int:pk>/', views.editarg, name='editarg'),
    path('Tareas/Gestion/listarg/eliminarg/<int:pk>/', views.eliminarg, name='eliminarg'),
    
    path('Tareas/Semestre/listars/', views.listars, name='listars'),
    path('Tareas/Semestre/listars/crears/', views.crears, name='crears'),
    path('Tareas/Semestre/listars/editars/<int:pk>/', views.editars, name='editars'),
    path('Tareas/Semestre/listars/eliminars/<int:pk>/', views.eliminars, name='eliminars'),
    
    path('Tareas/Materia/listarm/', views.listarm, name='listarm'),
    path('Tareas/Materia/listarm/crearm/', views.crearm, name='crearm'),
    path('Tareas/Materia/listarm/editarm/<int:pk>/', views.editarm, name='editarm'),
    path('Tareas/Materia/listarm/eliminarm/<int:pk>/', views.eliminarm, name='eliminarm'),
]
handler403 = handle_permission_denied
