from django.apps import AppConfig


class RepositorioTituladosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Repositorio_Titulados'
    
    def ready(self):
        import Repositorio_Titulados.signals