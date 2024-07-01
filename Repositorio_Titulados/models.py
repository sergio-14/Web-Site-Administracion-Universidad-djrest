from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from Seg_Mod_Graduacion.models import ProyectoFinal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

# Filtrar usuarios que están en el grupo "Estudiantes" y cuyo estado es "Aprobado"
def estudiantes_aprobados():
    return User.objects.filter(groups__name='Estudiantes', estado=True)

# Controlar que solo se permitan estos valores
PERIODO_CHOICES = [
    (1, '1'),
    (2, '2'),
]

# Modelo para Titulado, heredando datos de User y ProyectoFinal
class Titulado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Estudiantes', 'estado': True})
    proyecto_final = models.OneToOneField(ProyectoFinal, on_delete=models.CASCADE, limit_choices_to={'estado': 'Aprobado'})
    anio_ingreso = models.DateField()
    periodo_ingreso = models.IntegerField(choices=PERIODO_CHOICES)
    anio_egreso = models.DateField()
    periodo_egreso = models.IntegerField(choices=PERIODO_CHOICES)
    numero_acta = models.CharField(max_length=50)
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def clean(self):
        # Verificar que el proyecto final pertenece al usuario
        if self.proyecto_final.user != self.usuario:
            raise ValidationError('El proyecto final no pertenece al usuario seleccionado.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido} ({self.usuario.ru})"
