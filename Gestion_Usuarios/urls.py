from django.urls import path
from .views import (
    home, iniciar_sesion, registrar, signout, dashboard,
    listar_usuarios, crear_usuario, actualizar_usuario, eliminar_usuario
)
from django.conf import settings
from django.conf.urls.static import static
from Gestion_Usuarios import views

urlpatterns = [
    # Gestión De Usuarios
    path('', home, name='home'),
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('registrar/', registrar, name='registrar'),
    path('logout/', signout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # DASHBOARD/CRUD
    #Usuarios
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/actualizar/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/inactivos/', views.listar_usuarios_inactivos, name='listar_usuarios_inactivos'),
    path('usuarios/<int:pk>/reactivar/', views.reactivar_usuario, name='reactivar_usuario'),
    #grupos
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/<int:pk>/actualizar/', views.actualizar_grupo, name='actualizar_grupo'),
    path('grupos/<int:pk>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
