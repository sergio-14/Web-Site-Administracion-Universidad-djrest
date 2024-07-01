

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date
from django.conf import settings

User = get_user_model()

# Create your models here.
########  espacio de poryectos de interaccion social docentes  ##########

#tipo de proyecto de interaccion social docentes
class T_Tipo_Proyecto(models.Model):
    Id_tipo=models.AutoField(primary_key=True)
    S_Tipo= models.CharField(max_length=100, verbose_name='Tipo de Inv. Soc.')
    
    def __str__(self):
        return self.S_Tipo

#tipo fase de interaccion social docentes
class T_Fase_proyecto(models.Model):
    Id_fase= models.AutoField(primary_key=True)
    S_Fase=models.CharField(max_length=100,verbose_name='Fase o Etapa ')
    
    def __str__(self):
        return self.S_Fase 
    
#tipo gestion de interaccion social docentes
class T_Gestion(models.Model):
    Id_Ges=models.AutoField(primary_key=True)
    S_Gestion= models.CharField(max_length=100,verbose_name='Nombre de Gestion')
    
    def __str__(self):
        return self.S_Gestion
    
#tipo semestre de interaccion social docentes
class T_Semestre(models.Model):
    Id_Semestre= models.AutoField(primary_key=True)
    S_Semestre=models.CharField(max_length=100,verbose_name='Semestre')
    
    def __str__(self):
        return self.S_Semestre 

#tipo materia de interaccion social docentes  
class T_Materia(models.Model):
    Id_Materia= models.AutoField(primary_key=True)
    S_Materia=models.CharField(max_length=100,verbose_name='Materia')
    T_Semestre=models.ForeignKey(T_Semestre, on_delete=models.CASCADE, verbose_name="Semestre")
    def __str__(self):
        return self.S_Materia
    
#tipo agregacion de poryecto de interaccion social docentes
class T_Proyectos(models.Model):
    Id_Proyect = models.AutoField(primary_key=True)
    S_persona = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    S_Titulo = models.CharField(max_length=150, verbose_name='Titulo')
    Fecha_Inicio = models.DateField(auto_now=False, auto_now_add=False)
    Fecha_Finalizacion = models.DateField(auto_now=False, auto_now_add=False)
    S_Descripcion = models.TextField(verbose_name='Descripcion', blank=True)
    S_Documentacion = models.FileField(upload_to='Documento/', verbose_name='Documentacion', null=True)
    S_Imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
    T_Fase_proyecto = models.ForeignKey(T_Fase_proyecto, on_delete=models.CASCADE, verbose_name='Fase del Proyecto')
    T_Gestion = models.ForeignKey(T_Gestion, on_delete=models.CASCADE, verbose_name='Gestion')
    T_Tipo_Proyecto = models.ForeignKey(T_Tipo_Proyecto, on_delete=models.CASCADE, verbose_name='Tipo de Proyecto')
    T_Materia = models.ForeignKey(T_Materia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Materia')
     
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Fecha_Finalizacion < self.Fecha_Inicio:
            raise ValidationError('La fecha de finalización debe ser posterior a la fecha de inicio.')
        
    def __str__(self):
        return self.S_Titulo
    
class IntSocSettings(models.Model):
    fecha_inicio_habilitacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Inicio de Habilitación')
    fecha_fin_habilitacion = models.DateField(null=True, blank=True, verbose_name='Fecha Fin de Habilitación')

    def __str__(self):
        return "Configuración Global"

    def tiempo_restante(self):
        hoy = date.today()
        if self.fecha_fin_habilitacion and hoy <= self.fecha_fin_habilitacion:
            return (self.fecha_fin_habilitacion - hoy).days
        return None
  